import random 
import requests
from collections import OrderedDict

mis_headers=[
	# ordenador grande google chrome
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

	# ordenador grande microsoft edge
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

# https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
# This data was created by using the curl method explained above
def get_header(headers=mis_headers):
	# Create ordered dict from Headers above
	headers = random.choice(headers)
	h = OrderedDict()
	for header,value in headers.items():
			h[header]=value					
	return h


def comparar_header(header):
	print("Original:",header)
	j=requests.get('https://httpbin.org/headers',headers=header).json()
	print("Recibido:",j)
