import random, string
from flask import Flask, render_template, request, make_response
import json
import pandas as pd
import time
import random

from scripts.apuestas import Apuestas

a=Apuestas()
# a.buscar_partidos()
a.cargar_partidos()
a.comparar()
a.actualizar_json()
# a.ordenar_eventos_alfabeticamente()
# a.pretty_print()


# Schedule
# https://stackoverflow.com/questions/21214270/how-to-schedule-a-function-to-run-every-hour-on-flask
# https://pypi.org/project/APScheduler/
from apscheduler.schedulers.background import BackgroundScheduler
import telegram_bot
def f():
	# print("Hola")
	telegram_bot.enviar_mensaje(mensaje="hola")

# schedule = BackgroundScheduler(daemon=True)
# schedule.add_job(f,'interval',minutes=10)
# schedule.start()


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

@app.route('/check')
def check():
	telegram_bot.enviar_mensaje('check apuestas')

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

print("RUNNING...")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=random.randint(2000, 9000))
	# app.run(host='0.0.0.0', port=8080, debug=True)
