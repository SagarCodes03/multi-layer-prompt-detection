#%%
import bz2
import json
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load the attack prompts from the compressed JSONL file and create a DataFrame for the attack prompts with a label of 1 (indicating attacks). The DataFrame will have two columns: "text" for the attack prompts and "label" for the corresponding labels.
#%%
atack_prompts=[]
with bz2.open(r"C:\Users\Sagar Gowda H\Downloads\raw_dump_attacks.jsonl.bz2", "rt", encoding="utf-8") as f:
    for line in f:
        records = json.loads(line)
        atack_prompts.append(records["attacker_input"])

atack_df=pd.DataFrame({
    "text":atack_prompts,
    "label":1 # atacks = 1

})
#%%
# Load the non-attack prompts from the compressed JSONL file and create a DataFrame for the non-attack prompts with a label of 0 (indicating non-attacks). The DataFrame will have two columns: "text" for the non-attack prompts and "label" for the corresponding labels.
safe_df=pd.read_parquet(r"C:\Users\Sagar Gowda H\Downloads\train-00000-of-00001-a09b74b3ef9c3b56.parquet")
safe_df=safe_df[["instruction"]]
safe_df["label"]=0 # non atacks = 0
safe_df.columns=["text","label"]
# Combine the attack and non-attack DataFrames into a single DataFrame, shuffle the combined DataFrame to ensure a random distribution of attack and non-attack prompts, and reset the index of the combined DataFrame.
#%%
attack_sample = atack_df.sample(n=52002, random_state=42)
safe_sample = safe_df 
dataset = pd.concat([attack_sample, safe_sample])
dataset = dataset.sample(frac=1).reset_index(drop=True)
print(dataset.isnull().sum())
dataset = dataset.dropna(subset=["text"])
print(dataset.isnull().sum())

#%%
pd.set_option('display.max_colwidth', None)
print(dataset.head())
# %%

def clean_text(text):
    text = text.strip()
    text = text.replace("\n", " ")      # 🔥 FIX NEWLINES
    text = re.sub(r"\s+", " ", text)    # normalize spaces
    return text

dataset["text"] = dataset["text"].apply(clean_text)

#%%
train_df,test_df = train_test_split(dataset ,test_size=0.2, stratify=dataset["label"],random_state=42)
train_df,val_df = train_test_split(train_df,test_size=0.1,stratify=train_df["label"],random_state = 42)
# %%
print("Train distribution:\n", train_df["label"].value_counts(normalize=True))
print("\nVal distribution:\n", val_df["label"].value_counts(normalize=True))
print("\nTest distribution:\n", test_df["label"].value_counts(normalize=True))
# %%
vectorizer = TfidfVectorizer(
    max_features=20000,
    ngram_range=(1, 2)
)

# Fit ONLY on training data
X_train = vectorizer.fit_transform(train_df["text"])

# Transform validation and test
X_val = vectorizer.transform(val_df["text"])
X_test = vectorizer.transform(test_df["text"])

# %%
print(X_train.shape)
print(X_val.shape)
print(X_test.shape)
# %%
model = LogisticRegression(max_iter=1000)
model.fit(X_train, train_df["label"])
# %%
y_pred = model.predict(X_val)
print(classification_report(val_df["label"], y_pred))
# %%
val_temp=val_df.copy()
val_temp["predicted_label"]=y_pred
error = val_temp[val_temp["label"] != val_temp["predicted_label"]]
print("totall errors:",len(error))
print(error.head())
# %%
