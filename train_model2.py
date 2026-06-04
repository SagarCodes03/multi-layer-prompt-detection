# =========================================================
# train_model2.py
# ADVANCED PROMPT INJECTION DEFENSE TRAINING PIPELINE
# =========================================================

# =========================================================
# INSTALL FIRST IN COLAB
# =========================================================

# !pip install transformers datasets accelerate evaluate scikit-learn -q

# =========================================================
# IMPORTS
# =========================================================

import pandas as pd
import numpy as np
import torch

from datasets import (
    load_dataset,
    Dataset,
    concatenate_datasets,
    Value
)

from transformers import (

    AutoTokenizer,

    AutoModelForSequenceClassification,

    TrainingArguments,

    Trainer,

    EarlyStoppingCallback
)

from sklearn.metrics import (

    accuracy_score,

    precision_recall_fscore_support
)

# =========================================================
# CONFIG
# =========================================================

MODEL_NAME = (
    "ProtectAI/deberta-v3-base-prompt-injection-v2"
)

LOCAL_CSV = (
    "/content/combined_prompt_injection_threat_matrix_dataset.csv"
)

OUTPUT_DIR = (
    "/content/final_prompt_injection_model"
)

MAX_LENGTH = 128

# =========================================================
# LOAD LOCAL DATASET
# =========================================================

print("\nLoading Local Dataset...")

df_local = pd.read_csv(LOCAL_CSV)

df_local.columns = [

    c.lower().strip()

    for c in df_local.columns
]

df_local = df_local[["text", "label"]]

df_local = df_local.dropna()

# =========================================================
# LABEL NORMALIZATION
# =========================================================

def normalize_label(x):

    if isinstance(x, str):

        x = x.lower().strip()

        if x in [
            "safe",
            "benign",
            "normal",
            "clean"
        ]:
            return 0

        return 1

    return int(x)

df_local["label"] = df_local["label"].apply(
    normalize_label
)

ds_local = Dataset.from_pandas(df_local)

print(
    f"\nLocal Dataset Size: "
    f"{len(ds_local)}"
)

# =========================================================
# LOAD ATTACK DATASET 1
# =========================================================

print(
    "\nLoading neuralchemy/Prompt-injection-dataset..."
)

hf_attack_1 = load_dataset(

    "neuralchemy/Prompt-injection-dataset",

    split="train"
)

hf_attack_1 = hf_attack_1.remove_columns(

    [c for c in hf_attack_1.column_names

     if c not in ["text", "label"]]
)

hf_attack_1 = hf_attack_1.cast_column(
    "label",
    Value("int64")
)

print(
    f"HF Attack Dataset 1 Size: "
    f"{len(hf_attack_1)}"
)

# =========================================================
# LOAD ATTACK DATASET 2
# =========================================================

print(
    "\nLoading deepset/prompt-injections..."
)

hf_attack_2 = load_dataset(

    "deepset/prompt-injections",

    split="train"
)

hf_attack_2 = hf_attack_2.remove_columns(

    [c for c in hf_attack_2.column_names

     if c not in ["text", "label"]]
)

hf_attack_2 = hf_attack_2.cast_column(
    "label",
    Value("int64")
)

print(
    f"HF Attack Dataset 2 Size: "
    f"{len(hf_attack_2)}"
)

# =========================================================
# LOAD SAFE DATASET 1
# =========================================================

print(
    "\nLoading Anthropic/hh-rlhf..."
)

safe_ds_1 = load_dataset(

    "Anthropic/hh-rlhf",

    split="train"
)

safe_df_1 = pd.DataFrame({

    "text": safe_ds_1["chosen"][:8000],

    "label": [0] * 8000
})

safe_df_1 = safe_df_1.dropna()

safe_dataset_1 = Dataset.from_pandas(
    safe_df_1
)

print(
    f"Safe Dataset 1 Size: "
    f"{len(safe_dataset_1)}"
)

# =========================================================
# LOAD SAFE DATASET 2
# =========================================================

print(
    "\nLoading OpenAssistant/oasst1..."
)

safe_ds_2 = load_dataset(

    "OpenAssistant/oasst1",

    split="train"
)

safe_texts = []

for text in safe_ds_2["text"][:10000]:

    if text is not None:

        safe_texts.append(str(text))

safe_df_2 = pd.DataFrame({

    "text": safe_texts,

    "label": [0] * len(safe_texts)
})

safe_dataset_2 = Dataset.from_pandas(
    safe_df_2
)

print(
    f"Safe Dataset 2 Size: "
    f"{len(safe_dataset_2)}"
)

# =========================================================
# LOAD SAFE DATASET 3
# =========================================================

print(
    "\nLoading yahma/alpaca-cleaned..."
)

safe_ds_3 = load_dataset(

    "yahma/alpaca-cleaned",

    split="train"
)

alpaca_texts = []

for i in range(6000):

    instruction = str(
        safe_ds_3[i]["instruction"]
    )

    inp = str(
        safe_ds_3[i]["input"]
    )

    output = str(
        safe_ds_3[i]["output"]
    )

    combined = (
        instruction + " " +
        inp + " " +
        output
    )

    alpaca_texts.append(combined)

safe_df_3 = pd.DataFrame({

    "text": alpaca_texts,

    "label": [0] * len(alpaca_texts)
})

safe_dataset_3 = Dataset.from_pandas(
    safe_df_3
)

print(
    f"Safe Dataset 3 Size: "
    f"{len(safe_dataset_3)}"
)

# =========================================================
# COMBINE ALL DATASETS
# =========================================================

print("\nCombining Datasets...")

