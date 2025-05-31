from pathlib import Path

import pandas as pd
import requests

from parsers.wb_parser import WBParser
from wb_data_filler.utils.excel_handler import read_excel_file
from wb_data_filler.utils.processor import clean_numeric_value

parser = WBParser()

patch_in = "wb_data_filler/data/input/"
patch_out = "wb_data_filler/data/output/"
article = 227412442


def man_load(
    nm_id: int,
    template_path: Path = Path("wb_data_filler/data/input/Ноутбуки.xlsx"),
    output_path: Path = Path(f"{patch_out}manual_result.xlsx")
) -> None:
    '''
    Загружает данные по одному артикулу WB, заполняя шаблон Excel.

    Получает карточку товара с сервера Wildberries и
    подставляет полученные значения
    в шаблон Excel-файла. В числовые поля применяется предварительная очистка.
    Файл сохраняется в указанный путь.

    :param nm_id: Артикул товара Wildberries (числовой идентификатор).
    :param template_path: Путь к Excel-шаблону с ожидаемой структурой колонок.
    :param output_path: Путь, куда сохранить итоговый Excel-файл.
    '''
    df_template, column_names, value_descriptions = read_excel_file(
        template_path
    )
    result_df = pd.DataFrame(columns=column_names)
    result_df.loc[0] = [""] * len(column_names)
    numeric_fields = {
            name for name, desc in zip(column_names, value_descriptions)
            if isinstance(desc, str) and "Единица измерения" in desc
        }
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
                    print(
                        f"⚠️ Не удалось распарсить"
                        f"данные для артикула: {nm_id}"
                    )
                    return
                for i, column in enumerate(column_names):
                    value = parsed_data.get(column)
                    if value:
                        if column in numeric_fields:
                            value = clean_numeric_value(value)
                        result_df.at[0, column] = value

                result_df.at[0, "Артикул WB"] = str(nm_id)
                result_df.to_excel(output_path, index=False)
                print(f"✅ Данные сохранены в: {output_path.name}")
                return
        except requests.RequestException:
            continue
    print(f"❌ Не удалось найти данные по артикулу: {nm_id}")


man_load(article, output_path=Path(f"{patch_out}{article}_manual.xlsx"))
