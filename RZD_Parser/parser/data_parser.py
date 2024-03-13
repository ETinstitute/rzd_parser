import datetime
import re

from typing import TypeVar, Dict

import pandas as pd

Row = TypeVar('Row', bound=Dict[str, float])


class DataParser:
    general_pattern_mln = r'(\w+[\s\w]*?)\s–\s([\d,\.]+)\sмлн\sтонн'
    general_pattern_tis = r'(\w+[\s\w]*?)\s–\s([\d,\.]+)\sтыс.\sтонн'

    # break_pattern = r"в.*году.*составила"

    pogruzka_pattern = r"погрузка на сети.*составила\s(\d+,\d+)\sмлн тонн"
    pogruzka_pattern1 = r"погрузка на сети.*составила\s(\d+)\sмлн тонн"

    gruzooborot_pattern = r'грузооборот за (?:январь|февраль|март|апрель|май|июнь|июль|август|сентябрь|октябрь|ноябрь|декабрь)[\S\s]*?составил\s(\d{1,3}(?:,\d{1,3})*[.,]?\d+)\sмлрд тарифных тонно-км'
    gruzooborot_pattern1 = r'грузооборот в (?:январе|феврале|марте|апреле|мае|июне|июле|августе|сентябре|октябре|ноябре|декабре)[\S\s]*?составил\s(\d{1,3}(?:,\d{1,3})*[.,]?\d+)\sмлрд тарифных тонно-км'

    def parse_values(self, page_text: str) -> Row:
        page_text = self.__text_preprocess(page_text)
        result = dict()

        # result['Годовые данные'] = True if re.findall(self.break_pattern, page_text) else False

        if matches := re.findall(self.pogruzka_pattern, page_text):
            result["Погрузка на сети млн тонн"] = self.__extract_value(matches[0])

        if matches := re.findall(self.pogruzka_pattern1, page_text):
            # тоже самое, но число целое, не разделено запятой
            result["Погрузка на сети млн тонн"] = self.__extract_value(matches[0])

        if matches := re.findall(self.gruzooborot_pattern, page_text):
            result["Грузооборот млрд тарифных тонно-км"] = self.__extract_value(matches[0])

        if matches := re.findall(self.gruzooborot_pattern1, page_text):
            # тоже самое, но не "за апрель" а "в апреле"
            result["Грузооборот млрд тарифных тонно-км"] = self.__extract_value(matches[0])

        matches = re.findall(self.general_pattern_mln, page_text)
        result = result | {f'{match[0]} накоп. млн тонн': self.__extract_value(match[1]) for match in matches}

        matches = re.findall(self.general_pattern_tis, page_text)
        result = result | {f'{match[0]} накоп. млн тонн': self.__extract_value(match[1]) / 1000 for match in matches}

        return result

    @staticmethod
    def parse_date(text):
        date = pd.to_datetime(text, dayfirst=True) - pd.offsets.MonthEnd(1)
        year, month, day = str(date).split()[0].split('-')
        return f'{day}.{month}.{year}'

    @staticmethod
    def __extract_value(value: str) -> float:
        return float(value.replace(',', '.'))

    @staticmethod
    def __text_preprocess(text: str) -> str:
        # контейнеры
        text = text.lower()
        text = text.replace('в том числе в контейнерах', 'в том числе грузов в контейнерах')
        text = text.replace('зерна и продуктов перемола', 'зерна')

        return text
