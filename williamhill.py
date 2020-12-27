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
					e1,e2=nombre.split('  -  ')
					dobles=e1.find('/')
					if dobles>1:
						j1e1,j2e1=e1.split('/')
						j1e2,j2e2=e2.split('/')
						e1=[j1e1.split(' '),j2e1.split(' ')]
						e2=[j1e2.split(' '),j2e2.split(' ')]
						nombre=[e1,e2]
					else:
						nombre=[e1.split(' '),e2.split(' ')]
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
		
if __name__=='__main__':
	w=Williamhill()
	w.buscar_partidos()
	w.print()	
