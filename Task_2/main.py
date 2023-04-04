import datetime
import json
from parse_doc import ParseDoc
from take_table import TakeTableFromDoc
import pandas as pd
import os, inspect, sys


def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


if __name__ == "__main__":
    df = pd.read_excel("../task_1/regions_data.xlsx")
    err_parse = []
    err_nlz = []
    for i in range(len(df)):
        print()
        print("-------------------------------------------")
        print(f'Парсим документ региона - {df["region"][i]}')
        try:
            name = ParseDoc().start_parse(df["id"][i], df["region"][i], i+1)
        except Exception as e:
            err_parse.append({
                "key": i,
                "error": str(e) if str(e) else "SomeError",
            })
            continue

        try:
            path = os.path.join(get_script_dir(), f'{name}')
            TakeTableFromDoc().start(path, i+1)
        except Exception as e:
            err_nlz.append({
                "key": i,
                "error": str(e) if str(e) else "SomeError",
            })
            continue

    time = datetime.datetime.now().strftime("%d-%m-%Y__%H-%M-%S")

    if err_parse:
        with open(f'./src/log/log-parse__{time}.json', "w", encoding='utf-8') as f:
            json.dump(err_parse, f, indent=4)

    if err_nlz:
        with open(f'./src/log/log-nlz__{time}.json', "w", encoding='utf-8') as f:
            json.dump(err_nlz, f, indent=4)