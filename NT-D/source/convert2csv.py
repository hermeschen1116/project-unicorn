from pprint import pprint

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
		if tmp == '-':
			group.append('')
			group_count += 1
			continue
		if group_count < 2:
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
		if group_count == 9:
			if tmp.lower().find('non'):
				group.append('Y')
			elif tmp.lower() == 'for profit':
				group.append('N')
			else:
				group.append(tmp)
		if group_count == 10:
			if tmp.lower() == 'active':
				group.append('Y')
			elif tmp.lower() == 'closed':
				group.append('N')
			else:
				group.append(tmp)
		group_count += 1

with open('source.csv', 'w', encoding='UTF-8') as output:
	output.write('Company, Found Date, City, Nation, Industry, Founder, Investor, Total Founding, Company Type, Operating Status, Last Valuation\n')
	for sample in data:
		tmp = [s if s != '—' or s != '' else '' for s in sample]
		output.write(', '.join(tmp)+'\n')

