import os
import time
import json
from fractions import Fraction

from .logger import apuestas_logger as logger

class CasaDeApuestas():
	def __init__(self):
		self.nombre=None
		self.DATA=[]
		self.respuesta=None

	def guardar_html(self):
		logger.debug("html de "+self.nombre+" guardado en /htmls")
		htmls_folder_path=os.path.dirname(__file__)+'/htmls/'
		if not os.path.exists(htmls_folder_path):
			os.mkdir(htmls_folder_path)
			logger.debug("Creando carpeta: "+htmls_folder_path)
		f=open(htmls_folder_path+self.nombre+'.html','w', encoding="utf-8")
		f.write(self.respuesta.text)
		f.close()
	
	def cargar_html(self):
		logger.info("Cargando html para "+self.nombre)
		f=open(os.path.dirname(__file__)+'/htmls/'+self.nombre+'.html','r', encoding="utf-8")
		self.respuesta_text=f.read()
		f.close()

	def guardar_data_en_json(self):
		self.j={'timestamp':time.time(),'web':self.nombre}
		self.j['DATA']=[dato.to_dict() for dato in self.DATA]
		jsons_folder_path=os.path.dirname(__file__)+'/jsons/'
		if not os.path.exists(jsons_folder_path):
			os.mkdir(jsons_folder_path)
			logger.debug("Creando carpeta: "+jsons_folder_path)
		f=open(jsons_folder_path+self.nombre+'.json','w')
		json.dump(self.j,f)
		f.close()
	
	def cargar_data_de_json(self):
		f=open(os.path.dirname(__file__)+'/jsons/'+self.nombre+".json","r")
		j=json.load(f)
		f.close()
		for d in j['DATA']:
			if d['e1']['j2'] is None:
				self.DATA.append(Dato(
					Equipo(Jugador(
						nombre=d['e1']['j1']['nombre'],
						apellido=d['e1']['j1']['apellido'],
						inicial_nombre=d['e1']['j1']['inicial_nombre'],
						inicial_apellido=d['e1']['j1']['inicial_apellido']
						)),
					Equipo(Jugador(
						nombre=d['e2']['j1']['nombre'],
						apellido=d['e2']['j1']['apellido'],
						inicial_nombre=d['e2']['j1']['inicial_nombre'],
						inicial_apellido=d['e2']['j1']['inicial_apellido']
						)),
					odds1=Fraction(d['odds1']['numerator'],d['odds1']['denominator']),
					odds2=Fraction(d['odds2']['numerator'],d['odds2']['denominator']),
					dobles=d['dobles']
				))
			else:
				self.DATA.append(Dato(
					Equipo(
						Jugador(
							nombre=d['e1']['j1']['nombre'],
							apellido=d['e1']['j1']['apellido'],
							inicial_nombre=d['e1']['j1']['inicial_nombre'],
							inicial_apellido=d['e1']['j1']['inicial_apellido']
							),
						Jugador(
							nombre=d['e1']['j2']['nombre'],
							apellido=d['e1']['j2']['apellido'],
							inicial_nombre=d['e1']['j2']['inicial_nombre'],
							inicial_apellido=d['e1']['j2']['inicial_apellido']
							)	
						),
					Equipo(
						Jugador(
							nombre=d['e2']['j1']['nombre'],
							apellido=d['e2']['j1']['apellido'],
							inicial_nombre=d['e2']['j1']['inicial_nombre'],
							inicial_apellido=d['e2']['j1']['inicial_apellido']
							),
						Jugador(
							nombre=d['e2']['j2']['nombre'],
							apellido=d['e2']['j2']['apellido'],
							inicial_nombre=d['e2']['j2']['inicial_nombre'],
							inicial_apellido=d['e2']['j2']['inicial_apellido']
							)
						),
					odds1=Fraction(d['odds1']['numerator'],d['odds1']['denominator']),
					odds2=Fraction(d['odds2']['numerator'],d['odds2']['denominator']),
					dobles=d['dobles']
				))
		logger.debug(str(len(self.DATA))+" datos cargados para "+self.nombre)

	def print(self):
		print("\n"+self.nombre+":",len(self.DATA),"partidos\n")
		for partido in self.DATA:
			print(partido)

