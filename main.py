import requests
import random
import json
import os
from bs4 import BeautifulSoup


from herramientas_scraping import get_proxies
from herramientas_scraping import headers


#get_proxies.download_proxies_free_proxy2()


def guardar_en_archivo(t):
	f=open('respuesta.txt','w')
	f.write(str(t))
	f.close()