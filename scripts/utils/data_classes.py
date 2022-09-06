import os
import time
import json
from fractions import Fraction
import re
import pandas as pd
from datetime import datetime

from .logger import apuestas_logger as logger

class CasaDeApuestas():
	def __init__(self, nombre):
		self.nombre=nombre
		self.DATA=[]
		self.respuesta=None

		# Para guardar/cargar data
		self.htmls_folder_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','data/htmls'))
		self.html_file_path=os.path.join(self.htmls_folder_path,self.nombre+'.html')
		# print(f"{self.htmls_folder_path=}")
		# print(f"{self.html_file_path=}")
		self.jsons_folder_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','data/jsons'))
		self.json_file_path=os.path.join(self.jsons_folder_path,self.nombre+'.json')

	def guardar_html(self):
		if not os.path.exists(self.htmls_folder_path):
			os.mkdir(self.htmls_folder_path)
			logger.info("Creando carpeta: "+self.htmls_folder_path)
		f=open(self.html_file_path,'w', encoding="utf-8")
		f.write(self.respuesta.text)
		f.close()
		logger.info("html de "+self.nombre+" guardado en data/htmls")
	
	def cargar_html(self):
		logger.info("Cargando html para "+self.nombre)
		f=open(self.html_file_path,'r', encoding="utf-8")
		self.respuesta_text=f.read()
		f.close()

	def guardar_data_en_json(self):
		self.j={'timestamp':time.time(),'web':self.nombre}
		self.j['DATA']=[dato.to_dict() for dato in self.DATA]
		if not os.path.exists(self.jsons_folder_path):
			os.mkdir(self.jsons_folder_path)
			logger.info("Creando carpeta: "+self.jsons_folder_path)
		f=open(self.json_file_path,'w')
		json.dump(self.j,f)
		f.close()
		logger.info("json de "+self.nombre+" guardado en data/jsons")
	
	def cargar_data_de_json(self):
		f=open(self.json_file_path,"r")
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
		logger.info(str(len(self.DATA))+" datos cargados para "+self.nombre)

	def print(self):
		print("\n"+self.nombre+":",len(self.DATA),"partidos\n")
		for partido in self.DATA:
			print(partido)
	
	def __repr__(self):
		r="Nombre: "+str(self.nombre)+' Cantidad de datos: '+str(len(self.DATA))+'\n\n'
		for d in self.DATA:
			r+=d.__repr__()+'\n'
		return r

