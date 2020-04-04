import requests
import os
import sys
from bs4 import BeautifulSoup
from sys import argv
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from views.allnews import newslink

class DataMining:
	fail = 'No Connection, Please Check Your Internet Connection!'
	def __init__(self,siteurl):
		try:
			self.page = requests.get(siteurl)
			self.sitehome = siteurl
		except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.RequestException, requests.exceptions.ConnectionError, requests.exceptions.HTTPError,):
			self.page = 'noconnection'
			print self.noConn()
			sys.exit()
		return None

	def noConn(self):
		return self.fail

	def otherPage(self,site_new_url):
		self.othp = requests.get(site_new_url)
		return self.othp

	def splitUrl(self,geturl):
		surl = geturl.split('/')
		return surl.pop()

	def homeUrl(self,gethm):
		return gethm.rstrip('/')

	def mainScrape(self):
		if(self.page != 'noconnection'):
			if(self.page.status_code == 200):
				soup = BeautifulSoup(self.page.content, 'html.parser')
				# title = self.moreNews(soup)
				if(self.sitehome == 'http://onlinekhabar.com/'):
					nav = self.navItem(soup,'div','menu-primary-menu-container')
				elif(self.sitehome == 'https://baahrakhari.com/'):
					nav = self.navItem(soup,'ul','navbar-nav')
				# print self.splitUrl(self.sitehome)
				
			else:
				return self.noConn()
		return None

	def filter(self,allcont,htm_element,clss):
		return allcont.find(htm_element,class_=clss)

	def checknotnone(self,allcont,htm_element,clss):
		if allcont.find(htm_element,class_=clss) is not None:
			return allcont.find(htm_element,class_=clss)

		return None 

	def paginationcall(self,soup,MainCategory,SubCategory,count):
		for page in soup:
			if count >= 501:
				break
			elif page.has_attr('href'):
				pagesinglesoup = BeautifulSoup(self.otherPage(page['href']).content, 'html.parser')
				self.moreNews(pagesinglesoup,MainCategory,SubCategory,count)
		return None

	def moreNews(self,morecontent,MainCategory,SubCategory,counter):
		single_page = []
		more_news = morecontent.find_all('a',{'class':'title__regular'})
		pagination = morecontent.find_all('a',{'class':'next page-numbers'})
		if more_news is not None:
			count = counter
			for single in more_news:
				if count >= 501:
					break
				elif single.has_attr('href'):
					soupsingle = BeautifulSoup(self.otherPage(single['href']).content, 'html.parser')
					self.saveindividual(soupsingle,MainCategory,SubCategory,count)
				count = count + 1
		# if pagination is not None:
		# 	self.paginationcall(pagination,MainCategory,SubCategory,count)
		return None

	def saveindividual(self,allcont,MainCategory,SubCategory,counter):
		if allcont is not None:
			document = Document()
			getsoupsiglehead = self.checknotnone(allcont,'h2', 'mb-0')
			getsoupsigle = self.checknotnone(allcont,'div', 'main__read--content')
			singlecontent = getsoupsigle.select('p')
			h = getsoupsiglehead.get_text()
			content = document.add_heading(getsoupsiglehead.get_text(),2)
			for cont in singlecontent:
				conten1 = document.add_paragraph(cont.get_text())
			path = os.getcwd()
			if not os.path.exists('News'):
				os.mkdir('News')
				if not os.path.exists('News/%s' %(MainCategory)):
					os.mkdir('News/%s' %(MainCategory))
					if not os.path.exists('News/%s/%s' %(MainCategory, SubCategory)):
						os.mkdir('News/%s/%s' %(MainCategory, SubCategory))
						document.save('News/%s/%s/%s_news_%s.docx' %(MainCategory, SubCategory, SubCategory, counter))
			else:
				if not os.path.exists('News/%s' %(MainCategory)):
					os.mkdir('News/%s' %(MainCategory))
				elif not os.path.exists('News/%s/%s' %(MainCategory, SubCategory)):
					os.mkdir('News/%s/%s' %(MainCategory, SubCategory))
					document.save('News/%s/%s/%s_news_%s.docx' %(MainCategory, SubCategory, SubCategory, counter))
				else:
					document.save('News/%s/%s/%s_news_%s.docx' %(MainCategory, SubCategory, SubCategory, counter))			
		return None

	def category(self,getsoup,MainCatName):
		if(MainCatName == 'news'):
			pass
		else:
			selectCat = getsoup.find_all('a',{'class':'read__all--dot'});
			print MainCatName
			for individualcat in selectCat:
				if individualcat.has_attr('href'):
					newUrlcat =  str(self.homeUrl(self.sitehome) + individualcat['href'] )
					catsoup = BeautifulSoup(self.otherPage(newUrlcat).content, 'html.parser')
					self.moreNews(catsoup,MainCatName,self.splitUrl(str(individualcat['href'])),1)
		return None

	def navItem(self,allcont,htmele,eleclass):
		nav_strip = self.filter(allcont,htmele,eleclass)
		get_nav_item = nav_strip.select('a')
		nav_link = []
		cat = []
		for a in get_nav_item:
			print a
			if a.has_attr('href') and a['href'] != '/':
				cat.append(self.splitUrl(str(a['href'])))
				nav_link.append(str(a['href']))
			else:
				continue
		for nav,cattitle in zip(nav_link,cat):
			newsoup = BeautifulSoup(self.otherPage(nav).content, 'html.parser')
			self.category(newsoup,cattitle);
		return None


