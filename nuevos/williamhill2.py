import requests
from bs4 import BeautifulSoup
from fractions import Fraction

from data_classes import Dato


class Williamhill():
	def __init__(self):
		self.s=requests.Session()	
		self.DATA=[]	

	def buscar_partidos(self):
		self.respuesta=self.s.get("https://sports.williamhill.es/betting/es-es/tenis/partidos/competici%C3%B3n/hoy")
		if self.respuesta.status_code!=200:
			print("Williamhill: ERROR: Response Code:",self.respuesta.status_code)
			return 0
		self.soup=BeautifulSoup(self.respuesta.text,'html.parser')

		# eventos es una lista con cadauno de "los partidos"
		self.eventos=self.soup.find_all('div',{'class':'event'})
		for e in self.eventos:
			nombres=e.find('a').find_all('span')
			n1=nombres[0].text
			n2=nombres[1].text
			dobles=True if '/' in n1 else False
			b=e.find_all('button')
			precio1=Fraction(b[0].text)
			precio2=Fraction(b[1].text)
			self.DATA.append(Dato(n1,n2,precio1,precio2,dobles=dobles))

	def print(self):
		print("\nWilliamHill:",len(self.DATA),"partidos\n")
		for partido in self.DATA:
			print(partido)	
		
if __name__=='__main__':
	w=Williamhill()
	w.buscar_partidos2()
	w.print()	
