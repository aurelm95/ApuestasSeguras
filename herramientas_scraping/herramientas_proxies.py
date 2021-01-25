import requests
import random
import json
import os
import time
from bs4 import BeautifulSoup
import base64

# Tambien se pueden sacar proxies de aqui:
# http://es.proxies.su/?country=ES
# https://es.proxies.su/?anonymity_type=elite&country=ES

def download_proxies_free_proxy(spain=False):
	url = 'https://free-proxy-list.net/'
	response = requests.get(url)
	soup=BeautifulSoup(response.text,features="html5lib")
	filas=soup.find_all('tr')
	filas=[f for f in filas if f.find('td')!=None and f.find('th')==None]
	print('Aproximadamente',len(filas),"proxies encontrados en:",url)
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
			#print(diccionario['pais'])
			if len(diccionario['pais'])<=3: 
				#print(f)
				continue
			if diccionario['pais']=='Spain' or not spain:
				proxies["proxies"].append(diccionario)
		except Exception as e:
			print(e)
			print(f)
	print(len(proxies['proxies']),"proxies parseados. españa=",spain)
	proxies['comentarios']={
		'source':url,
		'extraido':time.asctime()
	}
	f=open(os.getcwd()+'/herramientas_scraping/proxies.json','w')
	json.dump(proxies, f)
	f.close()


def download_proxies_free_proxy2(spain=False):
	url='http://free-proxy.cz/en/proxylist/country/all/http/ping/level1'
	if spain:	url = url.replace('all','ES')
	headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'es',
	}
	response = requests.get(url, headers=headers, verify=False)
	soup=BeautifulSoup(response.text,features="html5lib")
	filas=soup.find('table',{'id':'proxy_list'}).find('tbody').find_all('tr')
	print('Aproximadamente',len(filas),"proxies encontrados en:",url)
	proxies={'proxies':[]}
	for f in filas:
		diccionario={}
		tds=f.find_all('td')
		if tds==[]:
			continue
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
		#print(diccionario['pais'])
		if spain and 'Spain' not in diccionario['pais']:
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
	f=open(os.getcwd()+'/herramientas_scraping/proxies2.json','w')
	json.dump(proxies, f)
	f.close()

def proxy_info(proxy=None):
	url='http://free-proxy.cz/en/ipinfo'
	response = requests.get(url)
	soup=BeautifulSoup(response.text,features="html5lib")
	return soup


def get_mi_ip(proxy=None):
	url = 'https://httpbin.org/ip'
	response=''
	if proxy==None:
		response = requests.get(url)
	else:
		response = requests.get(url,proxies=proxy,verify=False, timeout=10)
	print(response.json())
	return response.json()

def get_random_proxy(nombre='proxies',p=True):
	j=json.load(open(os.getcwd()+'/herramientas_scraping/'+nombre+'.json','r'))['proxies']
	if len(j)==0:
		print('No hay proxies para extraer')
		return None
	proxy=random.choice(j)
	if p==True: print(proxy)
	s=proxy['ip']+':'+proxy['puerto']
	proxy = {
	'http':  'http://'+s,
	'https': 'https://'+s
	}
	return proxy

def probar_proxies(nombre='proxies'):
	proxy=get_random_proxy(nombre)
	print(proxy)
	get_mi_ip(proxy)

