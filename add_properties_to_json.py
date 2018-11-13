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

max_crimes = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:0)))
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
			
			max_crimes['Ocorrencias-Totais'][str(2013+i)][tipo_crime] += qtd_crime
			max_crimes['Ocorrencias-Totais']['All'][tipo_crime] += qtd_crime

			max_crimes['Maiores-Ocorrencias'][str(2013+i)][tipo_crime] = max(max_crimes['Maiores-Ocorrencias'][str(2013+i)][tipo_crime], qtd_crime)

			tot += qtd_crime
			js += '"' + tipo_crime + '":' + str(qtd_crime) + ','

		tot_crimes['Total'] += tot
		max_crimes['Ocorrencias-Totais'][str(2013+i)]['Total'] += tot
		max_crimes['Ocorrencias-Totais']['All']['Total'] += tot
		max_crimes['Maiores-Ocorrencias'][str(2013+i)]['Total'] = max(max_crimes['Maiores-Ocorrencias'][str(2013+i)]['Total'], tot)

		js+='"Total":'+str(tot)+'},'

	js+='"All":'+str(dict(tot_crimes)).replace('\'', '"')
	js+='}}'
	for key, value in tot_crimes.items():
		max_crimes['Maiores-Ocorrencias']['All'][key] = max(max_crimes['Maiores-Ocorrencias']['All'][key], tot_crimes[key])

	fout.write(js.replace(',}', '}').replace(',,', ','))

aaa = [str({key: [{k: dict(v)} for k, v in value.items()]}) for key, value in max_crimes.items()]
for a in aaa:
	print(a.replace('\'', '"'))
