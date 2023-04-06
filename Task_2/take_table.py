"""

1. В файле буду рассматривать 3 закона об областном бюджете на 2023 год и на плановый период 2024 и 2025 годов
2. Выбрал документы Томской, Белгородской и Свердловской области - парсер в корне
3. Документы выгрузил в виде HTML разметки (.html) для дальнейшего парсинга

"""
from bs4 import BeautifulSoup
import re


class TakeTableFromDoc:

    def __init__(self):
        self.rub = ''

    def start(self, path: str, reg: int):
        name = path.split("__")[1].replace(".html", "")

        print("", "", "Parser started working", sep="\n")

        doc = self.open_doc(path)
        print("Открыли документ")

        try:
            table = self.parse_table(doc, 1)
            if not table:
                raise ValueError
        except:
            table = self.parse_table(doc, 0)
            if table:
                print("Получили все совпадения")
            else:
                print("Совпадений нет")
                raise ValueError

        nl_tb = self.normalize_tb(table)
        print("Нормализовали таблицы")

        self.save_table(nl_tb, name, reg)
        print("Сохранили документ")

        print("Success")

    def open_doc(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            doc = f.read()
        return doc

    def parse_table(self, doc, tag):
        first_h2 = 0
        tag = "h2" if tag else "h3"  # Передаем bool - 1(h2), 0(h3)

        # pattern = r'ВЕДОМСТВЕН\w* СТРУКТУР\w* РАСХОД\w* ОБЛАСТН\w* БЮДЖЕТ\w*'
        pattern = r'ВЕДОМСТВЕН\w* СТРУКТУР\w*'

        flag = False
        count = 1
        table = ''
        soup = BeautifulSoup(doc, "html.parser")

        for i, v in enumerate(soup):
            new_soap = BeautifulSoup(str(v), "html.parser")
            el = new_soap.find(tag)

            if el and not flag:
                first_h2 = i
            elif el and flag:
                for ind, val in enumerate(soup):
                    if first_h2 <= ind < i:
                        table += str(val)
                print(f'Получили совпадение - {count}')
                count += 1
                first_h2 = i
                flag = False
            item_text = v.get_text().upper()

            if re.findall(pattern, item_text):
                flag = True

        return table

    def delete_bad_tr(self, table):
        table.select_one('tr[height = "1"]').decompose()
        self.ident_rub(table)
        return table

    def normalize_tb(self, tb):
        soup = BeautifulSoup(tb, "html.parser")
        only_tb = soup.find_all('div', class_='table-container')
        str_tb = [str(self.delete_bad_tr(i)) for i in only_tb]
        return str_tb

    def ident_rub(self, table):
        own_t = table.get_text().lower()
        if "тыс. рубл" in own_t and not self.rub:
            self.rub = "тыс_рублей"
        elif "тысяч рубл" in own_t and not self.rub:
            self.rub = "тыс_рублей"
        elif "рубл" in own_t and not self.rub:
            self.rub = "рублей"

    def save_table(self, tb, name, reg):
        markup = "".join(tb)
        with open(f'./src/tables/{reg}_Таблицы__{name}__{self.rub}.html', "w", encoding='utf-8') as f:
            f.write(markup)
