import re
import json
import os
import unicodedata
import ast

if not os.path.exists('.data/jsons'):
    os.makedirs('.data/jsons')

def ra(text):
	return (unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')).decode('utf-8').lower().replace('/', '').replace('  ', ' ').replace(' ', '_')

bairros = ['Brasília','Gama','Taguatinga','Brazlândia','Sobradinho','Planaltina','Paranoá','Núcleo Bandeirante','Ceilândia','Guará','Cruzeiro','Samambaia','Santa Maria','São Sebastião','Recanto das Emas','Lago Sul','Riacho Fundo','Lago Norte','Candangolândia','Águas Claras','Riacho Fundo II','Sudoeste / Octogonal','Varjão','Park Way','SCIA','Sobradinho II','Jardim Botânico','Itapoã','SIA','Vicente Pires','Fercal']

for bairro in bairros:
	file_name = ra(bairro)
	# print('\''+file_name+'\',', end='')
	fin = open('htmls/'+file_name+'.txt', 'r')
	fout = open('.data/jsons/'+file_name+'.json', 'w')

	html = fin.read()

	if bairro == 'Brasília':
		bairro = 'Plano Piloto'

	word_to_regex = (json.dumps(bairro)).replace('\"', '').replace(r'\u', r'\\u').replace(' ', r'\s').replace(r'/', r'\\\/').replace('II', '2')
	pat_DF1 = r'\"langaddress\"\:\s\"' + word_to_regex + r'\,\sRegi\\u00e3o\sIntegrada\sde\sDesenvolvimento\sdo\sDistrito\sFederal\se\sEntorno\,\sDF\,\sRegi\\u00e3o\sCentro-Oeste\,\sBrasil\"'
	pat_DF2 = r'\"langaddress\"\:\s\"' + word_to_regex + r'\,\sRegi\\u00e3o\sIntegrada\sde\sDesenvolvimento\sdo\sDistrito\sFederal\se\sEntorno\,\sDistrito\sFederal\,\sRegi\\u00e3o\sCentro-Oeste\,\sBrasil\"'
	pat_DF3 = r'\"langaddress\"\:\s\"' + word_to_regex + r'\,\sRegi\\u00e3o\sIntegrada\sde\sDesenvolvimento\sdo\sDistrito\sFederal\se\sEntorno\,\sDF\,\sRegi\\u00e3o\sCentro-Oeste'
	pat_DF4 = r'\"langaddress\"\:\s\"' + word_to_regex + r'\,\sRegi\\u00e3o\sIntegrada\sde\sDesenvolvimento\sdo\sDistrito\sFederal\se\sEntorno\,\sDistrito\sFederal\,\sRegi\\u00e3o\sCentro-Oeste'
	pattern_city1 = r'(?<=' + pat_DF1 + r')(.*?)(?=\"icon)'
	pattern_city2 = r'(?<=' + pat_DF2 + r')(.*?)(?=\"icon)'
	pattern_city3 = r'(?<=' + pat_DF3 + r')(.*?)(?=\"icon)'
	pattern_city4 = r'(?<=' + pat_DF4 + r')(.*?)(?=\"icon)'

	find_city1 = re.compile(pattern_city1, re.DOTALL)
	find_city2 = re.compile(pattern_city2, re.DOTALL)
	find_city3 = re.compile(pattern_city3, re.DOTALL)
	find_city4 = re.compile(pattern_city4, re.DOTALL)


	extract_json = re.compile(r'(\{.*?\})')
	extract_bounding = re.compile(r'\s(\[.*?\])', re.DOTALL)

	string_json = find_city1.findall(html)
	if (len(string_json) == 0):
		string_json = find_city2.findall(html)
	if (len(string_json) == 0):
		string_json = find_city3.findall(html)
	if (len(string_json) == 0):
		string_json = find_city4.findall(html)

	bounding_box = extract_bounding.findall(string_json[0])
	trimmed_bb = re.sub(r'[\n\s\t\"]*','', bounding_box[0]) 
	rbound = ast.literal_eval(trimmed_bb)

	lng = str(rbound[3] + ((rbound[2]-rbound[3])/2.0))
	lat = str(rbound[1] + ((rbound[0]-rbound[1])/2.0))

	rjson = extract_json.findall(string_json[0])
	final_json = '{"type": "Feature", "geometry": '+rjson[0].replace(r'\\"', r'"').replace(r'\"', r'"')+', "properties":{"name":"'+bairro+'","center":['+lat+','+lng+']}}'
	fout.write(final_json) 
	fin.close()