IGNORED_COLUMNS = [
    'Группа', 'Артикул WB', 'Категория продавца', 'КИЗ', 'Баркоды', 'Цена',
    'Ставка НДС', 'Дата окончания действия сертификата/декларации',
    'Дата регистрации сертификата/декларации', 'Номер декларации соответствия',
    'Номер сертификата соответствия', 'ИКПУ', 'Код упаковки'
]
SEARCH_URL = (
    'https://search.wb.ru/exactmatch/ru/common/v7/search?'
    'ab_testing=false&appType=1&curr=rub&dest=-1257786&'
    'query={query}&resultset=catalog&sort=popular&'
    'spp=30&suppressSpellcheck=true&uclusters=0'
)
REQUIRED_FIELDS = {
    'description': 'Описание',
    'imt_name': 'Наименование',
    'vendor_code': 'Бренд',
    'Диагональ экрана (дюйм)': 'Диагональ экрана',
}
MANUAL_NUMERIC_FIELDS = {
    'Объем оперативной памяти (Гб)',
    'Количество слотов оперативной памяти',
    'Порт USB-C',
    'Порт USB 2.0',
    'Порт USB 3.x',
    'Порт USB 4.x',
    'Разъем HDMI',
    'LAN разъем (RJ45)'
}
