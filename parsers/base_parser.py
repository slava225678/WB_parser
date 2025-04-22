from abc import ABC, abstractmethod
from typing import Dict, Optional


class BaseParser(ABC):
    @abstractmethod
    def fetch_data(
        self, article:
        str, category:
        Optional[str] = None
    ) -> Dict[str, str]:
        """
        По артикулу получает данные с сайта.
        Возвращает словарь с ключами — названиями столбцов
        """
        pass
