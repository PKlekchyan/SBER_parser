import math

def filter_to_statesupport(list):
	prev_result = []

	for index, line in enumerate(list):
		if not math.isnan(line['ВР']) and float(line['ВР']) // 800 == 1 :
			pointer = index
			x8_index = pointer
			x8_name = line['Наименование']
			note = {}
			
			while True and pointer > 0:
				pointer -= 1
				this_line = list[pointer]
				
				if math.isnan(this_line['ВР']):
					note = ({
						'Наименование': this_line['Наименование'],
						'Бюджет 2023': (this_line['2023']),
						'Бюджет 2024': (this_line['2024']),
						'Бюджет 2025': (this_line['2025']),
						'ЦСР': this_line['ЦСР'],
						'ВР': this_line['ВР'],
						'Номер строки меры': pointer,
						'8xx - Номер строки': x8_index,
						'8xx - Наименование': x8_name,
					})
					
					# Находим направление программы
					while True and pointer > 0:
						pointer -= 1
						this_line = list[pointer]
						if math.isnan(this_line['ВР']) and math.isnan(this_line['ЦСР']): note['Сфера программы'] = this_line['Наименование']
						break
					
					prev_result.append(note)
					break

	return prev_result