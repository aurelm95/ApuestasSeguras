#Betstars

import requests
import time
from fractions import Fraction


class Betstars():
	def __init__(self):
		self.s=requests.Session()
		r=self.s.get("https://www.betstars.es/?no_redirect=1#/tennis/daily")

	def buscar_partidos(self):
		# La variable take indica el numero de partidos que quiero en la respuesta
		# La variable skip indice el numero de partidos que quiero saltarme
		# La variable date tiene que ser de la forma yyyy-mm-dd
		# Para la conversion de 1 a 01:
		# https://stackoverflow.com/questions/26849541/pythonic-formatting-from-1-to-01
		self.take=30
		self.skip=0
		t=time.gmtime()
		self.date=str(t.tm_year)+'-'+str("%02d" % t.tm_mon)+'-'+str("%02d" % t.tm_mday)
		self.r=self.s.get("https://sports.betstars.es/sportsbook/v1/api/getEventsForDay?sport=TENNIS&date="+self.date+"&skip="+str(self.skip)+"&take="+str(self.take)+"&utcOffset=1&locale=es-es&channelId=6&siteId=1024")

		# La respuesta es un diccionario que con la declaracion de las variales false y true puede ser interpretado por python
		false=False
		true=True
		exec('self.l='+self.r.text)
		
		self.DATA=[]
		for p in self.l:
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
			self.DATA.append([nombre,Fraction(odds[0]),Fraction(odds[1])])

	def print(self):
		for p in self.DATA:
			print(p[0][0],"vs",p[0][1],p[1],p[2])


if __name__=='__main__':
	b=Betstars()
	b.buscar_partidos()
	b.print()

