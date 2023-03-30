import re
from api.utils.transform_budget_word import transform_budget_word

def is_budget_doc(doc, region_name:str, year = 2023):
	budget_word = transform_budget_word(region_name)
	reg_ex = fr"^(О|Об)(?= ({budget_word}))(?=.*{year} год).*"
	
	return bool(re.match(reg_ex, doc['names'][0]))
