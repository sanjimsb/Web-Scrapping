from views.allnews import newslink
from scrape import DataMining

get_news_links = newslink()

for link in get_news_links.newsportal():
	mainFun = DataMining(link)
	mainFun.mainScrape()
		
