import requests
from bs4 import BeautifulSoup
from fractions import Fraction
import json
from datetime import datetime


from .utils.data_classes import Dato, Jugador, Equipo, CasaDeApuestas
from .utils.logger import apuestas_logger as logger


class Williamhill(CasaDeApuestas):
	def __init__(self):
		self.s=requests.Session()
		self.nombre="williamhill"
		CasaDeApuestas.__init__(self,self.nombre)
		self.DATA=[]	

	def buscar_partidos(self):
		self.url="https://sports.williamhill.es/betting/es-es/tenis/partidos/competici%C3%B3n/hoy"
		self.respuesta=self.s.get(self.url)
		if self.respuesta.status_code!=200:
			logger.error("Response Code: "+str(self.respuesta.status_code))
			return 0
		self.respuesta_text=self.respuesta.text
		logger.debug("Response code: "+str(self.respuesta.status_code))
	
	def parsear_partidos(self):
		self.DATA=[]
		self.soup=BeautifulSoup(self.respuesta_text,'html.parser')
		# eventos es una lista con cadauno de "los partidos"
		self.eventos=self.soup.find_all('div',{'class':'event'})

		for e in self.eventos:
			try:
				# Equipo
				nombres=e.find('a').find_all('span')
				n1=nombres[0].text
				n2=nombres[1].text
				dobles=True if '/' in n1 else False
				# print(n1,n2,dobles)
				if not dobles:
					seleccion=False if ' ' in n1 else True # si es un equipode una seleccion nacional
					if seleccion:
						logger.warning("se ha omitido un partido de selecciones: "+str(n1))
						continue
					n1,a1=n1.rsplit(' ',1)
					equipo1=Equipo(Jugador(nombre=n1,apellido=a1,web=self.nombre))
					n2,a2=n2.rsplit(' ',1)
					equipo2=Equipo(Jugador(nombre=n2,apellido=a2,web=self.nombre))
				else:
					e1j1,e1j2=n1.split("/")
					equipo1=Equipo(Jugador(apellido=e1j1,web=self.nombre),Jugador(apellido=e1j2,web=self.nombre))
					e2j1,e2j2=n2.split("/")
					equipo2=Equipo(Jugador(apellido=e2j1,web=self.nombre),Jugador(apellido=e2j2,web=self.nombre))
				
				# odds
				b=e.find_all('button')
				precio1=Fraction(b[0]['data-odds'])+1 # le sumo 1
				precio2=Fraction(b[1]['data-odds'])+1 # le sumo 1

				# fecha
				unix_timestamp=None
				try:
					fecha_ISOSTRING=e.find('time')['datetime']
					# https://stackoverflow.com/questions/969285/how-do-i-translate-an-iso-8601-datetime-string-into-a-python-datetime-object
					unix_timestamp=int(datetime.strptime(fecha_ISOSTRING, "%Y-%m-%dT%H:%M:%S%z").timestamp())
				except TypeError as e:
					logger.debug("warning que ignoro: no se ha podido parsear la fecha: "+str(e))

				except Exception as e:
					logger.timestamp_warning("No se ha podido parsear la fecha: "+str(e))

				self.DATA.append(Dato(equipo1,equipo2,precio1,precio2,dobles=dobles,timestamp=unix_timestamp))	

			except Exception as e:
				"""
				Falla cuando las odds es una string: 'EVS'
				"""
				if 'EVS' in str(e):
					logger.debug("Warning ignorado: "+str(e))
					continue
				logger.warning("Un partido no se ha podido parsear bien: "+str(e)+" line: "+str(e.__traceback__.tb_lineno))
		logger.debug("Partidos parseados")

		
if __name__=='__main__':
	w=Williamhill()
	w.buscar_partidos()
	# w.guardar_html()
	# w.cargar_html()
	w.parsear_partidos()
	w.guardar_data_en_json()
	# w.print()	