final_dataset = concatenate_datasets([

    ds_local,

    hf_attack_1,

    hf_attack_2,

    safe_dataset_1,

    safe_dataset_2,

    safe_dataset_3
])

# =========================================================
# REMOVE BAD TEXT
# =========================================================

final_dataset = final_dataset.filter(

    lambda x:
    x["text"] is not None
)

final_dataset = final_dataset.filter(

    lambda x:
    isinstance(x["text"], str)
)

final_dataset = final_dataset.filter(

    lambda x:
    len(x["text"].strip()) > 5
)

# =========================================================
# SHUFFLE
# =========================================================

final_dataset = final_dataset.shuffle(
    seed=42
)

# =========================================================
# CHECK CLASS DISTRIBUTION
# =========================================================

labels = final_dataset["label"]

safe_count = labels.count(0)

attack_count = labels.count(1)

print("\nClass Distribution Before Balancing")

print(f"SAFE   : {safe_count}")

print(f"ATTACK : {attack_count}")

# =========================================================
# BALANCE DATASET
# =========================================================

print("\nBalancing Dataset...")

safe_subset = final_dataset.filter(
    lambda x: x["label"] == 0
)

attack_subset = final_dataset.filter(
    lambda x: x["label"] == 1
)

min_size = min(

    len(safe_subset),

    len(attack_subset)
)

safe_subset = safe_subset.shuffle(
    seed=42
).select(range(min_size))

attack_subset = attack_subset.shuffle(
    seed=42
).select(range(min_size))

balanced_dataset = concatenate_datasets([

    safe_subset,

    attack_subset
])

balanced_dataset = balanced_dataset.shuffle(
    seed=42
)

# =========================================================
# FINAL CLASS DISTRIBUTION
# =========================================================

final_labels = balanced_dataset["label"]

final_safe = final_labels.count(0)

final_attack = final_labels.count(1)

print("\nBalanced Dataset Ready!")

print(f"SAFE   : {final_safe}")

print(f"ATTACK : {final_attack}")

print(
    f"\nTotal Dataset Size: "
    f"{len(balanced_dataset)}"
)

# =========================================================
# LOAD TOKENIZER
# =========================================================

print("\nLoading Tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

# =========================================================
# TOKENIZATION
# =========================================================

def tokenize_function(examples):

    texts = [

        str(x)

        for x in examples["text"]
    ]

    return tokenizer(

        texts,

        padding="max_length",

        truncation=True,

        max_length=MAX_LENGTH
    )

print("\nTokenizing Dataset...")

tokenized_dataset = balanced_dataset.map(

    tokenize_function,

    batched=True,

    remove_columns=["text"]
)

# =========================================================
# ENSURE LABELS ARE INT
# =========================================================

def cast_labels(example):

    example["label"] = int(
        example["label"]
    )

    return example

tokenized_dataset = tokenized_dataset.map(
    cast_labels
)

# =========================================================
# TRAIN TEST SPLIT
# =========================================================

dataset_split = tokenized_dataset.train_test_split(

    test_size=0.2,

    seed=42
)

train_dataset = dataset_split["train"]

test_dataset = dataset_split["test"]

# =========================================================
# LOAD MODEL
# =========================================================

print("\nLoading Security Model...")

model = AutoModelForSequenceClassification.from_pretrained(

    MODEL_NAME,

    num_labels=2
)

# =========================================================
# ENABLE GRADIENT CHECKPOINTING
# =========================================================

model.gradient_checkpointing_enable()

# =========================================================
# METRICS
# =========================================================

def compute_metrics(eval_pred):

    logits, labels = eval_pred

    predictions = np.argmax(
        logits,
        axis=-1
    )

    precision, recall, f1, _ = (
        precision_recall_fscore_support(

            labels,

            predictions,

            average="binary"
        )
    )

    accuracy = accuracy_score(
        labels,
        predictions
    )

    return {

        "accuracy": accuracy,

        "precision": precision,

        "recall": recall,

        "f1": f1
    }

# =========================================================
# TRAINING ARGUMENTS
# =========================================================

training_args = TrainingArguments(

    output_dir=OUTPUT_DIR,

    eval_strategy="epoch",

    save_strategy="epoch",

    learning_rate=2e-5,

    per_device_train_batch_size=8,

    per_device_eval_batch_size=8,

    gradient_accumulation_steps=2,

    num_train_epochs=3,

    weight_decay=0.01,

    warmup_ratio=0.1,

    logging_steps=50,

    load_best_model_at_end=True,

    metric_for_best_model="f1",

    greater_is_better=True,

    fp16=torch.cuda.is_available(),

    save_total_limit=2,

    report_to="none"
)

# =========================================================
# TRAINER
# =========================================================

trainer = Trainer(

    model=model,

    args=training_args,

    train_dataset=train_dataset,

    eval_dataset=test_dataset,

    compute_metrics=compute_metrics,

    callbacks=[

        EarlyStoppingCallback(
            early_stopping_patience=2
        )
    ]
)

# =========================================================
# TRAIN MODEL
# =========================================================

print("\n🚀 Starting Training...\n")

trainer.train()

# =========================================================
# FINAL EVALUATION
# =========================================================

print("\nEvaluating Model...\n")

results = trainer.evaluate()

print("\nFinal Results:\n")

for k, v in results.items():

    print(f"{k}: {v}")

# =========================================================
# SAVE MODEL
# =========================================================

print("\nSaving Fine-Tuned Model...\n")

trainer.save_model(OUTPUT_DIR)

tokenizer.save_pretrained(OUTPUT_DIR)

print(

    f"\nModel Saved Successfully To:\n"

    f"{OUTPUT_DIR}"
)