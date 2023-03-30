from api.constants.exeptions import EXEPTIONS_REGIONS as exeptions

def transform_budget_word(name: str):
	if dict(exeptions).get(name): return exeptions[name]
	
	budget_word = 'бюджете'

	if 'область' in name:
		reg = name.split()[0]
		budget_word += f" {reg[:-2]}ой области|областном бюджете"

	if 'Республика' in name:
		reg = name.split()[1]
		budget_word += f" Республики {reg[:-2]}|республиканском бюджете"

	if 'край' in name:
		reg = name.split()[0]
		budget_word += f" {reg[:-2]}ого края|краевом бюджете"

	if 'автономный округ' in name:
		reg = name.split()[0]
		budget_word += f" {reg[:-2]}ого автономного округа|окружном бюджете"

	return budget_word
