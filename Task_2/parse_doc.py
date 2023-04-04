"""
Тут я сделал простенький парсер CNTD для доков с известным идентификатором
"""
import time
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


class ParseDoc:

    def __init__(self):
        self.doc_id = None
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

    def start_parse(self, doc_id: int, name: str, reg: int):
        name = "_".join(name.split(" "))
        self.doc_id = doc_id
        amount = self.get_amount()
        store = self.get_pages(amount)
        file_name = self.save_txt(store, name, reg)
        return file_name

    def get_amount(self):  # Возвращает количество страниц для парсинга
        driver = uc.Chrome()
        driver.set_page_load_timeout(5)
        driver.get('https://docs.cntd.ru/document/{}'.format(self.doc_id))  # Получаем HTML страницу по IDшнику
        response = driver.find_elements(by=By.XPATH, value='//div[@class="document-content"]/div/div/div')
        driver.close()

        amount = len(response)
        print(f'Всего страниц = {amount}')
        return amount

    def get_pages(self, amount: int):
        store = ""
        for i in range(1, amount + 1):
            item = self.parse_page(i)
            time.sleep(0.5)
            store += item
            text = f'***Получили страницу {i} ***'
            print('\b' * len(text), end='', flush=True)
            print(text, end='', flush=True)

        return store

    def parse_page(self, num_page: int):
        response = requests.get(self.API_URI.format(self.doc_id, num_page))
        if len(response.text) == 0:
            print("ПОЛУЧИЛИ ПУСТУЮ СТРАНИЦУ")
            time.sleep(5)
            response = requests.get(self.API_URI.format(self.doc_id, num_page))
        return response.text

    def save_txt(self, store: str, name: str, reg: int):
        file_name = f'./src/budget/{reg}_Бюджеты__{name}.html'

        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(store)

        return file_name
