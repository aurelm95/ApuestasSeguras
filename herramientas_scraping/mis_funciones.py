import os
from pprint import pprint

def guardar_en_archivo(t):
	f=open('respuesta.txt','w')
	f.write(str(t))
	f.close()
	print("Texto guardado en: respuesta.txt")

def clear():
	os.system('clear')