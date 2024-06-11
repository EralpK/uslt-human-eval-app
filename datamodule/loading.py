from pathlib import Path

from datamodule.configs import ModelNames

for model in ModelNames:
    file_path = Path(f"../data/{model.value}.txt")
    # read the file
    with open(file_path) as f:
        print(f.read())
