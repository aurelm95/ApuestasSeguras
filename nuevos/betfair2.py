import requests 
from bs4 import BeautifulSoup
from fractions import Fraction

from data_classes import Dato

class Betfair():
	def __init__(self):
		self.s=requests.Session()
	
	def buscar_partidos(self):
		self.respuesta=self.s.get("https://www.betfair.es/sport/tennis")
		# https://www.betstars.es/?no_redirect=1#/tennis/daily
		# https://sports.m.bwin.es/es/sports/tenis-5
		#print(respuesta.text)

		self.soup=BeautifulSoup(self.respuesta.text,'html.parser')
		#partidos=soup.find_all('a',{'class':'ui-nav event-team-container ui-top event-link ui-gtm-click'})
		#partidos[0]['data-galabel']

		self.partidos=self.soup.find_all('li',{'class':'com-coupon-line-new-layout betbutton-layout avb-row avb-table market-avb set-template market-1-columns'})
		#print("hay ",len(self.partidos)," partidos")
		self.DATA=[]
		for partido in self.partidos:
			# Esta web dara problemas porque muchas veces solo pone los apellidos
			# Los partidos pueden ser variaciones de las dos siguientes formas:
			#J Delaney / E Vanshelboim v K Onishi / S Sekiguchi
			#Goffin - Albot
			#Pervolarakis v F Auger-Aliassime
			#Soeda - M Cuevas
			#Nishioka - P Cuevas
			
			nombre1,nombre2=partido.find_all('span',{'class':'team-name'})
			nombre1=nombre1['title']
			nombre2=nombre2['title']
			p1=Fraction(partido.find('li',{'class':'selection sel-0'}).find('span').text.replace('\n',''))
			p2=Fraction(partido.find('li',{'class':'selection sel-1'}).find('span').text.replace('\n',''))

			dobles=False
			if ' / ' in nombre1:
				dobles=True
				nombre1=nombre1.split(' / ')
				nombre2=nombre2.split(' / ')

			self.DATA.append(Dato(nombre1,nombre2,p1,p2,dobles=dobles))


	def print(self):
		print("hay ",len(self.partidos)," partidos")
		for partido in self.DATA:
			print(partido)

if __name__=='__main__':
	b=Betfair()
	b.buscar_partidos()
	b.print()
