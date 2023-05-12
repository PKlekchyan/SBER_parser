import pandas as pd
import re


class UploadTableFromFile:

    def __init__(self):
        # ТИП ТАБЛИЦЫ
        self.type_of_tb = 0  # 0 - тип где все года в одной таблице, 1 - тип где года в разных таблицах
        # Какая размерность у столбца бюджетов
        self.type_of_bg = 0  # 0 - тип где столбец описан в руб. 1 - мера столбца в тыс. руб
        # Задаем константы для ИД таблицы
        self.NAMES_ID = 0
        self.CSR = []
        self.VR = 0
        self.ID_2023 = 0
        self.ID_2024 = 0
        self.ID_2025 = 0

    def start(self, path):
        df = pd.read_html(path, encoding="UTF-8")
        indexes = self.search_title(df)
        filter_indexes = self.search_vr(df, indexes)
        true_arr = self.true_ind_arr(filter_indexes)
        self.get_index(true_arr, df)
        clean_df = self.clean_tb(filter_indexes, df)
        return clean_df, [self.type_of_tb, self.type_of_bg, self.NAMES_ID, self.CSR, self.VR, self.ID_2023, self.ID_2024,
                self.ID_2025]

    def valid_func(self, x):
        try:
            return int(x)
        except:
            return x

    def search_title(self, df2):
        # Определяем в каких таблицах есть заголовки
        title_index = []

        for ind, i in enumerate(df2):

            for j, k in i.iloc[0:1].iterrows():
                new_arr = k.apply(lambda x: str(type(self.valid_func(x))))
                new_arr = set(new_arr)

                if len(new_arr) == 1:
                    title_index.append(ind)

        return title_index

    def search_vr(self, df2, title_index):
        # Определяем в каких таблицах есть вид расходов
        # Если таблица с нужным заголовком не последняя, то получаем индекс следующей
        # за ней таблицей с заголовком и записываем его в переменную. Это для того, чтобы почистить хвост листа (возьмем данные от [need_title: bad_title])
        # До нужной таблицы с заголовком так же не берем

        pattern = r'ВИД\w* РАСХОД\w*'
        filter_title_index = []

        for m in title_index:
            filter_title_index.append({m: False})

            for i, k in df2[m].iloc[:3].iterrows():
                for j in range(len(k)):
                    if re.findall(r'ВР', str(k[j]).upper()) or re.findall(pattern, str(k[j]).upper()):
                        del filter_title_index[-1]
                        filter_title_index.append({m: True})

                        # Проверяем исключение таблиц, когда есть профицит или дефицит бюджета (минус не ищем, т.к. может использоваться как перенос)
                        for y, z in df2[m].iloc[:20].iterrows():
                            l = [z[i] for i in range(len(z))]
                            for d in l:
                                if "+" in str(d):
                                    del filter_title_index[-1]
                                    filter_title_index.append({m: False})

        return filter_title_index

    def true_ind_arr(self, arr):
        true_arr = []

        for i in arr:
            for x, y in i.items():
                if y:
                    true_arr.append(x)

        # Check type of table and set result
        if len(true_arr) > 1:
            self.type_of_tb = 1
        else:
            self.type_of_tb = 0

        return true_arr

    def get_index(self, tb, df2):
        pattern_csr = r'ЦЕЛЕВ\w* СТАТЬ\w*'
        pattern_vr = r'ВИД\w* РАСХОД\w*'

        for m in tb:
            prog = []

            for i, k in df2[m].iloc[:3].iterrows():
                for j in range(len(k)):

                    if re.findall(r'НАИМЕНОВАНИЕ', str(k[j]).upper()):
                        self.NAMES_ID = j

                    if re.findall(r'ЦСР', str(k[j]).upper()) or re.findall(pattern_csr, str(k[j]).upper()):
                        prog = [*prog, j]

                    if re.findall(r"\b[К]?ВР\b", str(k[j]).upper()) or re.findall(pattern_vr, str(k[j]).upper()):
                        self.VR = j

                    if k[j] == "2023" or re.findall(r'2023', str(k[j]).upper()) or re.findall(r'СУММА', str(
                            k[j]).upper()) or re.findall(r'ИТОГО', str(k[j]).upper()):
                        if self.ID_2023 == 0:
                            self.ID_2023 = j

                    if re.findall(r"ТЫС\w* РУБ\w*", str(k[j]).upper()):
                        self.type_of_bg = 1

                    if k[j] == "2024" or re.findall(r'2024', str(k[j]).upper()):
                        self.ID_2024 = j

                    if k[j] == "2025" or re.findall(r'2025', str(k[j]).upper()):
                        self.ID_2025 = j

            self.CSR.append(prog)

    def clean_tb(self, filter_title_index, df2):
        normalize_dfs = []

        for i, k in enumerate(filter_title_index):
            for j, q_bool in k.items():
                if q_bool:
                    if len(filter_title_index) == i + 1:
                        normalize_dfs.extend(df2[j:])
                    else:
                        for f, b_bool in filter_title_index[i + 1].items():
                            normalize_dfs.extend(df2[j:f])

        return self.delete_bad_rows(normalize_dfs)


    def delete_bad_rows(self, tb):
        for m in tb:
            for i, k in m.iterrows():
                row_arr = [k[j] for j in range(len(k))]
                uniq_test = set(row_arr)
                if len(uniq_test) == 1:
                    m.drop(i, inplace=True)

        return tb