# 🏩 Wildberries Data Filler

Автоматический парсер и обработчик Excel-файлов с артикулами товаров продавца на [Wildberries.ru](https://www.wildberries.ru/). Скрипт извлекает характеристики товаров и дополняет ими шаблонные таблицы. Поддерживается как **пакетная обработка файлов**, так и **ручной ввод артикула**.

## 🔧 Функциональность

* 🔎 Получение данных по артикулу через API Wildberries
* 📄 Обработка Excel-шаблонов и заполнение недостающих характеристик
* 🩼 Очистка числовых значений от текста
* 🔄 Обработка всех файлов из папки input
* 📝 Ручной режим обработки одного артикула
* 🛠️ Поддержка полей, требующих очистки

## 📁 Структура проекта

```
wb_data_filler/
│
├── data/                    # Папка с входными и выходными Excel-файлами
│   ├── input/               # Входные файлы (.xlsx) для обработки
│   └── output/              # Сюда сохраняются обработанные файлы
│
├── parsers/                 # Модуль парсинга
│   ├── __init__.py         
│   ├── base_parser.py       # Базовый класс парсера
│   └── wb_parser.py         # Парсер карточек Wildberries
│
├── utils/                   # Утилиты и вспомогательные модули
│   ├── excel_handler.py     # Работа с Excel-файлами
│   ├── manual_loading_WB.py # Ручная загрузка данных (опционально)
│   └── processor.py         # Основной процесс обработки файлов
│
├── main.py                  # Точка входа в программу
├── config.py                # Конфигурационные переменные
├── requirements.txt         # Зависимости проекта
├── LICENSE                 
├── .gitignore              
└── README.md                # Документация проекта
```

## 🚀 Запуск

### 1. Установка

```bash
git clone https://github.com/slava225678/wb_data_filler.git
cd wb_data_filler
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Обработка файлов

```bash
python main.py
```

### 3. Ручной запуск

```bash
python manual.py
```

## 🩼 Очистка чисел

```python
def clean_numeric_value(value: str) -> str:
    """
    "1.4 кг" → "1"
    "23 см" → "23"
    """
```

## 🔍 API WB

* Поиск: `https://search.wb.ru/exactmatch/...`
* Детали товара: `https://basket-{n}.wbbasket.ru/.../card.json`

## 📆 requirements.txt

```txt
pandas
openpyxl
requests
tqdm
```

## 👨‍💻 Автор

[GitHub](https://github.com/slava225678)

---

🌟 Проект готов для использования и расширения!
