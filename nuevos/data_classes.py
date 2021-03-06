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

	def nuevo_dato(self,dato,web):
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
		