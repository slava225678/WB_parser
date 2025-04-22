import pandas as pd
from pathlib import Path
from typing import List, Tuple


def read_excel_file(
        file_path: Path
) -> Tuple[pd.DataFrame, List[str]]:
    df = pd.read_excel(file_path, header=None)
    column_names = df.iloc[2].tolist()  # строка 3 — заголовки
    df.columns = column_names
    data_df = df.iloc[4:].reset_index(drop=True)  # строки с данными
    return data_df, column_names


def write_to_excel(
        df: pd.DataFrame,
        original_path: Path,
        output_dir: Path
) -> None:
    output_path = output_dir / f"{original_path.stem}_filled.xlsx"
    df.to_excel(output_path, index=False)
