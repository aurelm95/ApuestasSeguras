#bwin
import requests
from fractions import Fraction
from datetime import datetime

from .utils.data_classes import Dato, Jugador, Equipo, CasaDeApuestas
from .utils.logger import apuestas_logger as logger

class Bwin(CasaDeApuestas):
	def __init__(self):
		# https://curl.trillworks.com/
		# importante el "accept-encoding": "text/html",
		# he tenido que retocarlo manualmente para que me devuelva
		# la respuesta bien codificada
		self.s=requests.Session()
		self.nombre="bwin"
		CasaDeApuestas.__init__(self,self.nombre)
		self.DATA=[]
		self.headers = {
		    'origin': 'https://sports.m.bwin.es',
		    "accept-encoding": "text/html",
		    'accept-language': 'es-ES,es;q=0.9',
		    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
		    'content-type': 'application/json',
		    'accept': 'application/json, text/plain, */*',
		    'cache-control': 'no-cache',
		    'authority': 'cds-api.bwin.es',
		    'x-bwin-browser-url': 'https://sports.m.bwin.es/es/sports/tenis-5',
		    'referer': 'https://sports.m.bwin.es/es/sports/tenis-5',
		}

		self.params = (
		    ('x-bwin-accessid', 'OTdhMjU3MWQtYzI5Yi00NWQ5LWFmOGEtNmFhOTJjMWVhNmRl'),
		    ('lang', 'es'),
		    ('country', 'ES'),
		    ('userCountry', 'ES'),
		)

		self.data = '{"sportIds":"5","fixtureCategories":"Gridable,NonGridable,Other","offerMapping":"Filtered","offerCategories":"Gridable,Other","scoreboardMode":"Slim","marqueeRequest":{"marqueeData":[],"take":8},"fixtureTypes":"Standard"}'

	def buscar_partidos(self):
		self.DATA=[]
		self.respuesta = self.s.post('https://cds-api.bwin.es/bettingoffer/lobby/sport', headers=self.headers, params=self.params, data=self.data)
		self.j=self.respuesta.json()
		logger.debug("Status code: "+str(self.respuesta.status_code))

		def parsear_juagador_dobles(s):
			nombre,apellido=s.rsplit('. ',1)
			if len(nombre)==1:
				return Jugador(inicial_nombre=nombre,apellido=apellido,web=self.nombre)
			return Jugador(nombre=nombre,apellido=apellido,web=self.nombre)
		
		def parsear_juagador(s):
			if '(' in s:
				s=s.split('(')[0] # A veces los nombres contienen entre parentesis la nacionalidad. por ejmeplo: Clement Tabur (FRA) o bien: Yuta Shimizu (JPN)
			if s[-1]==' ':
				s=s[:-1] # posiblemente tras el split de arriba quede un espacio final. Lo quito.
			if '. ' in s:
				nombre,apellido=s.rsplit('. ',1)
				if apellido=='': logger.error(s+" -> apellido=''")
				if len(nombre)==1:
					return Jugador(inicial_nombre=nombre,apellido=apellido,web=self.nombre)
				return Jugador(nombre=nombre,apellido=apellido,web=self.nombre)
			elif ' ' in s:
				nombre,apellido=s.rsplit(' ',1)
				if apellido=='': logger.error(s+" -> apellido=''")
				return Jugador(nombre=nombre,apellido=apellido,web=self.nombre)
			return Jugador(apellido=s,web=self.nombre)

		for p in self.j['highlights']:
			try:
				# logger.debug(f"{p['games']=}")
				e1=p['games'][0]['results'][0]
				# Note that due to the usual issues with binary floating-point (see Floating Point Arithmetic: Issues and Limitations), the argument to Fraction(1.1) is not exactly equal to 11/10, and so Fraction(1.1) does not return Fraction(11, 10) as one might expect.
				# https://docs.python.org/2/library/fractions.html
				# He hecho una chapucilla
				odds1=Fraction(int(e1['odds']*100))/100
				j1=e1['name']['value']
				e2=p['games'][0]['results'][1]
				odds2=Fraction(int(e2['odds']*100))/100
				j2=e2['name']['value']
				unix_timestamp=None
				try:
					unix_timestamp=int(datetime.strptime(p['startDate'], "%Y-%m-%dT%H:%M:%SZ").timestamp())
				except Exception as e:
					logger.timestamp_warning("No se ha podido parsear la fecha: "+str(e)+" string original: "+p['startDate'])

				dobles=True if '/' in j1 else False
				if dobles:
					e1j1,e1j2=j1.split('/')
					e2j1,e2j2=j2.split('/')

					e1j1=parsear_juagador_dobles(e1j1)
					e1j2=parsear_juagador_dobles(e1j2)
					e2j1=parsear_juagador_dobles(e2j1)
					e2j2=parsear_juagador_dobles(e2j2)

					self.DATA.append(Dato(Equipo(e1j1,e1j2),Equipo(e2j1,e2j2),odds1,odds2,dobles=dobles,timestamp=unix_timestamp))
				
				else:
					j1=parsear_juagador(j1)
					j2=parsear_juagador(j2)

					self.DATA.append(Dato(Equipo(j1),Equipo(j2),odds1,odds2,dobles=dobles,timestamp=unix_timestamp))
			except Exception as e:
				try:
					logger.warning("No se ha podido parsear: "+str(e)+" J1: "+str(j1)+" original: "+str(e1['name']['value'])+" J2: "+str(j2)+" original: "+str(e2['name']['value'])+" line: "+str(e.__traceback__.tb_lineno))
				except:
					logger.warning("No se ha podido parsear un partido: "+str(e)+" line: "+str(e.__traceback__.tb_lineno))
				pass


			
			#print(j1,"vs",j2,odds1,odds2)





if __name__=='__main__':
	b=Bwin()
	b.buscar_partidos()
	b.guardar_html()
	b.guardar_data_en_json()
	b.print()





