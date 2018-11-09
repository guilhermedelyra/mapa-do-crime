import requests
import os
import unicodedata

if not os.path.exists('htmls'):
    os.makedirs('htmls')

def ra(text):
	return (unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')).decode('utf-8').lower().replace('/', '').replace('  ', ' ').replace(' ', '_')


bairros = ['Brasília','Gama','Taguatinga','Brazlândia','Sobradinho','Planaltina','Paranoá','Núcleo Bandeirante','Ceilândia','Guará','Cruzeiro','Samambaia','Santa Maria','São Sebastião','Recanto das Emas','Lago Sul','Riacho Fundo','Lago Norte','Candangolândia','Águas Claras','Riacho Fundo II','Sudoeste / Octogonal','Varjão','Park Way','SCIA','Sobradinho II','Jardim Botânico','Itapoã','SIA','Vicente Pires','Fercal']

for bairro in bairros:
	r = requests.get("https://nominatim.openstreetmap.org/search.php?q=%s+brasilia+distrito+federal&polygon_geojson=1&viewbox=" % bairro.replace(' ', '+'))
	html = r.text

	file_name = ra(bairro)
	
	fout = open('htmls/'+file_name+'.txt', 'w')
	fout.write(html)
	fout.close()