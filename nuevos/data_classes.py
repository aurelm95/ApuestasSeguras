class Dato():
	def __init__(self,j1,j2,odds1,odds2,dobles=False):
		self.j1=j1
		self.j2=j2
		self.odds1=odds1
		self.odds2=odds2
		self.dobles=dobles

	def parsear_nombre(self):
		pass

	def reverse(self):
		return Dato(self.j2,self.j1,self.odds2,self.odds1)

	def __str__(self):
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

	def __str__(self):
		return str(self.j1)+' vs '+str(self.j2)+' | '+str(self.odds) 
		

	