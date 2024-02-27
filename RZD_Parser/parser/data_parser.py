import re

from typing import TypeVar, List, Dict

Row = TypeVar('Row', bound=Dict[str, float])


class DataParser:
    general_pattern = r'(\w+[\s\w]*?)\s–\s([\d,\.]+)\s(млн|тыс)\sтонн'
    pogruzka_pattern = r"погрузка на сети.*составила\s(\d+,\d+)\sмлн тонн"
    break_pattern = r"погрузка на сети.*году.*составила\s(\d+,\d+)\sмлн тонн"
    gruzooborot_pattern = r"грузооборот.*составил\s(\d+,\d+)\sмлрд тарифных тонно-км"

    def parse_values(self, page_text: str) -> Row:
        result = dict()
        page_text = page_text.lower()

        if re.findall(self.break_pattern, page_text):
            # Годовые данные, скипаем такие
            return dict()

        if pogruzka_matches := re.findall(self.pogruzka_pattern, page_text):
            # print(pogruzka_matches)
            result["Погрузка на сети млн тонн"] = self.__extract_value(pogruzka_matches[0])

        if gruzooborot_matches := re.findall(self.gruzooborot_pattern, page_text):
            result["Грузооборот млрд тарифных тонно-км"] = self.__extract_value(gruzooborot_matches[0])

        matches = re.findall(self.general_pattern, page_text)
        for match in matches:
            key = f'{match[0]} {match[2]} тонн'
            value = self.__extract_value(match[1])
            result[key] = value

        return result

    @staticmethod
    def __extract_value(value: str) -> float:
        return float(value.replace(',', '.'))
