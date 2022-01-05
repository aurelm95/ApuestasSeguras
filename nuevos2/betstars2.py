#Betstars

import requests
import time
from fractions import Fraction

from data_classes import Dato, Jugador, Equipo, CasaDeApuestas

class Betstars(CasaDeApuestas):
	def __init__(self):
		self.s=requests.Session()
		self.nombre='betstars'
		self.DATA=[]

	def buscar_partidos(self):
		r=self.s.get("https://www.betstars.es/?no_redirect=1#/tennis/daily")
		# La variable count indica el numero de partidos que quiero en la respuesta
		# La variable date tiene que ser de la forma yyyy-mm-dd
		# Para la conversion de 1 a 01:
		# https://stackoverflow.com/questions/26849541/pythonic-formatting-from-1-to-01
		self.count=30
		t=time.gmtime()
		self.date=str(t.tm_year)+'-'+str("%02d" % t.tm_mon)+'-'+str("%02d" % t.tm_mday)
		self.respuesta=self.s.get("https://sports.pokerstarssports.es/sportsbook/v1/api/getCompetitionsForDay?sport=TENNIS&date="+self.date+"&count="+str(self.count)+"&utcOffset=1&locale=es-es&channelId=18&siteId=1024")

		self.j=self.respuesta.json()
		for torneo in self.j:
			for p in torneo['event']:
				try:
					e1=p['participants']['participant'][0]['names']['longName']
					e2=p['participants']['participant'][1]['names']['longName']
					odds1=p['markets'][0]['selection'][1]['odds']['frac']
					odds2=p['markets'][0]['selection'][0]['odds']['frac']
					# Miramos si son dobles
					doble=True if ' / ' in e1 else False
					if doble:
						e1j1,e1j2=e1.split(' / ')
						e1n1,e1a1=e1j1.split(' ')
						e1n2,e1a2=e1j2.split(' ')
						e1=Equipo(
							Jugador(inicial_nombre=e1n1,apellido=e1a1),
							Jugador(inicial_nombre=e1n2,apellido=e1n2)
						)

						e2j1,e2j2=e2.split(' / ')
						e2n1,e2a1=e2j1.split(' ')
						e2n2,e2a2=e2j2.split(' ')
						e1=Equipo(
							Jugador(inicial_nombre=e2n1,apellido=e2a1),
							Jugador(inicial_nombre=e2n2,apellido=e2n2)
						)
					else:
						e1n1,e1a1=e1.split(' ')
						e1=Equipo(Jugador(nombre=e1n1,apellido=e1a1))

						e2n1,e2a1=e2.split(' ')
						e2=Equipo(Jugador(nombre=e2n1,apellido=e2a1))
						
					# print("e1:",e1,"e2:",e2,"dobles:",doble)
					d=Dato(e1,e2,Fraction(odds1),Fraction(odds2),dobles=doble)
					self.DATA.append(d)
				except Exception as e:
					print("e1:",e1,"e2:",e2,"dobles:",doble)
					print(e)
					pass


if __name__=='__main__':
	b=Betstars()
	b.buscar_partidos()
	b.guardar_html()
	b.guardar_data_en_json()
	b.print()