class Jugador():
	def __init__(self,apellido,nombre=None,inicial_nombre=None,inicial_apellido=None):
		self.nombre=nombre
		self.apellido=apellido
		self.inicial_nombre=inicial_nombre
		self.inicial_apellido=inicial_apellido
	
	def to_dict(self):
		return {'nombre':self.nombre,'apellido':self.apellido,'inicial_nombre':self.inicial_nombre,'inicial_apellido':self.inicial_apellido}
	
	def __repr__(self):
		if self.nombre is not None:
			return self.nombre+' '+self.apellido
		if self.inicial_nombre is not None:
			return self.inicial_nombre+' '+self.apellido
		return self.apellido
	
	def __eq__(self, other):
		if self.apellido.lower() in other.apellido.lower() or other.apellido.lower() in self.apellido.lower():
			if self.nombre==other.nombre:
				return True
			if self.inicial_nombre is not None and other.inicial_nombre is not None:			
				if self.inicial_nombre.lower()==other.inicial_nombre.lower():
					return True
			if self.inicial_nombre is not None and other.nombre is not None:
				if self.inicial_nombre.lower()==other.nombre[0].lower():
					return True
			if self.nombre is not None and other.inicial_nombre is not None:
				if self.nombre[0].lower()==other.inicial_nombre.lower():
					return True
			if (self.inicial_nombre is None and self.nombre is None) or (other.inicial_nombre is None and other.nombre is None):
				return True
			if self.nombre is not None and other.nombre is not None:
				if self.nombre.lower() in other.nombre.lower() or other.nombre.lower() in self.nombre.lower():
					logger.warning("Jugador: "+str(self)+" y Jugador: "+str(other)+" han coincidido por inclusion de nombres")
					return True
				if self.nombre.replace(" ","").lower()==other.nombre.replace(" ","").lower():
					logger.warning("Jugador: "+str(self)+" y Jugador: "+str(other)+" han coincidido por omision de espacios en los nombres")
					return True
				
		return False

class Equipo():
	def __init__(self,j1,j2=None):
		self.j1=j1
		self.j2=j2
		self.dobles=True if j2 is not None else False
	
	def to_dict(self):
		if not self.dobles:
			return {'j1':self.j1.to_dict(),'j2':None}
		return {'j1':self.j1.to_dict(),'j2':self.j2.to_dict()}
	
	def __repr__(self):
		if not self.dobles:
			return self.j1.__repr__()
		return self.j1.__repr__()+'/'+self.j2.__repr__()

	def __eq__(self, other):
		if self.dobles:
			if not other.dobles:
				return False
			return self.j1==other.j1 and self.j2==other.j2
		return self.j1==other.j1

class Dato():
	def __init__(self,e1,e2,odds1,odds2,dobles=False,timestamp=None):
		self.e1=e1
		self.e2=e2
		self.odds1=odds1
		self.odds2=odds2
		self.dobles=dobles
		self.timestamp=timestamp

	def reverse(self):
		return Dato(self.e2,self.e1,self.odds2,self.odds1,dobles=self.dobles)
	
	def to_dict(self):
		return {'e1':self.e1.to_dict(),'e2':self.e2.to_dict(),'odds1':{'numerator':self.odds1.numerator,'denominator':self.odds1.denominator},'odds2':{'numerator':self.odds2.numerator,'denominator':self.odds2.denominator},'dobles':self.dobles}

	def __repr__(self):
		if not self.dobles:
			return str(self.e1)+' vs '+str(self.e2)+' | '+str(self.odds1)+' - '+str(self.odds2)
		return str(self.e1)+' vs '+str(self.e2)+' | '+str(self.odds1)+' - '+str(self.odds2)

