import requests
from bs4 import BeautifulSoup
from fractions import Fraction


class Williamhill():
	def __init__(self):
		self.s=requests.Session()
		

	def buscar_partidos(self):
		self.respuesta=self.s.get("http://sports.williamhill.es/bet_esp/es/betting/y/17/mh/Tenis.html")
		self.soup=BeautifulSoup(self.respuesta.text,'html.parser')
		self.DATA=[]

		#Partidos jugandose actualmente
		'''print("\nPartidos jugandose actualmente:\n")
		filas=self.soup.find_all("tr",{'class':'rowLive'})
		for fila in filas:
			jugadores=fila.find('td',{'class':'CentrePad'}).text
			precio1, precio2=fila.find_all('div',{'class':'eventpriceholder-left'})
			precio1=precio1.text.replace('\t','').replace('\n','')
			precio2=precio2.text.replace('\t','').replace('\n','')
			print([jugadores, precio1, precio2])
			#print(jugadores)'''

		#Partidos futuros
		lista=self.soup.find_all('tr',{'class':'rowOdd'})
		for item in lista:
			if item.has_attr('id') and not item.has_attr('style'):
				try:
					nombre=item.find('td',{'class':'CentrePad'}).text.replace('\t','').replace('\n','').replace(u'\xa0', u' ').replace(' ₋ ','-')
					precio1, precio2=item.find_all('div',{'class':'eventpriceholder-left'})
					precio1=Fraction(precio1.text.replace('\t','').replace('\n',''))
					precio2=Fraction(precio2.text.replace('\t','').replace('\n',''))
					self.DATA.append([nombre, precio1, precio2])
				except:
					pass

	def print(self):
		print("\nWilliamHill:",len(self.DATA),"partidos\n")
		for partido in self.DATA:
			print(partido)	
		
	
