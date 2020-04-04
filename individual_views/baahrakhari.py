# from . import DataMining
from bs4 import BeautifulSoup

def barakhari(getsoup,maincat):
	selectCat = getsoup.find_all('div',{'class':'md-newspage'})
	print maincat
	print selectCat
	return None