class Evento():
	def __init__(self,dato,web):
		# Datos generales del evento
		self.e1=dato.e1
		self.e2=dato.e2
		self.dobles=dato.dobles
		self.timestamp=dato.timestamp

		# Datos sobre la seguridad de la apuesta del evento
		self.segura=False
		self.web_apuesta_segura1=None
		self.web_apuesta_segura2=None
		self.apuesta_a_web1=None
		self.apuesta_a_web1=None
		self.esperanza=0
		self.ganancia_minima_asegurada=0

		# Los guardo como unas odds de la web
		self.odds={web:[dato.odds1,dato.odds2]}
	
	def nuevas_odds(self,dato,web):
		self.odds[web]=[dato.odds1,dato.odds2]

	def comprobar_apuesta_segura(self):
		for web1 in list(self.odds.keys()):
			for web2 in list(self.odds.keys()):
				if web1==web2: continue # asumo que nunca pasara
				esperanza=float((self.odds[web1][0]-1)*(self.odds[web2][1]-1)) # Paso de Fraction a float
				# self.esperanza=max(self.esperanza,float(esperanza))
				if esperanza>self.esperanza:
					self.esperanza=esperanza
					self.web_apuesta_segura1=web1
					self.web_apuesta_segura2=web2
		if self.esperanza>1:
			self.segura=True
			"""
			Sea x lo que voy a apostar en la casa1 (y por lo tanto apostare 1-x en la casa2)
			Digamos que a:=odds[web_apuesta_segura1][0] y b:=odds[web_apuesta_segura2][1]
			
			mi beneficio netos será o bien x*a-1 o bien (1-x)*b-1. Como estos beneficios (rectas)
			tienen un crecimiento opuesto con respecto de x, con tal de maximizar las ganancias
			(es decir maximizar min(x*a-1,(1-x)*b-1) ) tengo que resolver x*a-1=(1-x)*b-1.

			x=b/(a+b)  por lo tanto  y=a/(a+b)
			"""
			a=self.odds[self.web_apuesta_segura1][0]
			b=self.odds[self.web_apuesta_segura2][1]

			self.apuesta_a_web1=b/(a+b)
			self.apuesta_a_web2=a/(a+b)
			self.ganancia_minima_asegurada=self.apuesta_a_web1*a-1

			conclusion="Apostando "
			conclusion+=str(self.apuesta_a_web1)+" en la web "+self.web_apuesta_segura1+" por "+str(self.e1)
			conclusion+=" y "
			conclusion+=str(self.apuesta_a_web2)+" en la web "+self.web_apuesta_segura2+" por "+str(self.e2)
			conclusion+=" gano asegurados: "+str(self.ganancia_minima_asegurada)+"="+str(float(self.ganancia_minima_asegurada))

			if not self.apuesta_a_web1*a-1==self.apuesta_a_web2*b-1:
				logger.error("El calculo de: "+conclusion+" no cuadra")

			logger.info(conclusion)



	def nuevo_dato(self,dato,web):
		if self.e1==dato.e1 and self.e2==dato.e2:
			self.odds[web]=[dato.odds1,dato.odds2]
			return True
		if self.e1==dato.e2 and self.e2==dato.e1:
			self.odds[web]=[dato.odds2,dato.odds1]
			return True
		return False

	def to_dict(self):
		j={'e1':self.e1.to_dict(),'e2':self.e2.to_dict()}
		odds={}
		for web in list(self.odds.keys()):
			odds[web]={
				'odds1':{'numerator':self.odds[web][0].numerator,'denominator':self.odds[web][0].denominator},
				'odds2':{'numerator':self.odds[web][1].numerator,'denominator':self.odds[web][1].denominator}
			}
		# j|={'odds':odds,'dobles:':self.dobles,'segura':self.segura}
		j.update({'odds':odds,'dobles:':self.dobles,'segura':self.segura})
		j['esperanza']=self.esperanza
		return j

	def __repr__(self):
		return str(self.e1)+' vs '+str(self.e2)+' | '+str(self.odds)+' || '+str(self.esperanza) 
		