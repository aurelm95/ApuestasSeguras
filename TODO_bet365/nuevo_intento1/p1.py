import requests

cookies = {
    'pstk': '381A8E560B91487585EAD37AA349D78C000003', # expires in 1 week
    'rmbs': '3', # expires in 6 months
    'aps03': 'cf=N&cg=4&cst=0&ct=171&hd=N&lng=3&oty=2&tzi=4', # expires in 10 years
    '__cf_bm': '8cmzVDUCCISm446388oR4WP.TEYmhMG5Z9OUGOKV7cE-1643576421-0-AapVn0MyertPVbF5xbuCT/9UahhW8cvGLWt71YJ4FPPALOslK7gp3MqpPSz2it+0YlV05ZS6UF7BAmA/pUZi01Kbhi992oGLKxExxDFgg+qdWJidYB165SUJHbPjawBgisAwYjRYIg16BIkulh26g9O/spmOve+1trzfq+d/h5VL', #expires in 1 day
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'X-Net-Sync-Term': 'LE74YQ==.tCxcVFE3eD7uC3i37qzOVFmBkoyzDTKTrRS/kdvEUIg=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.bet365.es/',
    'Accept-Language': 'es-ES,es;q=0.9',
}

params = (
    ('lid', '3'),
    ('zid', '0'),
    ('pd', '#AS#B13#'),
    ('cid', '171'),
    ('cgid', '4'),
    ('ctid', '171'),
)


cookies2 = {
    'pstk': '2669CE9B907264859AA3D6C68684346B000003',
    'rmbs': '3',
    'aps03': 'cf=N&cg=4&cst=0&ct=171&hd=N&lng=3&oty=2&tzi=4',
    '__cf_bm': 'dHu4rUmjxVzmf9ytfEMVA0Fpx7v1xrOieWERk_FUqvY-1643586632-0-ASJ3JPBbI6nqdD+ds364EotFuw100o+02ouoo+CYqKwJ6yV7NlgRJzACsbee95dhk9iYzu6lAJ6FLq7EK9m0eBH+5hPRdNFcthu5jw60kFSj5J2uG7lCw14C9YLdyNdgELae0jhx0Wg+Uon1hIgxHs3q/1XJ7CLhrxMJM8ZzadWM',
}

headers2 = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'X-Net-Sync-Term': 'QnL4YQ==.iTu0w96J594DCMCnlRZkZDa24evFcv1aXqfOHbT4Gbo=', # este es el unico que cambia pero da igual, lo importante son las cookies
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.bet365.es/',
    'Accept-Language': 'es-ES,es;q=0.9',
}

# los params son siempre iguales
params2 = (
    ('lid', '3'),
    ('zid', '0'),
    ('pd', '#AS#B13#'),
    ('cid', '171'),
    ('cgid', '4'),
    ('ctid', '171'),
)

# s=requests.Session()

# r=s.get("https://www.bet365.es", headers=headers)

# response = requests.get('https://www.bet365.es/SportsBook.API/web', headers=headers, params=params, cookies=cookies)
# response = requests.get('https://www.bet365.es/SportsBook.API/web', headers=headers2, params=params2, cookies=cookies2)

s=requests.Session()

# https://stackoverflow.com/questions/17224054/how-to-add-a-cookie-to-the-cookiejar-in-python-requests-library
requests.utils.add_dict_to_cookiejar(s.cookies, cookies2)
s.headers=headers2

response = s.get('https://www.bet365.es/SportsBook.API/web', params=params)