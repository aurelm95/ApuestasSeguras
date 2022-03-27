import requests 
from bs4 import BeautifulSoup
from fractions import Fraction

from .utils.data_classes import Dato, Jugador, Equipo, CasaDeApuestas
from .utils.logger import apuestas_logger as logger

class Betfair(CasaDeApuestas):
	def __init__(self):
		self.s=requests.Session()
		self.nombre='betfair'
		CasaDeApuestas.__init__(self,self.nombre)
		self.DATA=[]
	
	def buscar_partidos(self):
		self.DATA=[]
		self.url="https://www.betfair.es/sport/tennis"
		self.respuesta=self.s.get(self.url)
		# https://www.betstars.es/?no_redirect=1#/tennis/daily
		# https://sports.m.bwin.es/es/sports/tenis-5
		#print(respuesta.text)

		self.soup=BeautifulSoup(self.respuesta.text,'html.parser')
		#partidos=soup.find_all('a',{'class':'ui-nav event-team-container ui-top event-link ui-gtm-click'})
		#partidos[0]['data-galabel']

		self.partidos=self.soup.find_all('li',{'class':'com-coupon-line-new-layout betbutton-layout avb-row avb-table market-avb set-template market-1-columns'})
		#print("hay ",len(self.partidos)," partidos")
		for partido in self.partidos:
			# Esta web dara problemas porque muchas veces solo pone los apellidos
			# Los partidos pueden ser variaciones de las dos siguientes formas:
			#J Delaney / E Vanshelboim v K Onishi / S Sekiguchi
			#Goffin - Albot
			#Pervolarakis v F Auger-Aliassime
			#Soeda - M Cuevas
			#Nishioka - P Cuevas
			try:
				nombre1,nombre2=partido.find_all('span',{'class':'team-name'})
				nombre1=nombre1['title']
				nombre2=nombre2['title']
				p1=partido.find('li',{'class':'selection sel-0'}).find('span').text.replace('\n','')
				p2=partido.find('li',{'class':'selection sel-1'}).find('span').text.replace('\n','')
				if p1==' ' or p1=='\xa0' or p2==' ' or p2=='\xa0':
					logger.debug("Un partido no tenia datos de sus odds")
					continue
				p1=Fraction(p1)
				p2=Fraction(p2)

				def parsear_jugador(s):
					s=s.strip() # Para quitar el espacio que hay entre el apellido y la barra / y el espacio que hay entre la barra / y el nombre en el caso de los dobles
					if ' ' in s:
						nombre,apellido=s.rsplit(' ',1)
						if len(nombre)==1:
							return Jugador(inicial_nombre=nombre,apellido=apellido,web=self.nombre)
						return Jugador(nombre=nombre,apellido=apellido,web=self.nombre)
					return Jugador(apellido=s,web=self.nombre)

				dobles=True if '/' in nombre1 else False
				# print("\tnombre1",nombre1,"nombre2:",nombre2,"dobles:",dobles)
				if dobles:
					e1j1,e1j2=nombre1.split('/')
					e2j1,e2j2=nombre2.split('/')

					e1j1=parsear_jugador(e1j1)
					e1j2=parsear_jugador(e1j2)
					e2j1=parsear_jugador(e2j1)
					e2j2=parsear_jugador(e2j2)
				
					if e1j2.apellido=='': logger.debug("nombre del equipo1: "+nombre1+" originales: "+partido.find_all('span',{'class':'team-name'})[0]['title'])
					if e2j2.apellido=='': logger.debug("nombre del equipo2: "+nombre2+" originales: "+partido.find_all('span',{'class':'team-name'})[1]['title'])
					self.DATA.append(Dato(Equipo(e1j1,e1j2),Equipo(e2j1,e2j2),p1,p2,dobles=dobles))

				else:
					j1=parsear_jugador(nombre1)
					j2=parsear_jugador(nombre2)

					self.DATA.append(Dato(Equipo(j1),Equipo(j2),p1,p2,dobles=dobles))
			except ValueError as e:
				if 'Fraction' in e.__repr__():
					logger.warning("Una de las fracciones de se ha podido leer: "+partido.find('li',{'class':'selection sel-0'}).find('span').text.replace('\n','')+" "+partido.find('li',{'class':'selection sel-1'}).find('span').text.replace('\n','')+" line: "+str(e.__traceback__.tb_lineno))
				else:
					logger.warning("Los nombres de los jugadores no han podido parsearse bien: "+str(e)+" nombre1: "+str(nombre1)+" nombre2: "+str(nombre2)+" line: "+str(e.__traceback__.tb_lineno))
			except Exception as e:
				logger.warning("Un partido no se ha podido parsear bien: "+str(e)+" line: "+str(e.__traceback__.tb_lineno))

if __name__=='__main__':
	b=Betfair()
	b.cargar_data_de_json()
	# b.buscar_partidos()
	# b.guardar_html()
	# b.guardar_data_en_json()
	b.print()
