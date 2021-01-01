import requests 
from bs4 import BeautifulSoup
from fractions import Fraction

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

		self.partidos=self.soup.find_all('div',{'class':'details-market market-0-runners'})
		#print("hay ",len(self.partidos)," partidos")
		self.DATA=[]
		self.DATA2=[]
		for partido in self.partidos:
			# Esta web dara problemas porque muchas veces solo pone los apellidos
			# Los partidos pueden ser variaciones de las dos siguientes formas:
			#J Delaney / E Vanshelboim v K Onishi / S Sekiguchi
			#Goffin - Albot
			#Pervolarakis v F Auger-Aliassime
			#Soeda - M Cuevas
			#Nishioka - P Cuevas
			
			nombre=partido.find('a')['data-galabel']
			nombre=nombre[:nombre.find('scroller')-1]
			NOMBRE=nombre
			vs=max(nombre.find(' v '),nombre.find(' - '))
			equipo1=nombre[:vs]
			equipo2=nombre[vs+3:]
			# Verificamos si se trata de un 2 vs 2 o un 1 vs 1
			# El metodo find devuelve -1 en caso de no encontrado
			barra1=equipo1.find(' / ')
			if barra1>0:
				n1e1=equipo1[:barra1]
				n2e1=equipo1[barra1+3:]
				equipo1=[n1e1.split(' '),n2e1.split(' ')]

				barra2=equipo2.find(' / ')
				n1e2=equipo2[:barra2]
				n2e2=equipo2[barra2+3:]
				equipo2=[n1e2.split(' '),n2e2.split(' ')]
				
				nombre=[equipo1,equipo2]
			else:
				nombre=[equipo1.split(' '),equipo2.split(' ')]
			#print("He convertido:",NOMBRE,"en:",nombre)
			# A continuacion les restare 1 para pasarlos a ODDs
			try:
				precio1=Fraction(partido.find_all('li')[0].text.replace('\n',''))-1
				precio2=Fraction(partido.find_all('li')[1].text.replace('\n',''))-1
			except:
				print("Betfair(): En el partido:",NOMBRE," no se ha podido leer el precio:")
				print(partido.find_all('li')[0].text.replace('\n',''))
				print(partido.find_all('li')[1].text.replace('\n',''))
			self.DATA.append([nombre,precio1,precio2])
			self.DATA2.append(nombre)

	def print(self):
		print("hay ",len(self.partidos)," partidos")
		for partido in self.DATA:
			print(partido[0],partido[1],partido[2])

if __name__=='__main__':
	b=Betfair()
	b.buscar_partidos()
	b.print()
