from pprint import pprint

import pandas as pd


group_count: int = 0
group: list = []
data: list = []
tmp: str = ''
with open('original_source.txt', 'r', encoding='UTF-8') as source:
	for line in source.readlines():
		if line == '\n':
			data.append(group)
			group_count = 0
			group = []
			continue
		tmp = line.strip().strip('\n')
		if tmp == '-' or tmp == '':
			group.append('')
			group_count += 1
			continue
		if group_count < 1:
			group_count += 1
			continue
		if group_count == 1:
			if tmp.lower().find('logo') == -1:
				group.append(tmp.strip().strip('\n'))
			group_count += 1
			continue
		if group_count == 2 or group_count == 5 or group_count == 6 or group_count == 7:
			tmp = tmp.split(',')
			group.append(tmp[0].strip().strip('\n'))
		if group_count == 3:
			for i in range(2001, 2050):
				if tmp.find(str(i)) != -1:
					group.append(str(i))
					break
		if group_count == 4:
			tmp = tmp.split(',')
			group.append(tmp[0].strip())
			group.append(tmp[-1].strip())
		if group_count == 8 or group_count == 11:
			group.append(tmp[1::].replace(',', ''))
		if group_count == 9 or group_count == 10:
			group.append(tmp.lower())
		group_count += 1

with open('source.csv', 'w', encoding='UTF-8') as output:
	output.write('Company,Founded Year,City,Nation,Industry,Founder,Investor,Total Founding,Company Type,Operating Status,Last Valuation\n')
	for sample in data:
		tmp = [s if s != '—' and s != '' else '' for s in sample]
		output.write(','.join(tmp)+'\n')

# dataset = pd.read_csv('source.csv', sep=',', encoding='utf-8')
# dataset.drop_duplicates()
# dataset.to_csv('source.csv', encoding='utf-8')

