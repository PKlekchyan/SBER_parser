import json
import pandas as pd
import glob
from os import listdir
from os.path import isfile, join
import re
import os
import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import datetime as dt
from bs4 import BeautifulSoup


class TakeMeraDocs:
    def __init__(self):
        self.doc_id = None
        self.type_docs = "Субсидия"
        self.cookies = {
            '_ym_uid': '1676562523269007969',
            '_ym_d': '1676562523',
            'auth_strategy': 'sso',
            'auth_sso_session': 'SSO_927dacf7-9bde-4367-bdbc-0b14a97d7136_kSaQJ6Fyk1DTyMaw8YHiDHvjzaFqbD9Q_19677e70492ccb5d7c8698c3894ec990ac5a8dd6c963eecf7917dba89b321f3e',
            'auth_sso-channel': 'ee37267fddf347815f8f5aca9c5c5956c947826c',
            '_gid': 'GA1.2.73893347.1680022641',
            '_ym_isad': '1',
            'cas1_session': 'eyJpdiI6InNyZmhIU3BqREZyMFlndlJZSk12Z0E9PSIsInZhbHVlIjoiSDhCZ1lqR3dMVTZsbXY4ZjFTRjZ4VlM1L1JRVGxQRUMxaHNJdUlPc1llWlBzLzIraGJFT2xadGJSZVZsR3UrTThrcnVOTUNjVCsyTElDdnVFL21lc0pyMHlIWmIyUWprcWx5L2ZJME16UFNVSkxsRlJjakJobThsODg4V1NOdkMiLCJtYWMiOiI2YzU0MzQxYTJmNjYwN2M0ODQwNjJjMzFkYmI1ODBjOWNhNGI2NTMxNTA1YjBmYTZjZTM5NjE5YzlmMWY2YmUxIn0%3D',
            '_ym_visorc': 'b',
            'blockInfo': '{"406380321":{"version":3165,"heights":{"1":6054,"2":6104,"3":9370,"4":9228,"5":11461,"6":15552,"7":16058,"8":17950,"9":15816,"10":15816,"11":20876,"12":16806,"13":14958,"14":16762,"15":15684,"16":15046,"17":13726,"18":12516,"19":16696,"20":15354,"21":18302,"22":19952,"23":18324,"24":15618,"25":15420,"26":21271,"27":16450,"28":9252,"29":15653,"30":13794,"31":15486,"32":14939,"33":14712,"34":17584,"35":16542,"36":16905,"37":17717,"38":20566,"39":15764,"40":12285,"41":27784,"42":24043,"43":16938,"44":18258,"45":14842,"46":11772,"47":18786,"48":16072,"49":20986,"50":15725,"51":10646,"52":11863,"53":6419,"54":3994,"55":3379,"56":3192,"57":3582,"58":4198,"59":4039,"60":3600,"61":3526,"62":4085,"63":3642,"64":5302,"65":3721,"66":7253,"67":8529,"68":5793,"69":4163,"70":4611,"71":5343,"72":4086,"73":5532}}}',
            '_ga_20CEJ8PF8Y': 'GS1.1.1680022640.1.1.1680029478.0.0.0',
            '_ga': 'GA1.2.2078692182.1676562523',
            '_gat': '1',
        }
        self.headers = {
            'authority': 'docs.cntd.ru',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            # 'cookie': '_ym_uid=1676562523269007969; _ym_d=1676562523; auth_strategy=sso; auth_sso_session=SSO_927dacf7-9bde-4367-bdbc-0b14a97d7136_kSaQJ6Fyk1DTyMaw8YHiDHvjzaFqbD9Q_19677e70492ccb5d7c8698c3894ec990ac5a8dd6c963eecf7917dba89b321f3e; auth_sso-channel=ee37267fddf347815f8f5aca9c5c5956c947826c; _gid=GA1.2.73893347.1680022641; _ym_isad=1; cas1_session=eyJpdiI6InNyZmhIU3BqREZyMFlndlJZSk12Z0E9PSIsInZhbHVlIjoiSDhCZ1lqR3dMVTZsbXY4ZjFTRjZ4VlM1L1JRVGxQRUMxaHNJdUlPc1llWlBzLzIraGJFT2xadGJSZVZsR3UrTThrcnVOTUNjVCsyTElDdnVFL21lc0pyMHlIWmIyUWprcWx5L2ZJME16UFNVSkxsRlJjakJobThsODg4V1NOdkMiLCJtYWMiOiI2YzU0MzQxYTJmNjYwN2M0ODQwNjJjMzFkYmI1ODBjOWNhNGI2NTMxNTA1YjBmYTZjZTM5NjE5YzlmMWY2YmUxIn0%3D; _ym_visorc=b; blockInfo={"406380321":{"version":3165,"heights":{"1":6054,"2":6104,"3":9370,"4":9228,"5":11461,"6":15552,"7":16058,"8":17950,"9":15816,"10":15816,"11":20876,"12":16806,"13":14958,"14":16762,"15":15684,"16":15046,"17":13726,"18":12516,"19":16696,"20":15354,"21":18302,"22":19952,"23":18324,"24":15618,"25":15420,"26":21271,"27":16450,"28":9252,"29":15653,"30":13794,"31":15486,"32":14939,"33":14712,"34":17584,"35":16542,"36":16905,"37":17717,"38":20566,"39":15764,"40":12285,"41":27784,"42":24043,"43":16938,"44":18258,"45":14842,"46":11772,"47":18786,"48":16072,"49":20986,"50":15725,"51":10646,"52":11863,"53":6419,"54":3994,"55":3379,"56":3192,"57":3582,"58":4198,"59":4039,"60":3600,"61":3526,"62":4085,"63":3642,"64":5302,"65":3721,"66":7253,"67":8529,"68":5793,"69":4163,"70":4611,"71":5343,"72":4086,"73":5532}}}; _ga_20CEJ8PF8Y=GS1.1.1680022640.1.1.1680029478.0.0.0; _ga=GA1.2.2078692182.1676562523; _gat=1',
            'if-none-match': '"17470-fIXdZ67yKRQTjDyudgo0GnjfeBs"',
            'referer': 'https://docs.cntd.ru/search?q=%D0%B7%D0%B0%D0%BA%D0%BE%D0%BD%20%D0%A1%D0%B2%D0%B5%D1%80%D0%B4%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B9%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D0%B8%20%C2%AB%D0%9E%D0%B1%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D0%BD%D0%BE%D0%BC%20%D0%B1%D1%8E%D0%B4%D0%B6%D0%B5%D1%82%D0%B5%20%D0%BD%D0%B0%202023%20%D0%B3%D0%BE%D0%B4%20%D0%B8%20%D0%BF%D0%BB%D0%B0%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%BF%D0%B5%D1%80%D0%B8%D0%BE%D0%B4%202024%20%D0%B8%202025%20%D0%B3%D0%BE%D0%B4%D0%BE%D0%B2%C2%BB',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }
        self.API_URI = "https://docs.cntd.ru/api/document/{}/content/text/block/{}?strict=true"  # doc_id, num_page

    def start_mera(self):
        err_nlz = []
        mypath = "../Task_4/tables/t3"
        # files = glob.glob("../Task_4/tables/e4/*.xlsx")
        files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for file_name in files:
            try:
                file_name = file_name.replace(".xlsx", "")
                # file_name = re.search(r'\\(.*?)\.xlsx', file).group(1)
                file = f'../Task_4/tables/t3/{file_name}.xlsx'
                name_split = file_name.split("__")
                reg = name_split[0].split("_")[0]
                reg_name = name_split[1]
                path = "./mera/%s" % name_split[1]
                name = "_".join(reg_name.split(" "))
                try:
                    os.mkdir("./mera/%s" % reg_name)
                except OSError:
                    print("Создать директорию %s не удалось" % reg_name)
                else:
                    print("Успешно создана директория %s " % reg_name)


                xslx_file = {}
                df = pd.read_excel(file)
                if not len(df):
                    continue

                docs_of_mera = self.filter_docs_mera(df, file_name)

                if len(docs_of_mera):
                    for i, doc in enumerate(docs_of_mera):
                        reg_name += "__{}".format(doc["id"])

                        self.doc_id = int(doc["id"])
                        amount = self.get_amount_mera()
                        store = self.get_pages_mera(amount)
                        soup = BeautifulSoup(store, features="lxml")
                        text = soup.get_text(" ")
                        xslx_file[f"{i}"] = {**doc, "Текст": text}

                        # file_save = f'{path}/{reg}_{self.type_docs}__{name}.html'
                        # self.save(store, file_save)

                final_df = pd.read_json(json.dumps(xslx_file), orient='index')
                final_df.to_csv(f'{path}/{reg}_{self.type_docs}__{name}.csv', encoding="utf-8")

            except Exception as e:
                err_nlz.append({
                    "name": file_name,
                    "error": str(e) if str(e) else "SomeError",
                })
                continue

        if err_nlz:
            with open(f'./log/log-nlz.json', "w", encoding='utf-8') as f:
                json.dump(err_nlz, f, indent=4)

    def filter_docs_mera(self, df, file_name):
        region = file_name.split("__")[1].split("_")
        pattern = [re.compile(f'{i[:-2].upper()}{chr(92)}w*') for i in region]
        df.drop_duplicates(subset=['Наименование'], keep=False, inplace=True)
        df.reset_index(inplace=True)

        docs_of_mera = []
        print(len(df))

        for u in range(len(df)):
            mera = df['Наименование'][u][:160]
            pattern2 = [re.compile(f'{i[:-3].upper()}{chr(92)}w*') for i in mera.split(" ") if len(i) > 5]
            page = 1
            region_sch = " ".join(region)

            params = {
                'q': f'{mera} {region_sch}',
                'page': page
            }
            response = requests.get('https://docs.cntd.ru/api/search/intellectual/documents', params=params)
            if response.status_code != 200:
                time.sleep(5)
                response = requests.get('https://docs.cntd.ru/api/search/intellectual/documents', params=params)

            data = json.loads(response.text)
            pages = [data["documents"]["data"]]

            print(mera, data["documents"]["pagination"]["total"])

            if int(data["documents"]["pagination"]["last_page"]) > 1:
                for i in range(1, int(data["documents"]["pagination"]["last_page"])):
                    page += 1
                    params = {
                        'q': f'{mera} {region}',
                        'page': page
                    }
                    response = requests.get('https://docs.cntd.ru/api/search/intellectual/documents', params=params)
                    if response.status_code != 200:
                        time.sleep(5)
                        page -= 1
                    else:
                        text = f'***Получили страницу {i} ***'
                        print('\b' * len(text), end='', flush=True)
                        print(text, end='', flush=True)

                        time.sleep(0.5)

                        pages.append(json.loads(response.text)["documents"]["data"])
                print("\n")
            filter_doc = []
            try:
                for page in pages:
                    for i in page:
                        if i["status"] != None:
                            if i["status"]["id"] == 1:
                                if i["registrations"][0]["date"] != None:
                                    true_arr = []
                                    true_arr2 = []
                                    if not re.findall(r"О ВНЕСЕН\w*", i["names"][0].upper()) and re.findall(r"ПОРЯД\w*", i["names"][0].upper()):
                                        for ptn in pattern2:
                                            if re.findall(ptn, i["names"][0].upper()):
                                                true_arr2.append(1)
                                            else:
                                                true_arr2.append(0)

                                        for ptn in pattern:
                                            if re.findall(ptn, i["registrations"][0]["doctype"]["name"].upper()):
                                                true_arr.append(1)
                                            else:
                                                true_arr.append(0)
                                        if not 0 in true_arr:
                                            if len(true_arr2) and true_arr2.count(1) / len(true_arr2) > 0.5:
                                                if len(filter_doc):
                                                    date = filter_doc[0]["registrations"][0]["date"]

                                                    if dt.datetime.strptime(i["registrations"][0]["date"],
                                                                            '%Y-%m-%d') > dt.datetime.strptime(date,
                                                                                                               '%Y-%m-%d'):
                                                        del filter_doc[0]
                                                        filter_doc.append(
                                                            {
                                                                "id": int(i['id']),
                                                                "doc_name": i["names"][0],
                                                                "department": i["registrations"][0]["department"]["name"],
                                                                "doctype": i["registrations"][0]["doctype"]["name"],
                                                                "date": i["registrations"][0]["date"],
                                                                "number": str(i["registrations"][0]["number"]),
                                                                "link": f"https://docs.cntd.ru/document/{i['id']}"
                                                            }
                                                        )
                                                else:
                                                    filter_doc.append(
                                                        {
                                                            "id": int(i['id']),
                                                            "doc_name": i["names"][0],
                                                            "department": i["registrations"][0]["department"]["name"],
                                                            "doctype": i["registrations"][0]["doctype"]["name"],
                                                            "date": i["registrations"][0]["date"],
                                                            "number": str(i["registrations"][0]["number"]),
                                                            "link": f"https://docs.cntd.ru/document/{i['id']}"
                                                        }
                                                    )
            except:
                continue

            csr = str(df['ЦСР'][u])
            vr = str(df['ВР'][u]) if df['ВР'][u] else df['ВР'][u]
            budget23 = str(df['Бюджет 2023'][u])
            budget24 = str(df['Бюджет 2024'][u])
            budget25 = str(df['Бюджет 2025'][u])

            if len(filter_doc):
                docs_of_mera.append(
                    {
                        "Наименование меры": df['Наименование'][u] if df['Наименование'][u] else None,
                        "ЦСР": csr if csr else None,
                        "ВР": vr if vr else None,
                        "Бюджет 2023": budget23 if budget23 else None,
                        "Бюджет 2024": budget24 if budget24 else None,
                        "Бюджет 2025": budget25 if budget25 else None,
                        "id": filter_doc[0]["id"] if filter_doc[0]["id"] else None,
                        "Наименование документа": filter_doc[0]["doc_name"] if filter_doc[0]["doc_name"] else None,
                        "Департамент": filter_doc[0]["department"] if filter_doc[0]["department"] else None,
                        "Тип документа": filter_doc[0]["doctype"] if filter_doc[0]["doctype"] else None,
                        "Дата": filter_doc[0]["date"] if filter_doc[0]["date"] else None,
                        "Номер приказа": filter_doc[0]["number"] if filter_doc[0]["number"] else None,
                        "Ссылка": filter_doc[0]["link"] if filter_doc[0]["link"] else None
                    }
                )

        return docs_of_mera

    def get_amount_mera(self):  # Возвращает количество страниц для парсинга
        driver = uc.Chrome()
        driver.set_page_load_timeout(5)
        driver.get('https://docs.cntd.ru/document/{}'.format(self.doc_id))  # Получаем HTML страницу по IDшнику
        response = driver.find_elements(by=By.XPATH, value='//div[@class="document-content"]/div/div/div')
        driver.close()

        amount = len(response)
        print(f'Всего страниц = {amount}')
        return amount

    def get_pages_mera(self, amount: int):
        store = ""
        for i in range(1, amount + 1):
            item = self.parse_page_mera(i)
            time.sleep(0.5)
            store += item
            text = f'***Получили страницу {i} ***'
            print('\b' * len(text), end='', flush=True)
            print(text, end='', flush=True)
            print()

        return store

    def parse_page_mera(self, num_page: int):
        response = requests.get(self.API_URI.format(self.doc_id, num_page))
        if len(response.text) == 0:
            print("ПОЛУЧИЛИ ПУСТУЮ СТРАНИЦУ")
            time.sleep(5)
            response = requests.get(self.API_URI.format(self.doc_id, num_page))
        return response.text

    def save_mera(self, store: str, file_name: str):

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(store)


if __name__ == "__main__":
    TakeMeraDocs().start_mera()
