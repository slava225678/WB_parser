from pathlib import Path
from typing import List, Tuple
import pandas as pd
import requests
from parsers.wb_parser import WBParser

parser = WBParser()

patch_in = "wb_data_filler/data/input/"
patch_out = "wb_data_filler/data/output/"
article = 350730026


def read_excel_file(
        file_path: Path
) -> Tuple[pd.DataFrame, List[str]]:
    df = pd.read_excel(file_path, header=None)
    column_names = df.iloc[2].tolist()  # строка 3 — заголовки
    df.columns = column_names
    data_df = df.iloc[4:].reset_index(drop=True)  # строки с данными
    return data_df, column_names


def man_load(
    nm_id: int,
    template_path: Path = Path("wb_data_filler/data/input/Ноутбуки.xlsx"),
    output_path: Path = Path(f"{patch_out}manual_result.xlsx")
) -> None:
    # Получаем структуру из шаблонного файла
    df_template, column_names = read_excel_file(template_path)
    # Оставим только одну строку (пустую) для заполнения
    result_df = pd.DataFrame(columns=column_names)
    result_df.loc[0] = [""] * len(column_names)
    # Поиск карточки товара
    vol_id = nm_id // 100000
    part_id = nm_id // 1000

    for basket in range(100):
        url = (
            f"https://basket-{basket}.wbbasket.ru/"
            f"vol{vol_id}/part{part_id}/{nm_id}/info/ru/card.json"
        )
        try:
            r = requests.get(url, timeout=15)
            if r.ok:
                parsed_data = parser._parse_card_json(r.json(), basket=basket)
                if not parsed_data:
                    print(f"⚠️ Не удалось распарсить данные для артикула: {nm_id}")
                    return

                # Заполняем результат в соответствии с колонками
                for column in column_names:
                    if column in parsed_data:
                        result_df.at[0, column] = parsed_data[column]
                result_df.at[0, "Артикул WB"] = str(nm_id)

                result_df.to_excel(output_path, index=False)
                print(f"✅ Данные сохранены в: {output_path.name}")
                return
        except requests.RequestException:
            continue
    print(f"❌ Не удалось найти данные по артикулу: {nm_id}")


man_load(article, output_path=Path(f"{patch_out}{article}_manual.xlsx"))
