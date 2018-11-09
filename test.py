import re
f = open('example.txt')
kk = f.read()
tt = r'(?<=\"langaddress\"\:\s\"Gama\,\sRegi\\u00e3o\sIntegrada\sde\sDesenvolvimento\sdo\sDistrito\sFederal\se\sEntorno\,\sDistrito\sFederal\,\sRegi\\u00e3o\sCentro-Oeste\,\sBrasil\")(.*?)(?=aBoundingBox)'
#rg = re.compile(r'(?<=\"langaddress\"\:\s\"Bras\\u00edlia\,\sRegi\\u00e3o\sIntegrada\sde\sDesenvolvimento\sdo\sDistrito\sFederal\se\sEntorno\,\sDistrito\sFederal\,\sRegi\\u00e3o\sCentro-Oeste\,\sBrasil\")(.*?)(?=aBoundingBox)', re.DOTALL)
rg = re.compile(tt, re.DOTALL)
# la = re.compile(r'(\{.*?\})')
xd = rg.findall(kk)
print(xd)
print(len(xd))
