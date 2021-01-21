import requests
import random
import json
import os
import time
from bs4 import BeautifulSoup
import base64

def download_proxies_free_proxy():
	url = 'https://free-proxy-list.net/'
	response = requests.get(url)
	soup=BeautifulSoup(response.text,features="html5lib")
	filas=soup.find_all('tr')
	filas=[f for f in filas if f.find('td')!=None and f.find('th')==None]
	print(len(filas),"proxies encontrados en:",url)
	#filas=filas[:25]
	proxies={"proxies":[]}
	for f in filas:
		try:
			diccionario={}
			tds=f.find_all('td')
			diccionario['ip']=tds[0].text
			diccionario['puerto']=tds[1].text
			diccionario['codigo_pais']=tds[2].text
			diccionario['pais']=tds[3].text
			diccionario['anonimidad']=tds[4].text
			diccionario['google']=tds[5].text
			diccionario['https']=tds[6].text
			diccionario['last checked']=tds[7].text
			print(diccionario['pais'])
			if diccionario['pais']=='Spain':
				proxies["proxies"].append(diccionario)
		except Exception as e:
			print(e)
			print(f)
	print(len(proxies['proxies']),"proxies en españa")
	proxies['comentarios']={
		'source':url,
		'extraido':time.asctime()
	}
	f=open(os.getcwd()+'/herramientas_scraping/downloaded_proxies.json','w')
	json.dump(proxies, f)
	f.close()


def download_proxies_free_proxy2():
	url = 'http://free-proxy.cz/en/proxylist/country/ES/http/ping/level1'
	#url = 'http://free-proxy.cz/en/proxylist/'
	response = requests.get(url)
	soup=BeautifulSoup(response.text,features="html5lib")
	filas=soup.find('table',{'id':'proxy_list'}).find('tbody').find_all('tr')
	proxies={'proxies':[]}
	for f in filas:
		diccionario={}
		tds=f.find_all('td')
		javascript=tds[0].text
		#print("javascript:",javascript)
		if 'adsbygoogle' in javascript:
			continue
		ip=javascript.split('"')[1]
		#print("IP codificada:",ip)
		ip=base64.b64decode(ip).decode('ascii')
		diccionario['ip']=ip
		diccionario['puerto']=tds[1].text
		diccionario['protocol']=tds[2].text
		diccionario['pais']=tds[3].text
		print(diccionario['pais'])
		if 'Spain' not in diccionario['pais']:
			continue
		diccionario['region']=tds[4].text
		diccionario['ciudad']=tds[5].text
		diccionario['anonimidad']=tds[6].text
		diccionario['velocidad']=tds[7].text
		diccionario['tiempo de respuesta']=tds[9].text
		diccionario['last checked']=tds[10].text
		proxies["proxies"].append(diccionario)
	print(len(proxies['proxies']),"proxies en españa")
	proxies['comentarios']={
		'source':url,
		'extraido':time.asctime()
	}
	f=open(os.getcwd()+'/herramientas_scraping/downloaded_proxies.json','w')
	json.dump(proxies, f)
	f.close()

def proxy_info(proxy=None):
	url='http://free-proxy.cz/en/ipinfo'
	response = requests.get(url)
	soup=BeautifulSoup(response.text,features="html5lib")
	return soup



# Tambien se pueden sacar proxies de aqui:
# http://es.proxies.su/?country=ES
# https://es.proxies.su/?anonymity_type=elite&country=ES

def get_mi_ip(proxy=None):
	url = 'https://httpbin.org/ip'
	response=''
	if proxy==None:
		response = requests.get(url)
	else:
		response = requests.get(url,proxies=proxy)
	print(response.json())
	return response.json()

def get_random_proxy(nombre='proxies'):
	j=json.load(open(os.getcwd()+'/herramientas_scraping/'+nombre+'.json','r'))['mdict']
	r_ip=random.choice(list(j.keys()))
	r_p=j[r_ip]
	s=str(r_ip)+':'+str(r_p)
	proxy = {
	'http':  s,
	'https': s,
	}
	return proxy

def probar_proxies(nombre='proxies'):
	proxy=get_random_proxy(nombre)
	print(proxy)
	get_mi_ip(proxy)

