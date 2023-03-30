import pandas as pd
from api.constants.regions import REGIONS as regions
from api.api import get_region_budget

if __name__ == "__main__":
	docs_list = []

	for region in regions:
		doc = get_region_budget(region)
		docs_list.append(doc)

	df = pd.DataFrame(docs_list)

	df.to_excel('./regions_data.xlsx')
