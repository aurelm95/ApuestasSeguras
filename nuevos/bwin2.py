#bwin
import requests
from fractions import Fraction

from nuevos.data_classes import Dato

class Bwin():
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
		self.r = self.s.post('https://cds-api.bwin.es/bettingoffer/lobby/sport', headers=self.headers, params=self.params, data=self.data)
		self.j=self.r.json()
		
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
			self.DATA.append(Dato(j1,j2,odds1,odds2,dobles=dobles))
			#print(j1,"vs",j2,odds1,odds2)

	def guardar_html(self):
		f=open('API/htmls/'+self.nombre+'.html','w')
		f.write(self.r.text)
		f.close()

	def print(self):
		for p in self.DATA:
			print(p)



if __name__=='__main__':
	b=Bwin()
	b.buscar_partidos()
	b.print()





