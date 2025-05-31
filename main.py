from pathlib import Path

from wb_data_filler.utils.processor import process_all_files

if __name__ == "__main__":
    '''
    Скрипт запускает массовую обработку Excel-файлов с артикулами товаров.

    Считывает шаблоны из директории `data/input`,
    запрашивает данные с Wildberries по артикулу,
    заполняет таблицы и сохраняет результат в `data/output`.
    '''
    input_dir = Path("wb_data_filler/data/input/")
    output_dir = Path("wb_data_filler/data/output/")
    output_dir.mkdir(parents=True, exist_ok=True)

    process_all_files(input_dir, output_dir)
