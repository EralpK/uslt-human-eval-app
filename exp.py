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

# Create a list to hold the rows for the DataFrame
data = []

# Pair each line from the original text with each corresponding line from the simplified text files
for i, original_line in enumerate(original_lines):
    for model in ModelNames:
        data.append(
            {
                "text_pair_id": f"{i}",
                "Original": original_line.strip(),
                "Simplified": simplified_lines[model][i].strip(),
                "Model": model.name,
                "Adequacy": None,  # Placeholder for Adequacy
                "Fluency": None,  # Placeholder for Fluency
                "Simplicity": None,  # Placeholder for Simplicity
            }
        )

# Create a DataFrame from the data
df = pd.DataFrame(data)

df.to_csv("evaluations.csv")

# %%
