import requests
from typing import TypedDict
from api.constants.regions import RegionInterface
from api.utils.is_budget_doc import is_budget_doc
from api.utils.transform_doc_struct import transform_doc_struct

API_ENDPOINT = 'https://docs.cntd.ru/api/search'

class SearchParams(TypedDict):
	order_by: str # registration_date:desc, registration_date:asc
	category: int # тип документа, в нашем случае 4 - региональное право
	thematic: int # тематика документа, в нашем случае 675300007 - Государственные (муниципальные программы)
	region: int # тут все понятно, но у cntd свои 'id' для регионов
	query: str # еще и ищет по тексту

def get_region_budget(region: RegionInterface, year: int = 2023,  text: str = 'бюджет', ):
	params: SearchParams = {
		"order_by": 'registration_date:desc',
		"category": 4,
		"thematic": (675300007,675300008)[region['name'] == 'Республика Ингушетия'] ,
		"region" : region['id'],
		"query": text 
	}

	response = requests.get(API_ENDPOINT, params=params)
	total_pages = response.json()['pagination']['last_page']

	for page in range(1, total_pages):
		response = requests.get(API_ENDPOINT, params={**params, 'page': page})
		docs = response.json()['data']
		filtred_docs = list(filter(lambda doc: is_budget_doc(doc, region['name']), docs))

		if (len(filtred_docs)): 
			print(region["name"] + ' --- ' + filtred_docs[0]['names'][0])
			return transform_doc_struct(filtred_docs[0], region["name"])

	return print(f'Для региона - {region["name"]} - не было найдено бюджетных планов')
