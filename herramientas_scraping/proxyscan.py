import requests
import random
import json
import os
import time
from bs4 import BeautifulSoup



def download_proxies(spain=False):
	url='https://www.proxyscan.io/api/proxy'
	if spain: url+='?country=es'
	r=requests.get()
	j=r.json()
	print("Se han descargado",len(j),'proxies. españa=',spain)
	f=open(os.getcwd()+'/herramientas_scraping/proxyscan.json','w')
	json.dump(j, f)
	f.close()

def get_random_proxy(nombre='proxyscan'):
	j=json.load(open(os.getcwd()+'/herramientas_scraping/'+nombre+'.json','r'))
	proxy=random.choice(j)
	s=str(proxy['Ip'])+':'+str(proxy['Port'])
	proxy = {
	'http':  'http://'+s,
	'https': 'https://'+s,
	}
	return proxy