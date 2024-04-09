# This script needs these libraries to be installed:
#   numpy, transformers, datasets

import wandb

import os
import numpy as np
from datasets import load_dataset
from transformers import TrainingArguments, Trainer
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {"accuracy": np.mean(predictions == labels)}


# download prepare the data - selected poetry dataset 
dataset = load_dataset("yelp_review_full")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# reduced the range of training examples to 300 to make it run faster
small_train_dataset = dataset["train"].shuffle(seed=42).select(range(300))

# reduced the range of evaluation samples to 50 to make it run faster
small_eval_dataset = dataset["test"].shuffle(seed=42).select(range(50))

small_train_dataset = small_train_dataset.map(tokenize_function, batched=True)
small_eval_dataset = small_train_dataset.map(tokenize_function, batched=True)

# download the model
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=5
)

# set the wandb project where this run will be logged
os.environ["WANDB_PROJECT"] = "my-awesome-project"

# save your trained model checkpoint to wandb
os.environ["WANDB_LOG_MODEL"] = "true"

# turn off watch to log faster
os.environ["WANDB_WATCH"] = "false"

# pass "wandb" to the `report_to` parameter to turn on wandb logging
training_args = TrainingArguments(
    output_dir="models",
    report_to="wandb",
    logging_steps=5,
    per_device_train_batch_size=12,  # Reduced from 32 to 16
    per_device_eval_batch_size=12,  # Reduced from 32 to 16
    evaluation_strategy="steps",
    eval_steps=10,
    max_steps=50,
    save_steps=50,
)

# define the trainer and start training
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=small_train_dataset,
    eval_dataset=small_eval_dataset,
    compute_metrics=compute_metrics,
)
trainer.train()

# [optional] finish the wandb run, necessary in notebooks
wandb.save("wikipedia.wandb")
wandb.finish()