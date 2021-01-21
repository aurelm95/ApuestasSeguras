import requests

# peticiones al link:
# https://www.amazon.es/dp/B07J6Q2L98/
mis_headers_portatil=[
	# Portatil google chrome
	{
    'authority': 'www.amazon.es',
    'rtt': '50',
    'downlink': '6.65',
    'ect': '4g',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'es-ES,es;q=0.9',
    'cookie': 'session-id=262-3366911-1290525; i18n-prefs=EUR; ubid-acbes=261-2755120-2883754; session-token=wW52nKHSt5AORb3p3f1ChGW6/o102Mf61EU2TjZKXM1O0OuRT6kTdcLVv4tcJBBba3CkiDSbMAe/xlXsk05g/hFrphmQcXx/Ft7Im/KyGd38NbJzT572RT60BGj7VHeBxz/35mM4xUFMfGHEa3ESYARhCaM1/UthFlRqVPxpSKReFyccURxfmNbcfE3MP2+O; session-id-time=2082758401l; csm-hit=tb:5352N0CZ224KTN4P00SJ+s-5352N0CZ224KTN4P00SJ|1611097054994&t:1611097054994&adb:adblk_no',
	},

	# Portatil firefox
	{
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
	},

	# Grande google Chrome
	{
    'authority': 'www.amazon.es',
    'sec-ch-ua': '^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'es-ES,es;q=0.9',
	},

	# Grande microsoft edge
	 {
    'authority': 'www.amazon.es',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'es',
	}
]



class Amazon():
	def __init__(self):
		self.s=requests.Session()
		self.link='https://www.amazon.es/Satisfyer-Vibration-presi%C3%B3n-vibraci%C3%B3n-impermeable/dp/B07J6Q2L98/ref=zg_bs_4347447031_1?_encoding=UTF8&psc=1&refRID=TB07HZX4G6QBRS4V0QZ4'
		self.link_simple='https://www.amazon.es/dp/B07J6Q2L98/'
	
	def buscar(self):
		#self.r=self.s.get(self.link)
		self.r=requests.get(self.link_simple,headers=mis_headers_portatil[1])