class Jugador():
	def __init__(self,apellido,nombre=None,inicial_nombre=None,inicial_apellido=None,web=None):
		self.nombre=nombre
		self.apellido=apellido
		self.inicial_nombre=inicial_nombre
		self.inicial_apellido=inicial_apellido
		if inicial_nombre is not None and len(inicial_nombre)>1:
			logger.error(self.__repr__()+" tiene una inicial con mas de una letra")
		if apellido=='' or apellido==' ' or apellido is None:
			logger.error(self.__repr__()+" no tiene apellido")
		
		self.web=web
		self.otros_nombres={}
		if web is not None:
			self.otros_nombres[web]={'inicial_nombre':inicial_nombre, 'nombre':nombre,'apellido':apellido}
			
	def to_dict(self):
		return {'nombre':self.nombre,'apellido':self.apellido,'inicial_nombre':self.inicial_nombre,'inicial_apellido':self.inicial_apellido}

	def _normalize(self,s):
		# https://es.stackoverflow.com/questions/135707/c%C3%B3mo-puedo-reemplazar-las-letras-con-tildes-por-las-mismas-sin-tilde-pero-no-l
		# -> NFD y eliminar diacríticos
		s = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", s), 0, re.I)
		# -> NFC
		s=normalize( 'NFC', s)
		return s.lower()

	def completar_con(self,other):
		if other.web is not None:
			self.otros_nombres[other.web]={'inicial_nombre':other.inicial_nombre, 'nombre':other.nombre,'apellido':other.apellido}
		
		if other.inicial_nombre is not None:
			if self.inicial_nombre is None:
				logger.debug("Añadiendo inicial_nombre a "+self.__repr__()+" de "+other.__repr__())
				self.inicial_nombre=other.inicial_nombre
			else:
				if self.inicial_nombre!=other.inicial_nombre:
					logger.error(self.__repr__()+" completandose con "+other.__repr__()+" pero tienen distinta inicial")

		if other.nombre is not None:
			if self.nombre is None:
				logger.debug("Añadiendo nombre a "+self.__repr__()+" de "+other.__repr__())
				self.nombre=other.nombre
			elif self.nombre!=other.nombre and self.nombre in other.nombre:
				logger.warning("Completando nombre de "+self.__repr__()+" con "+other.__repr__())
				self.nombre=other.nombre
		
	def __str__(self):
		if self.nombre is not None:
			return self.nombre+' '+self.apellido
		if self.inicial_nombre is not None:
			return self.inicial_nombre+' '+self.apellido
		return self.apellido
	
	def __repr__(self):
		r='Jugador('
		if self.inicial_nombre is not None:
			r+='inicial_nombre='+self.inicial_nombre+', '
			# return 'Jugador(inicial_nombre='+self.inicial_nombre+', apellido='+self.apellido+')'
		if self.nombre is not None:
			r+='nombre='+self.nombre+', '
			# return 'Jugador(nombre='+self.nombre+', apellido='+self.apellido+')'
		return r+'apellido='+self.apellido+')'
		# return 'Jugador(apellido='+self.apellido+')'
	
	def __eq__(self, other):
		if self.apellido.lower() in other.apellido.lower() or other.apellido.lower() in self.apellido.lower():
			if self.apellido.lower()!=other.apellido.lower():
				logger.debug(self.__repr__()+" y "+other.__repr__()+" no tienen exactamente el mismo apellido")
			if self.nombre is not None and other.nombre is not None:
				if self.nombre.lower()==other.nombre.lower():
					return True
			if self.inicial_nombre is not None and other.inicial_nombre is not None:			
				if self.inicial_nombre.lower()==other.inicial_nombre.lower():
					return True
			if self.inicial_nombre is not None and other.nombre is not None:
				if self.inicial_nombre.lower()==other.nombre[0].lower():
					# self.nombre
					return True
			if self.nombre is not None and other.inicial_nombre is not None:
				if self.nombre[0].lower()==other.inicial_nombre.lower():
					return True
			if (self.inicial_nombre is None and self.nombre is None) or (other.inicial_nombre is None and other.nombre is None):
				logger.warning(self.__repr__()+" y "+other.__repr__()+" han coincidido por falta de nombres/iniciales")
				return True
			if self.nombre is not None and other.nombre is not None:
				if self.nombre.lower() in other.nombre.lower() or other.nombre.lower() in self.nombre.lower():
					logger.warning(self.__repr__()+" y "+other.__repr__()+" han coincidido por inclusion de nombres")
					return True
				if self.nombre.replace(" ","").lower()==other.nombre.replace(" ","").lower():
					logger.warning(self.__repr__()+" y "+other.__repr__()+" han coincidido por omision de espacios en los nombres")
					return True
			logger.debug(self.__repr__()+" y "+other.__repr__()+" coinciden en apellido pero no en nombre")
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
	
	def __str__(self):
		if not self.dobles:
			return self.j1.__str__()
		return self.j1.__str__()+'/'+self.j2.__str__()
	
	def __repr__(self):
		if self.dobles:
			return 'Equipo(j1='+self.j1.__repr__()+', j2='+self.j2.__repr__()+')'
		return 'Equipo(j1='+self.j1.__repr__()+')'

	def __eq__(self,other):
		if self.dobles==other.dobles:
			if self.dobles==True:
				if self.j1==other.j1 and self.j2==other.j2:
					self.j1.completar_con(other.j1)
					self.j2.completar_con(other.j2)
					return True
			elif self.j1==other.j1:
				self.j1.completar_con(other.j1)
				return True
		return False

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
		return {'timestamp':self.timestamp,'e1':self.e1.to_dict(),'e2':self.e2.to_dict(),'odds1':{'numerator':self.odds1.numerator,'denominator':self.odds1.denominator},'odds2':{'numerator':self.odds2.numerator,'denominator':self.odds2.denominator},'dobles':self.dobles}

	def __str__(self):
		if not self.dobles:
			return str(self.e1)+' vs '+str(self.e2)+' | '+str(self.odds1)+' - '+str(self.odds2)
		return str(self.e1)+' vs '+str(self.e2)+' | '+str(self.odds1)+' - '+str(self.odds2)
	
	def __repr__(self):
		if self.timestamp is not None:
			return 'Dato(e1='+self.e1.__repr__()+', e2='+self.e2.__repr__()+', odds1='+str(self.odds1)+', odds2='+str(self.odds2)+', timestamp='+str(self.timestamp)+')'
		return 'Dato(e1='+self.e1.__repr__()+', e2='+self.e2.__repr__()+', odds1='+str(self.odds1)+', odds2='+str(self.odds2)+')'

