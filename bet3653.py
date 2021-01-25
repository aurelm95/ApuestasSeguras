import requests # https://pypi.org/project/requests/
#from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import re
from fractions import Fraction

from herramientas_scraping import scraperapi


class Bet365():
	def __init__(self):
		self.DATA=[]

	def buscar_partidos(self):
		self.url='https://www.bet365.es/SportsBook.API/web?lid=3&zid=0&pd=%23AS%23B13%23&cid=171&ctid=171'
		self.r = scraperapi.make_request(self.url)