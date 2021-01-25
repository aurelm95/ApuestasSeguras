#Betstars

import requests
import time
from fractions import Fraction

from nuevos.data_classes import Dato

class Betstars():
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
		self.r=self.s.get("https://sports.pokerstarssports.es/sportsbook/v1/api/getCompetitionsForDay?sport=TENNIS&date="+self.date+"&count="+str(self.count)+"&utcOffset=1&locale=es-es&channelId=18&siteId=1024")

		# La respuesta es un diccionario que con la declaracion de las variales false y true puede ser interpretado por python
		self.j=self.r.json()
		for torneo in self.j:
			for p in torneo['event']:
				e1=p['participants']['participant'][0]['names']['longName']
				e2=p['participants']['participant'][1]['names']['longName']
				odds1=p['markets'][0]['selection'][1]['odds']['frac']
				odds2=p['markets'][0]['selection'][0]['odds']['frac']
				odds=[odds1,odds2]
				# Miramos si son dobles
				doble=e1.find(' & ')
				if doble>0:
					j1e1=e1[:doble]
					j2e1=e1[doble+3:-1]
					e1=[j1e1.split(' '),j2e1.split(' ')]

					doble=e2.find(' & ')
					j1e2=e2[:doble]
					j2e2=e2[doble+3:-1]
					e2=[j1e2.split(' '),j2e2.split(' ')]
					
					nombre=[e1,e2]
				else:
					nombre=[e1.split(' '),e2.split(' ')]
				d=Dato(e1,e2,Fraction(odds[0]),Fraction(odds[1]),dobles=bool(doble))
				self.DATA.append(d)

	def guardar_html(self):
		f=open('API/htmls/'+self.nombre+'.html','w')
		f.write(self.r.text)
		f.close()

	def print(self):
		for p in self.DATA:
			print(p)


if __name__=='__main__':
	b=Betstars()
	b.buscar_partidos()
	b.print()

