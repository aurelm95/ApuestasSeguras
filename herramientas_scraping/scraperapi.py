import requests
import os



# https://www.scraperapi.com/dashboard




def make_request(url):
	scraperapi_url="http://api.scraperapi.com?api_key=8b049a828d27269d84d29e7e655c7062"
	url=scraperapi_url+'&url='+url
	return requests.get(url)