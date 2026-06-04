# data_processing.py

import torch
import pandas as pd

from torch.utils.data import Dataset

from transformers import AutoTokenizer

# IMPORTANT
from preprocess import clean_text


class TextDataset(Dataset):

    def __init__(
        self,
        csv_file,
        tokenizer,
        max_len=256
    ):

        self.df = pd.read_csv(csv_file)

        self.tokenizer = tokenizer

        self.max_len = max_len

        # remove nulls
        self.df = self.df.dropna()

        # preprocess dataset text
        self.df["text"] = self.df["text"].astype(str).apply(clean_text)

    def __len__(self):

        return len(self.df)

    def __getitem__(self, idx):

        text = str(self.df.iloc[idx]["text"])

        label = int(self.df.iloc[idx]["label"])

        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_len,
            return_tensors="pt"
        )

        return {

            "input_ids":
                encoding["input_ids"].flatten(),

            "attention_mask":
                encoding["attention_mask"].flatten(),

            "labels":
                torch.tensor(label, dtype=torch.long)
        }


