#Betstars

import requests
import time
from fractions import Fraction
from datetime import datetime

from .utils.data_classes import Dato, Jugador, Equipo, CasaDeApuestas
from .utils.logger import apuestas_logger as logger

class Betstars(CasaDeApuestas):
	def __init__(self):
		self.s=requests.Session()
		self.nombre='betstars'
		CasaDeApuestas.__init__(self,self.nombre)
		self.DATA=[]

	def buscar_partidos(self):
		self.DATA=[]
		r=self.s.get("https://www.betstars.es/?no_redirect=1#/tennis/daily")
		# La variable count indica el numero de partidos que quiero en la respuesta
		# La variable date tiene que ser de la forma yyyy-mm-dd
		# Para la conversion de 1 a 01:
		# https://stackoverflow.com/questions/26849541/pythonic-formatting-from-1-to-01
		self.count=30
		t=time.gmtime()
		self.date=str(t.tm_year)+'-'+str("%02d" % t.tm_mon)+'-'+str("%02d" % t.tm_mday)
		self.url="https://sports.pokerstarssports.es/sportsbook/v1/api/getCompetitionsForDay?sport=TENNIS&date="+self.date+"&count="+str(self.count)+"&utcOffset=1&locale=es-es&channelId=18&siteId=1024"
		self.respuesta=self.s.get(self.url)

		self.j=self.respuesta.json()
		for torneo in self.j:
			for p in torneo['event']:
				try:
					e1=p['participants']['participant'][0]['names']['longName']
					e2=p['participants']['participant'][1]['names']['longName']

					odds1=None
					odds2=None

					for mercado in p['markets']:
						if mercado['name']=='Ganador del partido':
							logger.debug("Torneo: "+str(self.j.index(torneo))+" Evento: "+str(torneo['event'].index(p))+" Odds encontradas")
							if mercado['selection'][0]['name']==p['participants']['participant'][0]['name']:
								odds1=mercado['selection'][0]['odds']['frac']
								odds2=mercado['selection'][1]['odds']['frac']
							else:
								odds1=mercado['selection'][1]['odds']['frac']
								odds2=mercado['selection'][0]['odds']['frac']
							break
					
					assert odds1 is not None and odds2 is not None

					# Miramos si son dobles
					doble=True if ' / ' in e1 else False
					if doble:
						e1j1,e1j2=e1.split(' / ')
						e1n1,e1a1=e1j1.strip().rsplit(' ',1)
						e1n2,e1a2=e1j2.strip().rsplit(' ',1)

						e1=Equipo(
							Jugador(inicial_nombre=e1n1,apellido=e1a1) if len(e1j1)==1 else Jugador(nombre=e1n1,apellido=e1a1),
							Jugador(inicial_nombre=e1n2,apellido=e1a2) if len(e1j2)==1 else Jugador(nombre=e1n2,apellido=e1a2)
						)

						e2j1,e2j2=e2.split(' / ')
						e2n1,e2a1=e2j1.strip().rsplit(' ',1)
						e2n2,e2a2=e2j2.strip().rsplit(' ',1)
						e2=Equipo(
							Jugador(inicial_nombre=e2n1,apellido=e2a1) if len(e2j1)==1 else Jugador(nombre=e2n1,apellido=e2a1),
							Jugador(inicial_nombre=e2n2,apellido=e2a2) if len(e2j2)==1 else Jugador(nombre=e2n2,apellido=e2a2)
						)
					else:
						e1n1,e1a1=e1.rsplit(' ',1)
						e1=Equipo(Jugador(nombre=e1n1,apellido=e1a1))

						e2n1,e2a1=e2.rsplit(' ',1)
						e2=Equipo(Jugador(nombre=e2n1,apellido=e2a1))

					unix_timestamp=None	
					try:
						unix_timestamp=int(p['eventTime'])//1000
					except Exception as e:
						logger.warning("No se ha podido parsear la fecha: "+str(e))

					d=Dato(e1,e2,Fraction(odds1)+1,Fraction(odds2)+1,dobles=doble,timestamp=unix_timestamp) # les sumo 1 a las odds
					self.DATA.append(d)
				except KeyError as e:
					logger.warning("Torneo: "+str(self.j.index(torneo))+" Evento: "+str(torneo['event'].index(p))+" KeyError: "+str(e)+" line: "+str(e.__traceback__.tb_lineno))
					# logger.exception(":(")
				except Exception as e:
					logger.warning("e1: "+str(e1)+" e2: "+str(e2)+" dobles: "+str(doble)+" ERROR: "+str(e)+" line: "+str(e.__traceback__.tb_lineno))
					pass


if __name__=='__main__':
	b=Betstars()
	b.buscar_partidos()
	b.guardar_html()
	b.guardar_data_en_json()
	b.print()

