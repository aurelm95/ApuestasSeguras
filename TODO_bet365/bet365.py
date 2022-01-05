import requests # https://pypi.org/project/requests/
#from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import re
from fractions import Fraction

class Bet365():
	def __init__(self):
		self.s=requests.Session()
		self.s.headers={
			"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
			"Accept-Encoding":"gzip, deflate, br",
			"Accepts-Language":"es-ES,es;q=0.9",
			"Connection":"keep-alive",
			"Host":"www.bet365.es",
			"Upgrade-Insecure-Requests":"1",
			"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
		}
		r=self.s.get("https://www.bet365.es")
		self.s.headers={
			"Accept":"*/*",
			"Accept-Encoding":"gzip, deflate, br",
			"Accepts-Language":"es-ES,es;q=0.9",
			"Connection":"keep-alive",
			"Cookie":"aps03=ct=171&lng=3",
			"Host":"www.bet365.es",
			"Origin":"https://www.bet365.es",
			"Referer":"https://www.bet365.es/",
			"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
		}
		r=self.s.get("https://www.bet365.es/defaultapi/sports-configuration")
		self.s.headers={
			"Accept":"*/*",
			"Accept-Encoding":"gzip, deflate, br",
			"Accepts-Language":"es-ES,es;q=0.9",
			"Connection":"keep-alive",
			"Cookie":"pstk=0DCF7DF1A2B1E0068CA25418D29084B0000003; rmbs=3; aps03=cf=N&cg=1&cst=0&ct=171&hd=N&lng=3&oty=2&tzi=4",
			"Host":"www.bet365.es",
			"Referer":"https://www.bet365.es/",
			"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
		}
		#r2=self.s.get("https://www.bet365.es/SportsBook.API/web?lid=3&zid=0&pd=%23AO%23B13%23%23V24%23W1%23&cid=171&ctid=171")
		#partidos de tenis con cuota superior a 2 en las proximas 3h y 12h respectivamente:
		#https://www.bet365.es/SportsBook.API/web?lid=3&zid=0&pd=%23AO%23B13%23%23V3%23W1%23&cid=171&ctid=171
		#https://www.bet365.es/SportsBook.API/web?lid=3&zid=0&pd=%23AO%23B13%23%23V12%23W1%23&cid=171&ctid=171
		#https://www.bet365.es/SportsBook.API/web?lid=3&zid=0&pd=%23AO%23B13%23%23V24%23W1%23&cid=171&ctid=171
		#self.texto=r2.text
		#self.DATA=[]
	
	def buscar_partidos(self):
		# Vuelvo a hacer la peticion y limpio los datos anteriores
		self.horas=12
		self.r2=self.s.get("https://www.bet365.es/SportsBook.API/web?lid=3&zid=0&pd=%23AO%23B13%23%23V"+str(self.horas)+"%23W1%23&cid=171&ctid=171")
		self.texto=self.r2.text
		self.DATA=[]

		# Los nombres de los partidos son de la forma:
		# EX=Dougaz/Mansouri v Hemery/Meraut;
		# Hay que buscar desde "EX=" hasta ";"

		# Tambien pueden ser de la forma
		# EX=WTA Limoges - Camila Giorgi v Liudmila Samsonova;
		# Por lo que hay que quitarles el nombre del evento

		# EX=WTA Limoges - Dobles Femeninos - Garcia-Perez/Sorribes Tormo v Pigossi/Zidansek;
		# por lo que hay que cortar hasta el ultimo '-'
		# Para buscar el ultimo caracter en una cadena se usa rfind()

		n=len(re.findall("EX=",self.texto))
		partidos=[]
		for k in range(n):
			comienzo=self.texto.find("EX=")
			final=self.texto.find(";",comienzo)
			nombre=self.texto[comienzo+3:final]
			if '-' in nombre:
				nombre=nombre[nombre.rfind('-')+2:]
			nombre=nombre.replace(' v ','  -  ')
			partidos.append(nombre)
			self.texto=self.texto[final:]
			#print(partidos[k])

		# Ahora hay que buscar los ODDs de las apuestas.
		# Son de la forma: OD=1/2; 
		# Primero se encuentran los ODDs de la pimera columa
		# y luego los de la segunda
		ODDs=[]
		for k in range(2*n):
			comienzo=self.texto.find("OD=")
			final=self.texto.find(";",comienzo)
			string=self.texto[comienzo+3:final]
			# string es de la forma "11/7" hay que pasarlo a float
			'''numerador=string[:string.find('/')]
			denominador=string[string.find('/')+1:]
			ODDs.append(round(1+float(int(numerador)/int(denominador)),2))'''
			ODDs.append(Fraction(string))
			self.texto=self.texto[final:]
			#print(ODDs[k])

		# Finalmente lo guardo todo en la misma lista
		for k in range(n):
			self.DATA.append([partidos[k],ODDs[k],ODDs[k+n]])

	def print(self):
		print("\nBet365:",len(self.DATA),"partidos\n")
		for partido in self.DATA:
			print(partido)

if __name__=='__main__':
	b=Bet365()
	b.buscar_partidos()
	b.print()