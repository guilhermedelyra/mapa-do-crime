from colour import Color
import json
import unicodedata
from collections import defaultdict
# https://coolors.co/242f3e-d59563-fe4a49-6bd425-fde74c
red = Color("#FE4A49")
yellow = Color("#FDE74C")
green = Color("#6BD425")
black = Color("#000000")
colors = list(green.range_to(Color(yellow),400)) + list(yellow.range_to(Color(red),1500))

def ra(text):
	return (unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')).decode('utf-8').lower().replace('/', '').replace('  ', ' ').replace(' ', '_')

bairros = ['Brasília','Gama','Taguatinga','Brazlândia','Sobradinho','Planaltina','Paranoá','Núcleo Bandeirante','Ceilândia','Guará','Cruzeiro','Samambaia','Santa Maria','São Sebastião','Recanto das Emas','Lago Sul','Riacho Fundo','Lago Norte','Candangolândia','Águas Claras','Riacho Fundo II','Sudoeste / Octogonal','Varjão','Park Way','SCIA','Sobradinho II','Jardim Botânico','Itapoã','SIA','Vicente Pires','Fercal']

_global = open('.data/jsons/global.json', 'r')
jg = json.load(_global)
jg = jg['Maiores-Ocorrencias']

for bairro in bairros:
	file_name = ra(bairro)
	fin = open('.data/jsons/'+file_name+'1.json', 'r')	
	fout = open('.data/jsons/'+file_name+'2.json', 'w')

	jb = json.load(fin)
	
	xd = dict(jb['properties'])
	del xd['name']
	del xd['center']

	idx = defaultdict(lambda:defaultdict(lambda:0))

	for key, value in jg.items():
		for k, v in value.items():
			i = 1
			if (k in xd[key]):
				i = int((xd[key][k]*1900)/v)
			if i != 0:
				i -= 1
			col = colors[i]
			stk = list(col.range_to(Color(black),3))[1]
			idx[key][k] = {"fillColor":str(col), "strokeColor":str(stk)}
	ha = [{key : str(dict(value))} for key, value in idx.items()]
	cl='},"Colors":'+str(ha).replace('"{', '{').replace('"}', '').replace('}}, {', '}},').replace('[','').replace(']','}')
	final = (str(jb).strip('}') + cl + '}}').replace('\'', '"')
	fout.write(final)