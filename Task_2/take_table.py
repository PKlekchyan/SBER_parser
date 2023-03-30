"""

1. В файле буду рассматривать 3 закона об областном бюджете на 2023 год и на плановый период 2024 и 2025 годов
2. Выбрал документы Томской, Белгородской и Свердловской области - парсер в корне
3. Документы выгрузил в виде HTML разметки (.txt) для дальнейшего парсинга

"""
from bs4 import BeautifulSoup

class TakeTableFromDoc:

    def __init__(self):
        pass

    def start(self, path):
        print("Parser started working")

        doc = self.open_doc(path)
        print("Открыли документ")

        table = self.parse_table(doc)
        print("Получили все таблицы")

        self.save_table(table)
        print("Сохранили документ")

        print("Success")

    def open_doc(self, path):
        with open(f'{path}', 'r', encoding='utf-8') as f:
            doc = f.read()
        return doc

    def parse_table(self, doc):
        first_h2 = 0
        own_text = "ВЕДОМСТВЕННАЯ СТРУКТУРА РАСХОДОВ ОБЛАСТНОГО БЮДЖЕТА"
        flag = False
        count = 1
        table = ''
        soup = BeautifulSoup(doc, "html.parser")

        for i, v in enumerate(soup):
            new_soap = BeautifulSoup(str(v), "html.parser")
            el = new_soap.find("h2")

            if el and not flag:
                first_h2 = i
            elif el and flag:
                for ind, val in enumerate(soup):
                    if first_h2 <= ind <= i+1:
                        table += str(val)
                print(f'Получили таблицу - {count}')
                count += 1
                first_h2 = i
                flag = False
            item_text = v.get_text()
            if own_text in item_text.upper():
                flag = True

        return table

    def save_table(self, tb):

        markup = "".join(tb)

        with open("./src/Таблицы_Свердловская.html", "w", encoding='utf-8') as f:
            f.write(markup)


if __name__ == "__main__":
    TakeTableFromDoc().start("./src/Бюджеты Свердловской_29-03-2023__01-16.txt")
