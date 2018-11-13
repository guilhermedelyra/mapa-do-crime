import csv
import codecs
import pandas as pd
import json
import unicodedata
from collections import defaultdict

def ra(text):
	return (unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')).decode('utf-8').lower().replace('/', '').replace('  ', ' ').replace(' ', '_')

filename = '.data/csvs/ocorrenciasmun-brasil'

bairros = ['Brasília','Gama','Taguatinga','Brazlândia','Sobradinho','Planaltina','Paranoá','Núcleo Bandeirante','Ceilândia','Guará','Cruzeiro','Samambaia','Santa Maria','São Sebastião','Recanto das Emas','Lago Sul','Riacho Fundo','Lago Norte','Candangolândia','Águas Claras','Riacho Fundo II','Sudoeste / Octogonal','Varjão','Park Way','SCIA','Sobradinho II','Jardim Botânico','Itapoã','SIA','Vicente Pires','Fercal']
df = []
for i in range(2013, 2018):
	path = filename+str(i)
	df.append(pd.read_csv(path+'-lol.csv', encoding='latin1'))

max_crimes = defaultdict(lambda: 0)
all_crimes = 0
for bairro in bairros:
	file_name = ra(bairro)
	fin = open('.data/jsons/'+file_name+'.json', 'r')
	fout = open('.data/jsons/'+file_name+'1.json', 'w')
	js = fin.read().strip('}}\n')

	tot_crimes = defaultdict(lambda: 0)

	for i in range(0, 5):
		js += ', "'+str(2013+i)+'":{'
		cdf = df[i]
		lal = cdf[cdf['Município'] == bairro]
		out = lal.to_json(orient='records')
		d = json.loads(out)
		tot = 0
		for j in d:
			tipo_crime = j['Tipo Crime']
			qtd_crime = int(j['PC-Qtde Ocorrências'])
			tot_crimes[tipo_crime] += qtd_crime
			tot += qtd_crime
			js += '"' + tipo_crime + '":' + str(qtd_crime) + ','

		tot_crimes['Total'] += tot
		js+='"Total":'+str(tot)+'},'

		max_crimes[str(2013+i)] = max(max_crimes[str(2013+i)], tot)
		all_crimes+=tot

	js+='"All":'+str(dict(tot_crimes)).replace('\'', '"')
	js+='}}'

	fout.write(js.replace(',}', '}').replace(',,', ','))

print(max_crimes)
print(all_crimes)