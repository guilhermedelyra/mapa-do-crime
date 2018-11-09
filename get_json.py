import requests
import re
import json
from bs4 import BeautifulSoup

bairros = ['Brasília','Gama','Taguatinga','Brazlândia','Sobradinho','Planaltina','Paranoá','Núcleo Bandeirante','Ceilândia','Guará','Cruzeiro','Samambaia','Santa Maria','São Sebastião','Recanto das Emas','Lago Sul','Riacho Fundo','Lago Norte','Candangolândia','Águas Claras','Riacho Fundo II','Sudoeste/Octogonal','Varjão','Park Way','SCIA','Sobradinho II','Jardim Botânico','Itapoã','SIA','Vicente Pires','Fercal']

for bairro in bairros:
	# r = requests.get("https://nominatim.openstreetmap.org/search.php?q=%s+brasilia+distrito+federal&polygon_geojson=1&viewbox=" % bairro.replace(' ', '+'))
	# html = r.text
	f = open(bairro.replace('/', ' ')+'.txt', 'r')
	html = f.read()
	# f.write(html)

	if bairro == 'Brasília':
		bairro = 'Plano Piloto'

	word_to_regex = (json.dumps(bairro)).replace('\"', '').replace(r'\u', r'\\u').replace(' ', r'\s')
	pat_DF1 = r'\"langaddress\"\:\s\"' + word_to_regex + r'\,\sRegi\\u00e3o\sIntegrada\sde\sDesenvolvimento\sdo\sDistrito\sFederal\se\sEntorno\,\sDF\,\sRegi\\u00e3o\sCentro-Oeste\,\sBrasil\"'
	pat_DF2 = r'\"langaddress\"\:\s\"' + word_to_regex + r'\,\sRegi\\u00e3o\sIntegrada\sde\sDesenvolvimento\sdo\sDistrito\sFederal\se\sEntorno\,\sDistrito\sFederal\,\sRegi\\u00e3o\sCentro-Oeste\"'
	pattern_city1 = r'(?<=' + pat_DF1 + r')(.*?)(?=aBoundingBox)'
	pattern_city2 = r'(?<=' + pat_DF2 + r')(.*?)(?=aBoundingBox)'

	find_city1 = re.compile(pattern_city1, re.DOTALL)
	find_city2 = re.compile(pattern_city2, re.DOTALL)

	string_json = find_city1.findall(html)
	if (len(string_json) == 0):
		string_json = find_city2.findall(html)
	print(string_json)
	f.close()
	# rjson = json.dumps(string_json[0])
	# print(bairro)
	# print(rjson)
	# print('\n\n\n\n')