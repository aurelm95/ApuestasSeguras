import requests
s=requests.Session()

# Consigo la cookie aps03
headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.google.com/',
    'Accept-Language': 'es-ES,es;q=0.9',
}

response = s.get('https://www.bet365.es/', headers=headers)

print(response)


# para conseguir la cookie pstk
# problema: no se de donde sale la cookie __cf_bm
# cookies = {
#     'aps03': 'ct=171&lng=3',
#     '__cf_bm': 'ix1bVpvhYA0ds_LpxfrJkDoClYl9h_h7foIAc.s67uw-1643585729-0-AVzXqpHlUV+nenT6iZz7ats42rjXKs0YP4IYRY85p45D8feeeVSU9OobgovkInDIW95M9aGQmpFiVwgxVdxpseI=',
# }

# headers = {
#     'Connection': 'keep-alive',
#     'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
#     'Origin': 'https://www.bet365.es',
#     'sec-ch-ua-mobile': '?0',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
#     'sec-ch-ua-platform': '"Windows"',
#     'Accept': '*/*',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Dest': 'empty',
#     'Referer': 'https://www.bet365.es/',
#     'Accept-Language': 'es-ES,es;q=0.9',
# }

# params = (
#     ('_h', '9II7U6z5kFJPXiHxgn9ttg=='),
# )

# response = requests.get('https://www.bet365.es/defaultapi/sports-configuration', headers=headers, params=params, cookies=cookies)
