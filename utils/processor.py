import re
from pathlib import Path

from tqdm import tqdm

from config import IGNORED_COLUMNS, MANUAL_NUMERIC_FIELDS, REQUIRED_FIELDS
from parsers.wb_parser import WBParser
from wb_data_filler.utils.excel_handler import read_excel_file, write_to_excel


def clean_numeric_value(value: str) -> str:
    '''
    Преобразует строку с числом и единицами измерения в
    округлённое целое число в виде строки.

    Извлекает первое числовое значение из строки, заменяет
    запятую на точку (если есть),
    округляет его до ближайшего целого и возвращает как строку.
    Если число не найдено — возвращает оригинальное значение без изменений.

    Примеры:
        "1.4 кг" → "1"
        "23 см" → "23"
        "1000,5 мл" → "1000"

    :param value: Строка, содержащая числовое значение с текстом.
    :return: Строка с округлённым числом или оригинальное значение.
    '''
    if not isinstance(value, str):
        return value

    match = re.search(r"(\d+(\.\d+)?)", value.replace(",", "."))
    if match:
        num = float(match.group(1))
        return str(int(round(num)))
    return value


def process_all_files(input_dir: Path, output_dir: Path):
    '''
    Обрабатывает все Excel-файлы в указанной директории:
    заполняет шаблоны данными с Wildberries.

    Для каждого .xlsx файла:
    - определяет категорию по имени файла;
    - считывает структуру таблицы и описания полей;
    - определяет числовые поля;
    - по каждому артикулу ищет данные на Wildberries;
    - заполняет соответствующие поля в таблице;
    - сохраняет результат в файл в output-директории с суффиксом `_filled`.

    :param input_dir: Путь к папке с входными Excel-файлами шаблонов.
    :param output_dir: Путь к папке, куда сохраняются заполненные таблицы.
    '''
    parser = WBParser()
    input_files = list(input_dir.glob("*.xlsx"))

    for file_path in input_files:
        print(f"🔍 Обработка файла: {file_path.name}")
        category = file_path.stem
        df, column_names, value_descriptions = read_excel_file(file_path)
        result_df = df.copy()

        numeric_fields = {
            name for name, desc in zip(column_names, value_descriptions)
            if isinstance(desc, str) and "Единица измерения" in desc
        }
        numeric_fields.update(MANUAL_NUMERIC_FIELDS)

        for idx, row in tqdm(
            df.iterrows(),
            total=len(df),
            desc="Поиск данных"
        ):
            article = row.get("Артикул продавца")
            if not article or not isinstance(article, str):
                continue

            data = parser.fetch_data(article, category=category)
            for key, value in data.items():
                if key in IGNORED_COLUMNS:
                    continue
                if key in REQUIRED_FIELDS:
                    result_df.at[idx, REQUIRED_FIELDS[key]] = value
                elif key in numeric_fields:
                    result_df.at[idx, key] = int(clean_numeric_value(value))
                else:
                    result_df.at[idx, key] = value

        write_to_excel(result_df, file_path, output_dir)
        print(f"✅ Сохранён: {file_path.stem}_filled.xlsx\n")
