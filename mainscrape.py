from views.allnews import newslink
from scrape import DataMining
from sys import argv
script, numberofnews = argv

get_news_links = newslink()

for link in get_news_links.newsportal():
	mainFun = DataMining(link,numberofnews)
	mainFun.mainScrape()
		
