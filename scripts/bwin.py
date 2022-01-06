#bwin
import requests
from fractions import Fraction

from data_classes import Dato, Jugador, Equipo, CasaDeApuestas

class Bwin(CasaDeApuestas):
	def __init__(self):
		# https://curl.trillworks.com/
		# importante el "accept-encoding": "text/html",
		# he tenido que retocarlo manualmente para que me devuelva
		# la respuesta bien codificada
		self.s=requests.Session()
		self.nombre="bwin"
		self.DATA=[]
		self.headers = {
		    'origin': 'https://sports.m.bwin.es',
		    "accept-encoding": "text/html",
		    'accept-language': 'es-ES,es;q=0.9',
		    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
		    'content-type': 'application/json',
		    'accept': 'application/json, text/plain, */*',
		    'cache-control': 'no-cache',
		    'authority': 'cds-api.bwin.es',
		    'x-bwin-browser-url': 'https://sports.m.bwin.es/es/sports/tenis-5',
		    'referer': 'https://sports.m.bwin.es/es/sports/tenis-5',
		}

		self.params = (
		    ('x-bwin-accessid', 'OTdhMjU3MWQtYzI5Yi00NWQ5LWFmOGEtNmFhOTJjMWVhNmRl'),
		    ('lang', 'es'),
		    ('country', 'ES'),
		    ('userCountry', 'ES'),
		)

		self.data = '{"sportIds":"5","fixtureCategories":"Gridable,NonGridable,Other","offerMapping":"Filtered","offerCategories":"Gridable,Other","scoreboardMode":"Slim","marqueeRequest":{"marqueeData":[],"take":8},"fixtureTypes":"Standard"}'

	def buscar_partidos(self):
		self.respuesta = self.s.post('https://cds-api.bwin.es/bettingoffer/lobby/sport', headers=self.headers, params=self.params, data=self.data)
		self.j=self.respuesta.json()
		
		for p in self.j['highlights']:
			e1=p['games'][0]['results'][0]
			# Note that due to the usual issues with binary floating-point (see Floating Point Arithmetic: Issues and Limitations), the argument to Fraction(1.1) is not exactly equal to 11/10, and so Fraction(1.1) does not return Fraction(11, 10) as one might expect.
			# https://docs.python.org/2/library/fractions.html
			# He hecho una chapucilla
			odds1=Fraction(int(e1['odds']*100))/100
			j1=e1['name']['value']
			e2=p['games'][0]['results'][1]
			odds2=Fraction(int(e2['odds']*100))/100
			j2=e2['name']['value']
			dobles=True if '/' in j1 else False
			try:
				if dobles:
					e1j1,e1j2=j1.split('/')

					e1n1,e1a1=e1j1.split('. ')
					e1j1=Jugador(inicial_nombre=e1n1,apellido=e1a1)

					e1n2,e1a2=e1j2.split('. ')
					e1j2=Jugador(inicial_nombre=e1n2,apellido=e1a2)

					e2j1,e2j2=j2.split('/')

					e2n1,e2a1=e2j1.split('. ')
					e2j1=Jugador(inicial_nombre=e2n1,apellido=e2a1)

					e2n2,e2a2=e2j2.split('. ')
					e2j2=Jugador(inicial_nombre=e2n2,apellido=e2a2)

					self.DATA.append(Dato(Equipo(e1j1,e1j2),Equipo(e2j1,e2j2),odds1,odds2,dobles=dobles))
				
				else:
					# print("singles: j1:",j1,"j2:",j2)
					n1,a1=j1.split('. ')
					j1=Jugador(inicial_nombre=n1,apellido=a1)

					n2,a2=j2.split('. ')
					j2=Jugador(inicial_nombre=n2,apellido=a2)

					self.DATA.append(Dato(Equipo(j1),Equipo(j2),odds1,odds2,dobles=dobles))
			except Exception as e:
				print("\tERROR:",e)
				pass


			
			#print(j1,"vs",j2,odds1,odds2)





if __name__=='__main__':
	b=Bwin()
	b.buscar_partidos()
	b.guardar_html()
	b.guardar_data_en_json()
	b.print()




