from pathlib import Path
from parsers.wb_parser import WBParser
from excel_handler import read_excel_file, write_to_excel
from tqdm import tqdm
from config import IGNORED_COLUMNS


def process_all_files(input_dir: Path, output_dir: Path):
    parser = WBParser()
    input_files = list(input_dir.glob("*.xlsx"))

    for file_path in input_files:
        print(f"🔍 Обработка файла: {file_path.name}")
        category = file_path.stem
        df, column_names = read_excel_file(file_path)
        result_df = df.copy()

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
                if key == "description":
                    result_df.at[idx, "Описание"] = value
                elif key == "imt_name":
                    result_df.at[idx, "Наименование"] = value
                elif key == "vendor_code":
                    result_df.at[idx, "Бренд"] = value
                else:
                    result_df.at[idx, key] = value

        write_to_excel(result_df, file_path, output_dir)
        print(f"✅ Сохранён: {file_path.stem}_filled.xlsx\n")
