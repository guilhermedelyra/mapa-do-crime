import cairo
import re
import json
import os
import unicodedata
import ast

if not os.path.exists('.data/imgs'):
    os.makedirs('.data/imgs')

def ra(text):
	return (unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')).decode('utf-8').lower().replace('/', '').replace('  ', ' ').replace(' ', '_')

def text_extent(font, font_size, text, *args, **kwargs):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
    ctx = cairo.Context(surface)
    ctx.select_font_face(font, *args, **kwargs)
    ctx.set_font_size(font_size)
    return ctx.text_extents(text)

bairros = ['Brasília','Gama','Taguatinga','Brazlândia','Sobradinho','Planaltina','Paranoá','Núcleo Bandeirante','Ceilândia','Guará','Cruzeiro','Samambaia','Santa Maria','São Sebastião','Recanto das Emas','Lago Sul','Riacho Fundo','Lago Norte','Candangolândia','Águas Claras','Riacho Fundo II','Sudoeste','Varjão','Park Way','SCIA','Sobradinho II','Jardim Botânico','Itapoã','SIA','Vicente Pires','Fercal']

for bairro in bairros:
	file_name = ra(bairro)
	text=bairro
	font="Roboto"
	font_size=55.0
	font_args=[cairo.FONT_SLANT_NORMAL]
	(x_bearing, y_bearing, text_width, text_height,
	 x_advance, y_advance) = text_extent(font, font_size, text, *font_args)
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(text_width), int(text_height))
	ctx = cairo.Context(surface)
	ctx.select_font_face(font, *font_args)
	ctx.set_font_size(font_size)
	ctx.move_to(-x_bearing, -y_bearing)
	ctx.text_path(text)
	ctx.set_source_rgb(0.84, 0.58, 0.39)
	ctx.fill_preserve()
	ctx.set_source_rgb(0.14, 0.18, 0.24)
	ctx.set_line_width(1.8)
	ctx.stroke()

	surface.write_to_png(".data/imgs/"+file_name+".png")