class Evento():
	def __init__(self,dato,web):
		# Datos generales del evento
		self.e1=dato.e1
		self.e2=dato.e2
		self.dobles=dato.dobles
		self.timestamp=dato.timestamp
		self.timestamps=[]
		self.live=False
		if dato.timestamp is not None:
			self.timestamps.append(dato.timestamp)
			if dato.timestamp<time.time():
				self.live=True

		# Datos sobre la seguridad de la apuesta del evento
		self.segura=False
		self.web_apuesta_segura1=None
		self.web_apuesta_segura2=None
		self.apuesta_a_web1=None
		self.apuesta_a_web2=None
		self.esperanza=0
		self.ganancia_minima_asegurada=0
		self.conclusion=''

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

			self.conclusion="Apostando "
			self.conclusion+=str(self.apuesta_a_web1)+" en la web "+self.web_apuesta_segura1+" por "+str(self.e1)
			self.conclusion+=" y "
			self.conclusion+=str(self.apuesta_a_web2)+" en la web "+self.web_apuesta_segura2+" por "+str(self.e2)
			self.conclusion+=" gano asegurados: "+str(self.ganancia_minima_asegurada)+"="+str(float(self.ganancia_minima_asegurada))

			if not self.apuesta_a_web1*a-1==self.apuesta_a_web2*b-1:
				logger.error("El calculo de: "+self.conclusion+" no cuadra: self.apuesta_a_web1*a-1="+str(self.apuesta_a_web1*a-1)+" self.apuesta_a_web2*b-1="+str(self.apuesta_a_web2*b-1))

			logger.info(self.conclusion)

	def nuevo_dato(self,dato,web):
		metido=False
		if self.e1==dato.e1 and self.e2==dato.e2:
			if web in list(self.odds.keys()): logger.error("El evento "+self.__repr__()+" ya tiene odds de "+web+" y va a volver a meter el dato "+dato.__repr__())
			self.odds[web]=[dato.odds1,dato.odds2]
			metido=True
		elif self.e1==dato.e2 and self.e2==dato.e1:
			if web in list(self.odds.keys()): logger.error("El evento "+self.__repr__()+" ya tiene odds de "+web+" y va a volver a meter el dato "+dato.__repr__())
			self.odds[web]=[dato.odds2,dato.odds1]
			metido=True
		
		if metido:
			if dato.timestamp is not None:
				self.timestamps.append(dato.timestamp)
				if self.timestamp is None:
					self.timestamp=dato.timestamp
				else:
					if self.timestamp!=dato.timestamp:
						if self.timestamp<time.time():
							logger.timestamp_warning("El evento: "+self.__repr__()+" coincide con el dato: "+dato.__repr__()+" de la web "+web+" pero difieren en "+time.strftime('%H:%M:%S', time.gmtime(abs(self.timestamp-dato.timestamp)))+" en timestamp! Esto se debe a que el partido se está jugando en directo!")
							self.live=True
						else:
							logger.timestamp_warning("El evento: "+self.__repr__()+" coincide con el dato: "+dato.__repr__()+" de la web "+web+" pero difieren en "+time.strftime('%H:%M:%S', time.gmtime(abs(self.timestamp-dato.timestamp)))+" en timestamp! Estos son los timestamps hasta el momento: "+str(self.timestamps))
			return True
		return False

	def to_dict(self):
		j={'e1':self.e1.to_dict(),'e2':self.e2.to_dict()}
		j['timestamp']=self.timestamp
		j['Fecha']=datetime.utcfromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S (UTC)') if self.timestamp is not None else None
		odds={}
		for web in list(self.odds.keys()):
			odds[web]={
				'odds1':{'numerator':self.odds[web][0].numerator,'denominator':self.odds[web][0].denominator},
				'odds2':{'numerator':self.odds[web][1].numerator,'denominator':self.odds[web][1].denominator}
			}
		# j|={'odds':odds,'dobles:':self.dobles,'segura':self.segura}
		j.update({'odds':odds,'dobles:':self.dobles,'segura':self.segura})
		j['esperanza']=self.esperanza
		j['mejor_apuesta']={
			'web_apuesta_segura1':self.web_apuesta_segura1,
			'web_apuesta_segura2':self.web_apuesta_segura2,
			'apuesta_a_web1':{
				'numerator':None if self.apuesta_a_web1 is None else self.apuesta_a_web1.numerator,
				'denominator':None if self.apuesta_a_web1 is None else self.apuesta_a_web1.denominator,
				},
			'apuesta_a_web2':{
				'numerator':None if self.apuesta_a_web2 is None else self.apuesta_a_web2.numerator,
				'denominator':None if self.apuesta_a_web2 is None else self.apuesta_a_web2.denominator,
				},
			'ganancia_minima_asegurada':{
				'numerator':0 if self.ganancia_minima_asegurada==0 else self.ganancia_minima_asegurada.numerator,
				'denominator':1 if self.ganancia_minima_asegurada==0 else self.ganancia_minima_asegurada.denominator,
				},
			'conclusion':self.conclusion
		}
		return j

	def __repr__(self):
		if self.live:
			return str(self.e1)+' vs '+str(self.e2)+' | '+str(self.odds)+' || '+str(self.esperanza)+' | timestamp: EN CURSO'	
		return str(self.e1)+' vs '+str(self.e2)+' | '+str(self.odds)+' || '+str(self.esperanza)+' | timestamp: '+str(self.timestamp)


		