from . import williamhill
from . import betstars
from . import betfair
from . import bwin
#import telegram_bot

from .data_classes import Dato, Evento
from .logger import apuestas_logger as logger

import os
import json
import time
from fractions import Fraction
import pandas as pd


class Apuestas():
	def __init__(self):
		self.williamhill=williamhill.Williamhill()
		self.betstars=betstars.Betstars()
		self.betfair=betfair.Betfair()
		self.bwin=bwin.Bwin()
		
		self.DATA=[]
		self.webs=['williamhill','betstars','betfair','bwin']
		self.fecha_ultima_busqueda=None
		
	def buscar_partidos(self):
		logger.info("Buscando y parseando partidos en williamhill...")
		self.williamhill.buscar_partidos()
		self.williamhill.guardar_html()
		self.williamhill.parsear_partidos()
		logger.info("Guardando datos de williamhill en /json...")
		self.williamhill.guardar_data_en_json()
		
		logger.info(str(len(self.williamhill.DATA))+" partidos encontrados")

		logger.info("Buscando y parseando partidos en betstars...")
		self.betstars.buscar_partidos()
		self.betstars.guardar_html()
		logger.info("Guardando datos de betstars en /json...")
		self.betstars.guardar_data_en_json()
		logger.info(str(len(self.betstars.DATA))+" partidos encontrados")

		logger.info("Buscando y parseando partidos en betfair...")
		self.betfair.buscar_partidos()
		self.betfair.guardar_html()
		logger.info("Guardando datos de betfair en /json...")
		self.betfair.guardar_data_en_json()
		logger.info(str(len(self.betfair.DATA))+" partidos encontrados")

		logger.info("Buscando y parseando partidos en bwin...")
		self.bwin.buscar_partidos()
		self.bwin.guardar_html()
		logger.info("Guardando datos de bwin en /json...")
		self.bwin.guardar_data_en_json()
		logger.info(str(len(self.bwin.DATA))+" partidos encontrados")

		self.fecha_ultima_busqueda=time.time()

	# para development/debug
	def cargar_partidos(self):
		for casa in [self.williamhill, self.betstars, self.betfair, self.bwin]:
			logger.info("Cargando partidos de "+casa.nombre+"...")
			casa.cargar_data_de_json()
		logger.debug("Datos cargados")

	def comparar(self):
		logger.debug("Comparando...")
		self.DATA=[]
		for dato in self.williamhill.DATA:
			self.DATA.append(Evento(dato,'williamhill'))
		casas=[self.betstars,self.betfair,self.bwin]
		for casa in casas:
			for dato in casa.DATA:
				# if dato.dobles: continue
				for evento in self.DATA:
					# print("comparo:",evento,dato)
					metido=evento.nuevo_dato(dato,casa.nombre)
					# print("metido:",metido)
					if metido: break
				if not metido:
					self.DATA.append(Evento(dato,casa.nombre))

	# deprecated
	def ordenar_eventos_alfabeticamente(self):
		logger.warning("El metodo ordenar_eventos_alfabeticamente() esta obsoleto")
		return
		# https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
		self.DATA.sort(key=lambda x: x.j1)
	
	# deprecated
	def actualizar_json(self):
		logger.warning("El metodo actualizar_json() esta obsoleto")
		return
		self.j={'timestamp':self.fecha_ultima_busqueda}
		self.j['DATA']=[evento.to_dict() for evento in self.DATA]
		f=open(os.path.dirname(__file__)+'/jsons/tenis.json','w')
		json.dump(self.j,f)
		f.close()

	def guardar_html(self):
		self.williamhill.guardar_html()
		self.betstars.guardar_html()
		self.betfair.guardar_html()
		self.bwin.guardar_html()

	def buscar_apuestas_seguras(self):
		logger.debug("Buscando apuestas seguras...")
		for evento in self.DATA:
			evento.comprobar_apuesta_segura()

	def print_simple(self):		
		print("\n\nPrinteando partidos en williamhill...")
		self.williamhill.print()

		print("\n\nPrinteando partidos en betstars...")
		self.betstars.print()

		print("\n\nPrinteando partidos en betfair...")
		self.betfair.print()

		print("\n\nPrinteando partidos en bwin...")
		self.bwin.print()

	def pretty_print(self,archivo="pretty_print.txt"):
		TEXT="\n"
		ml=max([len(str(e.e1)+' vs '+str(e.e2)) for e in self.DATA])+1
		encabezado='Partidos'
		encabezado+=' '*(ml-len(encabezado))
		linea='-'*ml
		lca=16 # longitud casas de apuestas
		for w in self.webs:
			encabezado+=' | '+w
			encabezado+=' '*(lca-len(w))
			linea+='-+-'+'-'*lca
		# print(encabezado)
		# print(linea)
		TEXT+=encabezado+'\n'
		TEXT+=linea+'\n'
		for e in self.DATA:
			linea=str(e.e1)+' vs '+str(e.e2)
			linea+=' '*(ml-len(linea))
			for w in self.webs:
				linea+=' | '
				if w in e.odds.keys():
					odds=str(e.odds[w][0])+' vs '+str(e.odds[w][1])
					linea+=odds
					linea+=' '*(lca-len(odds))
				else:
					linea+=' '*lca
			# print(linea)
			TEXT+=linea+'\n'
		
		print(TEXT)
		f=open(archivo,"w")
		f.write(TEXT)
		f.close()

	def to_dataframe(self):
		df = pd.DataFrame(columns=["Equipo 1","Equipo 2","williamhill 1","williamhill 2","betstars 1","betstars 2","betfair 1","betfair 2","bwin 1","bwin 2","Esperanza","Segura","Ganancia","Conclusion"])
		for evento in self.DATA:
			linea={"Equipo 1":str(evento.e1),"Equipo 2":str(evento.e2)}
			for web in list(evento.odds.keys()):
				# linea|={web+' 1':round(float(evento.odds[web][0]),2),web+' 2':round(float(evento.odds[web][1]),2)}
				linea.update({web+' 1':round(float(evento.odds[web][0]),2),web+' 2':round(float(evento.odds[web][1]),2)})
			# print(evento.esperanza, type(evento.esperanza))
			linea['Esperanza']=evento.esperanza
			linea['Segura']=evento.segura
			linea['Ganancia']=float(evento.ganancia_minima_asegurada)
			linea['Conclusion']=evento.conclusion
			df=df.append(linea,ignore_index=True)
		return df


	

if __name__=='__main__':
	a=Apuestas()
	# a.buscar_partidos()
	a.cargar_partidos()
	a.comparar()
	a.buscar_apuestas_seguras()
	df=a.to_dataframe()
	pass


