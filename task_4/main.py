import pandas as pd
import glob
import re
from filter_to_satatesupport import filter_to_statesupport as ftosup


all_files_from_t2 = glob.glob("tables/t2/*.html")
print(all_files_from_t2)

for file in all_files_from_t2:
    file_name = re.search(r'\\(.*?)\.html', file).group(1)
    
    filtred = ftosup(pd.read_html(file, encoding='utf-8')[0].to_dict('records'))
    
    pd.DataFrame(filtred).to_excel(f'tables/t3/{file_name}.xlsx')
    print(f'Меры для "{file_name}" успешно собраны')
