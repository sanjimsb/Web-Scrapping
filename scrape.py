import requests
import os
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib3
from sys import argv
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from views.allnews import newslink
from individual_views.baahrakhari import barakhari


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

	def checkusnicode(self,s):
		if isinstance(s, str):
			link_type = 1
		elif isinstance(s, unicode):
			link_type = 0
		return link_type

	def getportalname(self,url):
		self.splittedurl = url.split('.com/')
		return self.splittedurl[0].replace('https://','')

	def mainScrape(self):
		if(self.page != 'noconnection'):
			if(self.page.status_code == 200):
				soup = BeautifulSoup(self.page.content, 'html.parser')
				# title = self.moreNews(soup)
				if(self.sitehome == 'https://onlinekhabar.com/'):
					nav = self.navItem(soup,'div','menu-primary-menu-container')
				elif(self.sitehome == 'https://gorkhapatraonline.com/'):
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
			if(self.sitehome == 'https://onlinekhabar.com/'):
				getsoupsiglehead = self.checknotnone(allcont,'h2', 'mb-0')
				getsoupsigle = self.checknotnone(allcont,'div', 'main__read--content')
			elif(self.sitehome == 'https://gorkhapatraonline.com/'):
				getsoupsiglehead = self.checknotnone(allcont,'h1', 'post-title')
				getsoupsigle = self.checknotnone(allcont,'div', 'newstext')

			singlecontent = getsoupsigle.select('p')
			h = getsoupsiglehead.get_text()
			content = document.add_heading(getsoupsiglehead.get_text(),2)
			for cont in singlecontent:
				conten1 = document.add_paragraph(cont.get_text())
			path = os.getcwd()
			sn = self.getportalname(self.sitehome)

			if not os.path.exists('News'):
				os.mkdir('News')
				if not os.path.exists('News/%s'% sn):
					os.mkdir('News/%s' %sn)
					if not os.path.exists('News/%s/%s' %(sn,MainCategory)):
						os.mkdir('News/%s/%s' %(sn,MainCategory))
						if(SubCategory != ''):
							if not os.path.exists('News/%s/%s/%s' %(sn,MainCategory, SubCategory)):
								os.mkdir('News/%s/%s' %(MainCategory, SubCategory))
								document.save('News/%s/%s/%s/%s_news_%s.docx' %(sn,MainCategory, SubCategory, SubCategory, counter))
						else:
							document.save('News/%s/%s/%s_news_%s.docx' %(sn,MainCategory, MainCategory, counter))
			else:
				if not os.path.exists('News/%s' % sn):
					os.mkdir('News/%s' %sn)
					if not os.path.exists('News/%s/%s' % (sn,MainCategory)):
						os.mkdir('News/%s/%s' % (sn,MainCategory))
						if (SubCategory != ''):
							if not os.path.exists('News/%s/%s/%s' %(sn,MainCategory, SubCategory)):
								os.mkdir('News/%s/%s/%s' %(sn,MainCategory, SubCategory))
								document.save('News/%s/%s/%s/%s_news_%s.docx' %(sn,MainCategory, SubCategory, SubCategory, counter))
							else:
								document.save('News/%s/%s/%s/%s_news_%s.docx' %(sn,MainCategory, SubCategory, SubCategory, counter))
						else:
							document.save('News/%s/%s/%s_news_%s.docx' %(sn,MainCategory, MainCategory, counter))
					else:
						if (SubCategory != ''):
							if not os.path.exists('News/%s/%s/%s' %(sn,MainCategory, SubCategory)):
								os.mkdir('News/%s/%s/%s' %(sn,MainCategory, SubCategory))
								document.save('News/%s/%s/%s/%s_news_%s.docx' %(sn,MainCategory, SubCategory, SubCategory, counter))
							else:
								document.save('News/%s/%s/%s/%s_news_%s.docx' %(sn,MainCategory, SubCategory, SubCategory, counter))
						else:
							document.save('News/%s/%s/%s_news_%s.docx' %(sn,MainCategory, MainCategory, counter))
				else:
					if not os.path.exists('News/%s/%s' % (sn,MainCategory)):
						os.mkdir('News/%s/%s' % (sn,MainCategory))
						if (SubCategory != ''):
							if not os.path.exists('News/%s/%s/%s' %(sn,MainCategory, SubCategory)):
								os.mkdir('News/%s/%s/%s' %(sn,MainCategory, SubCategory))
								document.save('News/%s/%s/%s/%s_news_%s.docx' %(sn,MainCategory, SubCategory, SubCategory, counter))
							else:
								document.save('News/%s/%s/%s/%s_news_%s.docx' %(sn,MainCategory, SubCategory, SubCategory, counter))
						else:
							document.save('News/%s/%s/%s_news_%s.docx' %(sn,MainCategory, MainCategory, counter))
					else:
						if (SubCategory != ''):
							if not os.path.exists('News/%s/%s/%s' %(sn,MainCategory, SubCategory)):
								os.mkdir('News/%s/%s/%s' %(sn,MainCategory, SubCategory))
								document.save('News/%s/%s/%s/%s_news_%s.docx' %(sn,MainCategory, SubCategory, SubCategory, counter))
							else:
								document.save('News/%s/%s/%s/%s_news_%s.docx' %(sn,MainCategory, SubCategory, SubCategory, counter))
						else:
							document.save('News/%s/%s/%s_news_%s.docx' %(sn,MainCategory, MainCategory, counter))

		return None

	def category(self,getsoup,MainCatName):
		if(self.sitehome == 'https://onlinekhabar.com/'):
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

		elif (self.sitehome == 'https://gorkhapatraonline.com/'):
			if getsoup is not None:
				linklist =[]
				selectCat = getsoup.find('div',{'class':'sports-groups'})
				if selectCat is not None:
					getlink = selectCat.find_all('a')
					count = 1
					for indlk in getlink:
						if indlk.has_attr('href'):
							catsoup = BeautifulSoup(self.otherPage(indlk['href']).content, 'html.parser')
							self.saveindividual(catsoup,MainCatName,'',count)
						count = count + 1

			# print getlink
			# sys.exit()
			# if selectCat is not None:
			# 	for indlk in selectCat:
			# 		selectLink = indlk.find_all('a')
			# 		linklist.append(selectLink)
			# print linklist
			# for lk in linklist:
			# 	self.moreNews(catsoup,MainCatName,self.splitUrl(str(individualcat['href'])),1)
					# print selectLink['href']
					# if selectLink.has_attr('href'):
					# 	newpagesoup = BeautifulSoup(self.otherPage(srt(selectLink['href'])).content, 'html.parser')
					# 	self.moreNews(newpagesoup,MainCatName,'',1)
			# selectCat = getsoup.find_all('div',{'class':'page-news-list'})
			# for individual_news in selectCat:
			# 	print individual_news
			# print getsoup
				
		return None

	def navItem(self,allcont,htmele,eleclass):
		nav_strip = self.filter(allcont,htmele,eleclass)
		get_nav_item = nav_strip.select('a')
		nav_link = []
		cat = []
		for a in get_nav_item:
			if a.has_attr('href') and a['href'] != '/' and a['href'] != '#':
				cat.append(self.splitUrl(str(a['href'].encode('ascii', 'ignore').decode('ascii'))))
				nav_link.append(str(a['href'].encode('ascii', 'ignore').decode('ascii')))
			else:
				continue
		for nav,cattitle in zip(nav_link,cat):
			newsoup = BeautifulSoup(self.otherPage(nav).content, 'html.parser')
			self.category(newsoup,cattitle);
		return None


