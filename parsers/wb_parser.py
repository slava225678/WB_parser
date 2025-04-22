import requests
from typing import Dict, Optional
from urllib.parse import quote

from .base_parser import BaseParser
from config import SEARCH_URL


class WBParser(BaseParser):

    def fetch_data(
        self,
        article: str,
        category: Optional[str] = None
    ) -> Dict[str, str]:
        try:
            query = quote(article)
            response = requests.get(
                SEARCH_URL.format(query=query),
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            products = data.get("data", {}).get("products", [])
            if not products:
                return {}

            product = products[0]
            nm_id = product["id"]
            vol_id = nm_id // 100000
            part_id = nm_id // 1000

            for basket in range(100):  # 0–99
                url = (
                    f"https://basket-{basket}.wbbasket.ru/"
                    f"vol{vol_id}/part{part_id}/{nm_id}/info/ru/card.json"
                )
                try:
                    r = requests.get(url, timeout=15)
                    if r.ok:
                        return self._parse_card_json(r.json(), basket=basket)
                except requests.RequestException:
                    continue

        except Exception as e:
            print(f"[Ошибка] {article}: {e}")
            return {}

        return {}

    def _parse_card_json(self, card: dict, basket: Optional[int] = None) -> Dict[str, str]:
        result = {}

        result["Наименование"] = card.get("imt_name")
        result["Описание"] = card.get("description")
        result["Бренд"] = card.get("vendor_code")
        # result["Фото"] = card.get("media")

        # 🖼️ Генерация ссылок на фото
        if basket is not None and "media" in card and "nm_id" in card:
            nm_id = card["nm_id"]
            vol_id = nm_id // 100000
            part_id = nm_id // 1000
            photo_count = card["media"]["photo_count"]
            photo_links = [
                f"https://basket-{basket}.wbbasket.ru/vol{vol_id}/part{part_id}/{nm_id}/images/big/{i}.webp"
                for i in range(1, photo_count + 1)
            ]
            # Объединяем все ссылки в одну строку, разделяя переносом строки
            result["Фото"] = ";".join(photo_links)

        # Обычные опции
        for option in card.get("options", []):
            name = option.get("name")
            value = option.get("value")
            if name and value:
                result[name] = value

        # Группированные опции
        for group in card.get("grouped_options", []):
            for option in group.get("options", []):
                name = option.get("name")
                value = option.get("value")
                if name and value:
                    result[name] = value

        return result
