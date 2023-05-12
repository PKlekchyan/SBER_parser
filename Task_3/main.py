import datetime
import json
from os import listdir
from os.path import isfile, join
from upload_table import UploadTableFromFile
from normalize import NormalizeTable


class NormalizeStarter:

    def start(self, mypath):
        list_names = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        err_nlz = []
        for i in list_names[2:]:
            try:
                full_path = f'../Task_2/src/tables/{i}'
                df, data = UploadTableFromFile().start(full_path)
                final_df = NormalizeTable().start(df, data)
                final_df.to_html(f"./tables/{i.replace('.html', '')}.html")
            except Exception as e:
                err_nlz.append({
                    "name": i,
                    "error": str(e) if str(e) else "SomeError",
                })
                continue

        time = datetime.datetime.now().strftime("%d-%m-%Y__%H-%M-%S")

        if err_nlz:
            with open(f'./log/log-nlz__{time}.json', "w", encoding='utf-8') as f:
                json.dump(err_nlz, f, indent=4)


NormalizeStarter().start("../Task_2/mera/tables")

