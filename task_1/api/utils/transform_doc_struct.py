def transform_doc_struct(doc, region_name):
	return {
		'id': doc['id'],
		'region': region_name,
		'name': doc['names'][0],
		'original_link': f"https://docs.cntd.ru/document/{doc['id']}",
		'date': doc['registrations'][0]['date'],
		'doctype': doc['registrations'][0]['doctype']['name'],
		'department': doc['registrations'][0]['department']['name'],
		'number': doc['registrations'][0]['number']
	}
	 
