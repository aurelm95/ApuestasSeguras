import os
import time
import json
from fractions import Fraction



class CasaDeApuestas():
	def __init__(self):
		self.nombre=None
		self.DATA=[]
		self.respuesta=None

	def guardar_html(self):
		f=open(os.path.dirname(__file__)+'/htmls/'+self.nombre+'.html','w', encoding="utf-8")
		f.write(self.respuesta.text)
		f.close()
	
	def cargar_html(self):
		f=open(os.path.dirname(__file__)+'/htmls/'+self.nombre+'.html','r', encoding="utf-8")
		self.respuesta_text=f.read()
		f.close()

	def guardar_data_en_json(self):
		self.j={'timestamp':time.time(),'web':self.nombre}
		self.j['DATA']=[dato.to_dict() for dato in self.DATA]
		f=open(os.path.dirname(__file__)+'/jsons/'+self.nombre+'.json','w')
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
		if self.apellido==other.apellido:
			if self.nombre==other.nombre:
				return True
			if self.inicial_nombre==other.inicial_nombre:
				return True
			if other.nombre is not None:
				if self.inicial_nombre==other.nombre[0]:
					return True
			if self.nombre is not None:
				if self.nombre[0]==other.inicial_nombre:
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
	def __init__(self,e1,e2,odds1,odds2,dobles=False):
		self.e1=e1
		self.e2=e2
		self.odds1=odds1
		self.odds2=odds2
		self.dobles=dobles

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

		self.segura=False
		self.esperanza=0

		# Los guardo como unas odds de la web
		self.odds={web:[dato.odds1,dato.odds2]}
	
	def nuevas_odds(self,dato,web):
		self.odds[web]=[dato.odds1,dato.odds2]

	def comprobar_apuesta_segura(self):
		for web1 in list(self.odds.keys()):
			for web2 in list(self.odds.keys()):
				if web1==web2: continue # asumo que nunca pasara
				esperanza=(self.odds[web1][0]-1)*(self.odds[web2][1]-1)
				self.esperanza=max(self.esperanza,float(esperanza))
				if esperanza>1:
					self.segura=True


	def nuevo_dato(self,dato,web):
		if self.e1==dato.e1 and self.e2==dato.e2:
			self.odds[web]=[dato.odds1,dato.odds2]
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
		