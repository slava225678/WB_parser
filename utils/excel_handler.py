from pathlib import Path
from typing import List, Tuple

import pandas as pd


def read_excel_file(
        file_path: Path
) -> Tuple[pd.DataFrame, List[str], List[str]]:
    '''
    Читает Excel-файл с шаблонной структурой и
    возвращает данные, заголовки и описания.

    Ожидается формат файла:
    - 3-я строка (index=2): заголовки столбцов;
    - 4-я строка (index=3): описания столбцов (например, единицы измерения);
    - с 5-й строки (index=4): данные.

    :param file_path: Путь к Excel-файлу с шаблоном.
    :return: Кортеж:
        - DataFrame с данными (без заголовков),
        - список названий колонок,
        - список описаний колонок.
    '''
    df = pd.read_excel(file_path, header=None)
    column_names = df.iloc[2].tolist()
    value_descriptions = df.iloc[3].tolist()
    df.columns = column_names
    data_df = df.iloc[4:].reset_index(drop=True)
    return data_df, column_names, value_descriptions


def write_to_excel(
        df: pd.DataFrame,
        original_path: Path,
        output_dir: Path
) -> None:
    '''
    Сохраняет переданный DataFrame в Excel-файл
    с добавкой '_filled' к исходному имени.

    :param df: DataFrame с результатами для сохранения.
    :param original_path: Исходный путь к шаблонному файлу (для имени).
    :param output_dir: Каталог для сохранения итогового файла.
    '''
    output_path = output_dir / f"{original_path.stem}_filled.xlsx"
    df.to_excel(output_path, index=False)
