import time
import json

class CasaDeApuestas():
	def __init__(self):
		self.nombre=None
		self.DATA=[]
		self.respuesta=None

	def guardar_html(self):
		f=open('htmls/'+self.nombre+'.html','w')
		f.write(self.respuesta.text)
		f.close()

	def guardar_data_en_json(self):
		self.j={'timestamp':time.time(),'web':self.nombre}
		self.j['DATA']=[dato.to_dict() for dato in self.DATA]
		f=open(self.nombre+'.json','w')
		json.dump(self.j,f)
		f.close()


	def print(self):
		print("\n"+self.nombre+":",len(self.DATA),"partidos\n")
		for partido in self.DATA:
			print(partido)


class NombreJugador():
	def __init__(self,nombre_completo):
		self.nombre=None
		self.apellido=None
		self.inical_nombre=None
		self.inicial_apellido=None
	
	def __eq__(self, other):
		if self.apellido==other.apellido:
			if self.nombre==other.nombre:
				return True
			if self.inical_nombre==other.inical_nombre:
				return True
		return False

class NombreEquipo():
	def __init__(self,nombre_completo):
		self.dobles=None
		self.j1=NombreJugador(nombre_completo)
		self.j2=NombreJugador(nombre_completo)

class Dato():
	def __init__(self,j1,j2,odds1,odds2,dobles=False):
		self.j1=j1
		self.j2=j2
		self.odds1=odds1
		self.odds2=odds2
		self.dobles=dobles
		self.parsear_nombre()

	def parsear_nombre(self):
		if ',' in self.j1:
			n=self.j1.split(',')
			self.j1=n[1][1:]+' '+n[0]
		if ',' in self.j2:
			n=self.j2.split(',')
			self.j2=n[1][1:]+' '+n[0]

	def reverse(self):
		return Dato(self.j2,self.j1,self.odds2,self.odds1,dobles=self.dobles)
	
	def to_dict(self):
		return {'j1':self.j1,'j2':self.j2,'odds1':{'numerator':self.odds1.numerator,'denominator':self.odds1.denominator},'odds2':{'numerator':self.odds2.numerator,'denominator':self.odds2.denominator},'dobles':self.dobles}

	def __repr__(self):
		if not self.dobles:
			return self.j1+' vs '+self.j2+' | '+str(self.odds1)+' - '+str(self.odds2)
		return str(self.j1)+' vs '+str(self.j2)+' | '+str(self.odds1)+' - '+str(self.odds2)


class Evento():
	def __init__(self,dato,web):
		# Datos generales del evento
		self.j1=dato.j1
		self.j2=dato.j2
		self.dobles=dato.dobles

		self.segura=False

		# Los guardo como unas odds de la web
		self.odds={web:[dato.odds1,dato.odds2]}
	
	def nuevas_odds(self,dato,web):
		self.odds[web]=[dato.odds1,dato.odds2]

	def apuesta_segura(self):
		pass

	def nuevo_dato(self,dato,web):
		if self.dobles!=dato.dobles: return False
		if dato.dobles: return False
		print("nuevo_dato():",dato)
		if self.j1==dato.j1 and self.j2==self.j2:
			self.odds[web]=[dato.odds1,dato.odds2]
			return True
		if self.j2==dato.j1 and self.j1==self.j2:
			self.odds[web]=[dato.odds2,dato.odds1]
			return True
		lj1=dato.j1.split('.')
		lj2=dato.j2.split('.')
		compatible=True
		for s in lj1:
			if s not in self.j1:
				compatible=False
				break
		for s in lj2:
			if s not in self.j2:
				compatible=False
				break
		if compatible:
			self.odds[web]=[dato.odds2,dato.odds1]
			return True
		compatible=True
		for s in lj1:
			if s not in self.j2:
				compatible=False
				break
		for s in lj2:
			if s not in self.j1:
				compatible=False
				break
		if compatible:
			self.odds[web]=[dato.odds1,dato.odds2]
			return True
		return False


	def __str__(self):
		return str(self.j1)+' vs '+str(self.j2)+' | '+str(self.odds) 
		