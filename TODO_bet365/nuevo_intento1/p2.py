import requests

cookies = {
    'pstk': '381A8E560B91487585EAD37AA349D78C000003',
    'rmbs': '3',
    'aps03': 'cf=N&cg=4&cst=0&ct=171&hd=N&lng=3&oty=2&tzi=4',
    'lrc': '72',
    '__cf_bm': '2RL7ObMO841aGN3xY8ifmt3nbD7aPY6cWFe3uKd9e08-1643579511-0-ATOjBeyoCFwkYCI9wzKeLIaAatLc5eHUxDMCeVWdVWpVDroTZDAAhZwIq3Mpeo0PVCXRaGfi+/ONsZemBa8CgEyqb9PZt42cK3+NL9JYS24OoouUh8pWm5cxu7MEoHSoLh+IrngUURjB5tOamSyBaVR3qE4uqNziAIzWJaMvqfr0',
}

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

response = requests.get('https://www.bet365.es/', headers=headers, cookies=cookies)