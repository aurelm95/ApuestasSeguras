import williamhill2 as williamhill
import betstars2 as betstars
import betfair2 as betfair
import bwin2 as bwin
#import telegram_bot

from data_classes import Dato, Evento

import json

class Apuestas():
	def __init__(self):
		self.williamhill=williamhill.Williamhill()
		self.betstars=betstars.Betstars()
		self.betfair=betfair.Betfair()
		self.bwin=bwin.Bwin()
		
		self.DATA=[]
		self.webs=['williamhill','betstars','betfair','bwin']
		
	def buscar_partidos(self):
		print("Buscando partidos en williamhill...")
		self.williamhill.buscar_partidos()

		print("Buscando partidos en betstars...")
		self.betstars.buscar_partidos()

		print("Buscando partidos en betfair...")
		self.betfair.buscar_partidos()

		print("Buscando partidos en bwin...")
		self.bwin.buscar_partidos()

	def comparar(self):
		# Pongo como base los numbre de williamhill porque son completos
		for dato in self.williamhill.DATA:
			self.DATA.append(Evento(dato,'williamhill'))
		
		# Los nombres de betstars son iguales que los de williamhill
		# El problema es que a veces (no se porque) cambia el orden de los jugadores
		for dato in self.betstars.DATA:
			metido=False
			for evento in self.DATA:
				if dato.j1==evento.j1 and dato.j2==evento.j2:
					evento.nuevas_odds(dato,'betstars')
					metido=True
					break
				elif dato.j1==evento.j1 and dato.j2==evento.j1:
					pass
			if not metido:
				self.DATA.append(Evento(dato,'betstars'))

		# williamhill: David Pichler  betstars: D Pichler
		for dato in self.betfair.DATA:
			if dato.dobles: continue
			n1=dato.j1.split(' ') # n1=['D','Pichler']
			n2=dato.j2.split(' ')
			metido=False
			for evento in self.DATA:
				if n1[0] in evento.j1 and n1[1] in evento.j1 and n2[0] in evento.j2 and n2[1] in evento.j2:
					evento.nuevas_odds(dato,'betfair')
					metido=True
					break
			if not metido:
				self.DATA.append(Evento(dato,'betfair'))

		# williamhill: David Pichler  bwin: D. Pichler
		for dato in self.bwin.DATA:
			if dato.dobles: continue
			n1=dato.j1.split(' ') # n1=['D.','Pichler']
			n2=dato.j2.split(' ')
			metido=False
			for evento in self.DATA:
				if n1[0].replace('.','') in evento.j1 and n1[1] in evento.j1 and n2[0].replace('.','') in evento.j2 and n2[1] in evento.j2:
					evento.nuevas_odds(dato,'bwin')
					metido=True
					break
			if not metido:
				self.DATA.append(Evento(dato,'bwin'))

	def comparar2(self):
		for dato in self.williamhill.DATA:
			self.DATA.append(Evento(dato,'williamhill'))
		objetos=[self.betstars,self.betfair,self.bwin]
		for o in objetos:
			for dato in o.DATA:
				for evento in self.DATA:
					metido=evento.nuevo_dato(dato,o.nombre)
					if metido: break
				if not metido:
					self.DATA.append(Evento(dato,o.nombre))

	def actualizar_json(self):
		self.j={}
		for e in self.DATA:
			odds={}
			for web in list(e.odds.keys()):
				d1=round(float(e.odds[web][0]),2)
				d2=round(float(e.odds[web][1]),2)
				odds[web]=str(d1)+' - '+str(d2)
			self.j[e.j1+' vs '+e.j2]=odds
		f=open('API/tenis.json','w')
		json.dump(self.j,f)
		f.close()

	def guardar_html(self):
		self.williamhill.guardar_html()
		self.betstars.guardar_html()
		self.betfair.guardar_html()
		self.bwin.guardar_html()

	def buscar_apuestas_seguras(self):
		pass

	def print_simple(self):		
		print("\n\nPrinteando partidos en williamhill...")
		self.williamhill.print()

		print("\n\nPrinteando partidos en betstars...")
		self.betstars.print()

		print("\n\nPrinteando partidos en betfair...")
		self.betfair.print()

		print("\n\nPrinteando partidos en bwin...")
		self.bwin.print()

	def pretty_print(self):
		print('\n')
		ml=max([len(str(e.j1)+' vs '+str(e.j2)) for e in self.DATA])+1
		encabezado='Partidos'
		encabezado+=' '*(ml-len(encabezado))
		linea='-'*ml
		lca=16 # longitud casas de apuestas
		for w in self.webs:
			encabezado+=' | '+w
			encabezado+=' '*(lca-len(w))
			linea+='-+-'+'-'*lca
		print(encabezado)
		print(linea)
		for e in self.DATA:
			linea=str(e.j1)+' vs '+str(e.j2)
			linea+=' '*(ml-len(linea))
			for w in self.webs:
				linea+=' | '
				if w in e.odds.keys():
					odds=str(e.odds[w][0])+' vs '+str(e.odds[w][1])
					linea+=odds
					linea+=' '*(lca-len(odds))
				else:
					linea+=' '*lca
			print(linea)



	

if __name__=='__main__':
	a=Apuestas()
	a.buscar_partidos()
	a.comparar()
	a.pretty_print()
	pass

