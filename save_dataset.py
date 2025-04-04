# %%
from pathlib import Path

import pandas as pd

from datamodule.configs import ModelNames

import random

random.seed(0)

# Directory paths
#base_dir = Path.cwd().joinpath("data/test")
base_dir = Path.cwd().joinpath("data/val")
original_file_path = base_dir / "original_text.txt"
simplified_dir = base_dir / "simplified"

# Read the original text file
with original_file_path.open("r", encoding="utf-8") as file:
    #original_lines = file.readlines()
    original_lines = file.readlines()

# Initialize a dictionary to hold simplified lines
simplified_lines = {model: [] for model in ModelNames}

# Read each simplified text file
for model in ModelNames:
    simplified_file_path = simplified_dir / f"{model.value}.txt"
    with simplified_file_path.open("r") as file:
        #simplified_lines[model] = file.readlines()
        simplified_lines[model] = file.readlines()

# Check if any of the simplified files have a different number of lines than the original file

# Check if simplified text totally matches the original text as statistics
for model in ModelNames:
    if len(original_lines) != len(simplified_lines[model]):
        raise ValueError(
            f"Number of lines in {model.value} does not match the original text which is {len(original_lines)}."
        )

# Check if the simplified text is different from the original text
count_dict = {model.value: 0 for model in ModelNames}

for model in ModelNames:
    pairs = zip(original_lines, simplified_lines[model])
    for _, (original_line, simplified_line) in enumerate(pairs):
        if original_line == simplified_line:
            count_dict[model.value] += 1

df_count = pd.DataFrame(count_dict.items(), columns=["Model", "Matched"])

# Create a list to hold the rows for the DataFrame
data = []

# Pair each line from the original text with each corresponding line from the simplified text files
tmp = 1
model_names = [model for model in ModelNames]
for i, original_line in enumerate(original_lines):
    random.shuffle(model_names) #comment if you don't want to shuffle amongst the models
    for model in model_names:
        data.append(
            {
                "id": tmp,
                "original_text_id": i + 1,
                "adequacy": None,  # Placeholder for Adequacy
                "fluency": None,  # Placeholder for Fluency
                "simplicity": None,  # Placeholder for Simplicity
                "model_id": model.name,
                "original": original_line.strip(),
                "simplified": simplified_lines[model][i].strip(),
            }
        )
        tmp += 1

#random.shuffle(data) #uncomment if you want to shuffle over all sentences

# Create a DataFrame from the data
df = pd.DataFrame(data)
df.to_csv("data_full_supreme.csv", index=False)
#df.to_csv("data_full.csv", index=False)

# %%
our_model = ModelNames.M6  # uslt
to_compare = ModelNames.M2  # lsbert

assert our_model != to_compare
assert our_model.value == "uslt"
assert to_compare.value == "lsbert"

# Select 25 simplifications for our model and 25 for the to_compare model, make sure that they select same simplifications from same original_text_id

our_df = df[(df["model_id"] == our_model.name)].sample(n=25)


cond1 = df["model_id"] == to_compare.name
cond2 = df["original_text_id"].isin(our_df["original_text_id"])
compare_df = df[(cond1 & cond2)]

our_df.sort_values("original_text_id", inplace=True)
compare_df.sort_values("original_text_id", inplace=True)

final = pd.concat([our_df, compare_df])

# shuffle the final dataframe
final = final.sample(frac=1).reset_index(drop=True)

# check that both models have the same original_text_id
tmp1 = final[final["model_id"] == our_model.name]["original_text_id"].sort_values()
tmp2 = final[final["model_id"] == to_compare.name]["original_text_id"].sort_values()
if not all(tmp1.values == tmp2.values):
    raise ValueError("Original text ids are not the same for both models.")
else:
    print("Original text ids are the same for both models.")

final["id"] = [i for i in range(1, 51)]
final.sort_values("id", inplace=True)

# %%
final.to_csv("data.csv", index=False)


# %%
