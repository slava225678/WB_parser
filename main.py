from pathlib import Path
from processor import process_all_files


if __name__ == "__main__":
    input_dir = Path("wb_data_filler/data/input/")
    output_dir = Path("wb_data_filler/data/output/")
    output_dir.mkdir(parents=True, exist_ok=True)

    process_all_files(input_dir, output_dir)
