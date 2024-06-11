# %%
from pathlib import Path

import pandas as pd

from datamodule.configs import ModelNames

# Directory paths
base_dir = Path.cwd().joinpath("data/test")
original_file_path = base_dir / "original_text.txt"
simplified_dir = base_dir / "simplified"

# Read the original text file
with original_file_path.open("r") as file:
    original_lines = file.readlines()

# Initialize a dictionary to hold simplified lines
simplified_lines = {model: [] for model in ModelNames}

# Read each simplified text file
for model in ModelNames:
    simplified_file_path = simplified_dir / f"{model.value}.txt"
    with simplified_file_path.open("r") as file:
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
for i, original_line in enumerate(original_lines):
    for model in ModelNames:
        data.append(
            {
                "text_pair_id": tmp,
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


# Create a DataFrame from the data
df = pd.DataFrame(data)
df.to_csv("evalcsv/full/evaluations.csv", index=False)

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
final.sort_values("original_text_id", inplace=True)

final["text_pair_id"] = [i for i in range(1, 51)]
final.to_csv("evalcsv/aykut/evaluations.csv", index=False)


# %%
