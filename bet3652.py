import requests # https://pypi.org/project/requests/
#from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import re
from fractions import Fraction
import random

class Bet365():
	def __init__(self):
		self.s=requests.Session()
		self.DATA=[]

		self.cookies = {
				'pstk': 'AD488D7CFABAABEAA803000E04845AAF000003',
				'rmbs': '3',
				'aps03': 'cf=N^&cg=4^&cst=0^&ct=171^&hd=N^&lng=3^&oty=2^&tzi=4',
		}

		self.headers = {
			'Connection': 'keep-alive',
			'sec-ch-ua': '^\\^Google',
			'sec-ch-ua-mobile': '?0',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
			'Accept': '*/*',
			'Sec-Fetch-Site': 'same-origin',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Dest': 'empty',
			'Referer': 'https://www.bet365.es/',
			'Accept-Language': 'es-ES,es;q=0.9',
		}

		self.params = (
				('lid', '3^'),
				('zid', '0^'),
				('pd', '^%^23AS^%^23B13^%^23^'),
				('cid', '171^'),
				('ctid', '171'),
		)
		# https://www.bet365.es/SportsBook.API/web?lid=3&zid=0&pd=%23AS%23B13%23&cid=171&ctid=171
		#response = requests.get('https://www.bet365.es/SportsBook.API/web', headers=headers, params=params, cookies=cookies)

	
	def parsear_partidos(self):
		self.texto=self.r.text
		

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

	def buscar_partidos(self):
		self.headers_list=[]
		# Headers chrome portatil
		headers = {
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'es-ES,es;q=0.9',
		}
		self.headers_list.append(headers)
		
		# Headers mozilla portatil
		headers = {
			'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
			'DNT': '1',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
		}
		self.headers_list.append(headers)


		self.r = requests.get('https://www.bet365.es/SportsBook.API/web?lid=3&zid=0&pd=%23AS%23B13%23&cid=171&ctid=171', headers=self.headers_list[random.randint(0,1)])
		if self.r.status_code==200:
			self.texto=self.r.text
		else:
			print("ERROR: response code:",self.r.status_code)

	def print(self):
		print("\nBet365:",len(self.DATA),"partidos\n")
		for partido in self.DATA:
			print(partido)

if __name__=='__main__':
	b=Bet365()
	#b.buscar_partidos()
	#b.print()