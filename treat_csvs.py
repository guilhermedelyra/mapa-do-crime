import csv
import codecs
import pandas as pd

filename = '.data/csvs/ocorrenciasmun-brasil'

for i in range(2013, 2018):
	path = filename+str(i)

	# with open(path+'-head.csv', 'rb') as inp, open(path+'-df.csv', 'wb') as out:
	# 	print(path)
	# 	writer = csv.writer(out)
	# 	for row in csv.reader(codecs.iterdecode(inp, 'latin1')):
	# 		print(len(row))
	# 		if row[1] == 'DF':
	# 			writer.writerow(row)

	df = pd.read_csv(path+'-head.csv', encoding='latin1', sep=";")
	print(df.columns)
	df = df[df.UF == 'Distrito Federal']
	df = df.groupby(['Município', 'Tipo Crime']).sum().reset_index()
	df.drop('Código IBGE Município', 1, inplace=True)
	df.drop('Mês', 1, inplace=True)

	# so tem dados até junho
	if(i == 2017):
		values = df['PC-Qtde Ocorrências'] * 2
		df['PC-Qtde Ocorrências'] = values
		
	df.to_csv(path+'-lol.csv', encoding='latin1', index=False)

