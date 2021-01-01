import williamhill
import betfair
import betstars
#import telegram_bot

class Apuestas():
	def __init__(self):
		self.williamhill=williamhill.Williamhill()
		print("Buscando partidos en williamhill...")
		self.williamhill.buscar_partidos()

		self.betfair=betfair.Betfair()
		print("Buscando partidos en betfair...")
		self.betfair.buscar_partidos()

		self.betstars=betstars.Betstars()
		print("Buscando partidos en betstars...")
		self.betstars.buscar_partidos()	

	def comparar(self):
		# Los nombres son de la forma:
		# Nombre Apellido  -  Nombre Apellido
		# Hay dos espacios entre el guion y los nombres
		# Deberan ser asi con todas las casas de apuestas

		

		#color print("\033[32mholaaa\033[00m")

		print("Comparando...\n")
		self.contador=0
		self.seguras=0
		# En la lista comparaciones por cada partido habra: [nombre del partido, [odd1 wh, odd2 wh], [odd1 bf, odd2 bf]]
		self.comparaciones=[]
		# En betfair suele haber solo los apellidos
		for p1 in self.williamhill.DATA:
			if type(p1[0][0][0])==type([1]):
				# De momento no tendre en cuenta los dobles
				continue
			nombre=str(p1[0][0][0])+' '+str(p1[0][0][1])+' vs '+str(p1[0][1][0])+' '+str(p1[0][1][1])
			self.comparaciones.append([nombre,[p1[1],p1[2]]])

			for p2 in self.betfair.DATA:
				if len(p2[0][0])==1 and len(p2[0][1])==1 and p2[0][0][0]==p1[0][0][1] and p2[0][1][0]==p1[0][1][1]:
					self.contador+=1
					self.comparaciones[-1].append([p2[1],p2[2]])
					self.apuesta_segura(p1,p2)
			if len(self.comparaciones[-1])==2:
				self.comparaciones[-1].append([0,0])

			for p3 in self.betstars.DATA:
				if p3[0][0][0]==p1[0][0][0] and p3[0][0][1]==p1[0][0][1] and p3[0][1][0]==p1[0][1][0] and p3[0][1][1]==p1[0][1][1]:
					self.comparaciones[-1].append([p3[1],p3[2]])
					self.contador+=1
					self.apuesta_segura(p1,p3)
					#print(p3[0])
				if p3[0][1][0]==p1[0][0][0] and p3[0][1][1]==p1[0][0][1] and p3[0][0][0]==p1[0][1][0] and p3[0][0][1]==p1[0][1][1]:
					self.comparaciones[-1].append([p3[2],p3[1]])
					self.contador+=1
					self.apuesta_segura(p1,p3)
					#print(p3[0])
			if len(self.comparaciones[-1])==3:
				self.comparaciones[-1].append([0,0])
													
		self.info=""
		self.info+="Williamhill: "+str(len(self.williamhill.DATA))+" partidos\n"
		self.info+="Betfair    : "+str(len(self.betfair.DATA))+" partidos\n"
		self.info+="Betstars   : "+str(len(self.betstars.DATA))+" partidos\n"
		self.info+="Han habido "+str(self.contador)+" coincidencias\nSeguras: "+str(self.seguras)+"\n\n"
		print(self.info)
		#if len(self.bet365.DATA)>0 and len(self.williamhill.DATA)>0 and contador==0:
		# Mensaje de posible error en el parseo o en la comparacion
		print("Mandando mensaje al telegram...")
		#telegram_bot.enviar_mensaje(self.info)

	def apuesta_segura(self,p1,p2):
		# Si la casa1 da para el jugador1 un pago de x por euro apostado
		# La casa2 deberia dar por el jugador2 y>1+1/(x-1) euros por euro apostado
		# Si tenemos en cuenta los Odds (ganancias-1) entonces
		# Si Odd1=x buscamos Odd2>1/x

		if p1[1]>1/p2[2] or p1[2]>1/p2[1]:
			print("Apuesta segura:")			
			n1=p1[0][0][0]+' '+p1[0][0][1]
			n2=p2[0][1][0]+' '+p2[0][1][1]
			print(n1," vs ",n2)
			ml=max([len(n1),len(n2)])
			espacios=' '*ml
			rayas='-'*ml
			print(espacios,'| williamhill | otra')
			print('|'+rayas,'---------------------------')
			print('|'+n1,' '*(ml-len(n1)),'| ',round(float(p1[1]+1),2),round(float(p2[1]+1),2))
			print('|'+rayas,'---------------------------')
			print('|'+n2,' '*(ml-len(n2)),'| ',round(float(p1[2]+1),2),round(float(p2[2]+1),2))
			print('|'+rayas,'---------------------------')
			
			print("Apostando 1 euro en wh por",n1," y ",round(float(p1[1]),2)," en la otra casa por",n2)
			print("1*",round(float(p1[1]+1),2),-1-round(float(p1[1]),2),"=",round(float(p1[1]+1),2)-1-round(float(p1[1]),2),">0")
			print(round(float(p1[1]),2),"*",round(float(p2[2]+1),2),-1-round(float(p1[1]),2),"=",round(float(p1[1]),2)*round(float(p2[2]+1),2)-1-round(float(p1[1]),2),">0")
			print("")
			self.seguras+=1

	def print(self):
		#self.bet365.print()
		#self.williamhill.print()
		'''print("\nwilliamhill:\n")
		for p in self.williamhill.DATA:
			print(p[0],p[1],p[2])
		print("\nbetfair:\n")
		for p in self.betfair.DATA:
			print(p[0],p[1],p[2])
		print("\nbetstars:\n")
		for p in self.betstars.DATA:
			print(p[0],p[1],p[2])'''

		print("\nTABLA:\n")
		ml=max([len(p[0]) for p in self.comparaciones])
		espacios=' '*ml
		rayas='-'*ml
		print(espacios,'| williamhill | betfair | betstars')
		print(rayas,'---------------------------')
		for p in self.comparaciones:
			l=len(p[0])
			try:
				print(p[0]+' '*(ml-l),'| ',round(float(p[1][0]),2),round(float(p[1][1]),2),' | ',round(float(p[2][0]),2),round(float(p[2][1]),2),' | ',round(float(p[3][0]),2),round(float(p[3][1]),2))
			except:
				print(p[0]+' '*(ml-l),'| ',float(p[1][0]),float(p[1][1]),' | ')

if __name__=='__main__':
	#a=Apuestas()
	#a.comparar()
	#a.print()
	pass

