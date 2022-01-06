import random, string
from flask import Flask, render_template, request, make_response
import json
import pandas as pd
import time

from scripts.apuestas import Apuestas

a=Apuestas()
# a.buscar_partidos()
a.cargar_partidos()
a.comparar()
a.actualizar_json()
# a.ordenar_eventos_alfabeticamente()
# a.pretty_print()



app = Flask(__name__)

ok_chars = string.ascii_letters + string.digits

@app.route('/')  # What happens when the user visits the site
def base_page():
	df=a.to_dataframe()
	html=df.to_html()
	html=html.replace('NaN','')
	html=time.asctime()+'\n\n'+html
	# html=html.replace('williamhill','<a href="https://sports.williamhill.es/betting/es-es/tenis/partidos/competici%C3%B3n/hoy">williamhill</a>')
	return html

# @app.route('/williamhill')
# def williamhill():
# 	return open('API/htmls/williamhill.html').read()

# @app.route('/betfair')
# def betfair():
# 	return open('API/htmls/betfair.html').read()

# @app.route('/betstars')
# def betstars():
# 	return open('API/htmls/betstars.html').read()

# @app.route('/bwin')
# def bwin():
	# return open('API/htmls/bwin.html').read()

# print("nombre:",__name__)

if __name__ == "__main__" or __name__=='API.web':
	app.run(host='0.0.0.0',port=4000,debug=True)
