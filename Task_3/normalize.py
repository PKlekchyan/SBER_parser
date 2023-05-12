import pandas as pd

class NormalizeTable:

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

    def start(self, df, data):
        self.type_of_tb, self.type_of_bg, self.NAMES_ID, self.CSR, self.VR, self.ID_2023, self.ID_2024, self.ID_2025 = data
        if self.type_of_tb:
            df = self.merge_tb(df)
            final_own = self.create_df(df)
        else:
            df = self.concat_tb(df)
            final_own = self.create_df(df)

        final_own['ЦСР'] = final_own['ЦСР'].apply(lambda x: self.delete_abrakadabra(x))
        final_own.drop([0, 1], inplace=True)
        final_own.reset_index(drop=True, inplace=True)
        return final_own

    def merge_tb(self, df):
        final_own_1 = pd.DataFrame()
        final_own_2 = pd.DataFrame()

        for i in df:

            i = i.drop(0)
            if not len(final_own_1.columns) or len(i.columns) == self.ID_2023 + 1:
                final_own_1 = pd.concat([final_own_1, i.iloc[:, [i for i in range(self.ID_2023 + 1)]].astype(str)])
            else:
                final_own_2 = pd.concat([final_own_2, i.iloc[:, [i for i in range(self.ID_2025 + 1)]].astype(str)])

        final_own_1.columns = [str(i) for i in range(self.ID_2023 + 1)]
        final_own_2.columns = [*[str(i) for i in range(self.ID_2023)], '2024', '2025']

        return final_own_1.merge(final_own_2, on=[str(i) for i in range(self.ID_2023)], how='left')

    def concat_tb(self, df_arr):

        mdl_df = pd.DataFrame()

        for i in df_arr:
            mdl_df = pd.concat([mdl_df, i.astype(str)])

        return mdl_df

    def create_df(self, mdw_df):
        final_own = pd.DataFrame()

        final_own["Наименование"] = mdw_df.iloc[:, [self.NAMES_ID]]
        final_own['ЦСР'] = mdw_df.iloc[:, self.CSR[0]].astype(str).agg(''.join, axis=1)
        final_own["ВР"] = mdw_df.iloc[:, [self.VR]]
        final_own["2023"] = mdw_df.iloc[:, [self.ID_2023]]
        final_own["2024"] = mdw_df.iloc[:, [self.ID_2024]]
        final_own["2025"] = mdw_df.iloc[:, [self.ID_2025]]

        return final_own

    def delete_abrakadabra(self, x):
        try:
            x = x.strip()
            arr = []
            for i in x:
                if i.isdigit():
                    arr.append(i)
            x = "".join(arr)
            return x
        except:
            return ""