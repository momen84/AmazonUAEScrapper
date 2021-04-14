#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  NewPy.py
#  
#  Copyright 2018 Momen <momen@momen-Lenovo>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import requests
from bs4 import BeautifulSoup
import time
import re
import ast
import amazon_scrapper_detect_variations as a_scrapper
#import amazon_books_scrapper as a_book_scrapper
import os
import logging
import database
from datetime import datetime
import random


__name__ = "Sellers_Crawler"
logging.basicConfig(level=logging.DEBUG,filename='a_scrapping.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent}
rest_time=5
all_categories='https://www.amazon.ae/gp/site-directory?ie=UTF8&ref_=nav_shopall_fullstore'
base_link='https://www.amazon.ae'





def get_products_links(link):
	logger.info('Started inside get_products_links({})'.format(link))
	req=requests.get(link,headers=headers)

	bsobj=BeautifulSoup(req.text,'lxml')
	
	results_div=bsobj.find('div',{'id':'search-results'})
	# products=results_div.findAll('a',{'class':'a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal'})
	products=results_div.findAll('div',{'class':'s-item-container'})

	logger.info('Found {} products'.format(len(products)-1))
	li_asin=results_div.findAll('li',id=re.compile(r'^result*'))
	bulk_asin=[]
	for data in li_asin:
		bulk_asin.append(data.attrs['data-asin'])
	
	logger.info('Check bulk_asin for {}'.format(bulk_asin))
	check_all=database.check_product_exists_bulk(bulk_asin)
	# print(check_all)
	if check_all is None or len(check_all)==0:
		logger.info('All records to be added')
		for product in products[:-1]:
			logger.info('Getting link for product number {}'.format(products.index(product)))
			product_link=product.find('a',{'class':'a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal'}).attrs['href']
			logger.info('Product link is {}'.format(product_link))
			print(product_link) #do not comment ..... Important for error tracing
			logger.info('Category link={}'.format(link))
			logger.info('Creating Product object from scrapper')
			product,seller=a_scrapper.get_product_details(product_link,link)
			logger.info('Got product , seller pair = {} , {} '.format(product,seller))
		# 	# print(product)
		# 	# print(seller)
			logger.info('Add product seller pair to products database')
			database.add_record(product,seller)
			logger.info('product seller pair added to products database')
			time.sleep(3)
	elif len(check_all)>0 :
		diff_asins=list(set(bulk_asin)-set([x[0] for x in check_all]))
		# print(diff_asins)
		# print(check_all)
		logger.info('Unique bulk ASINs={}'.format(len(diff_asins)))
		print('Unique bulk ASINs={}'.format(len(diff_asins)))
		for x in diff_asins:
		
			product_link='https://www.amazon.ae/dp/'+x
			logger.info('Getting link for product number {}'.format(diff_asins.index(x)))
			# product_link=product.find('a',{'class':'a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal'}).attrs['href']
			logger.info('Product link is {}'.format(product_link))
			print(product_link) #do not comment ..... Important for error tracing

			logger.info('Creating Product object from scrapper')
			product,seller=a_scrapper.get_product_details(product_link,link)
			logger.info('Got product , seller pair = {} , {} '.format(product,seller))
		# 	# print(product)
		# 	# print(seller)
			logger.info('Add product seller pair to products database')
			database.add_record(product,seller)
			logger.info('product seller pair added to products database')
			time.sleep(3)

def check_if_book(product_link):
	req=requests.get(product_link,headers=headers)

	bsobj=BeautifulSoup(req.text,'lxml')
	product_cat_section=bsobj.findAll('a',{'class':'a-link-normal a-color-tertiary'})
	product_category=[]
	for x in product_cat_section:
		product_category.append(x.get_text().strip())
	product_category='>'.join(product_category)
	# print(product_category)
	if 'Books' in product_category:
		return True
	else:
		return False


def get_products_links_from_sellers(seller_link,seller_id):
	req=requests.get(seller_link,headers=headers)

	bsobj=BeautifulSoup(req.text,'lxml')
	counter=0
	for product in bsobj.findAll('div'):
		if 'data-asin' in product.attrs:
			counter+=1
			product_link='https://www.amazon.ae/dp/'+product.attrs['data-asin']
			
			check_book=check_if_book(product_link)
			if check_book is True:
				print('Book scrapper to be implemented')
				
			else:
		
				logger.info('Getting link for product number {}'.format(product.attrs['data-index']))
				# product_link=product.find('a',{'class':'a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal'}).attrs['href']
				logger.info('Product link is {}'.format(product_link))
				print(product_link) #do not comment ..... Important for error tracing

				logger.info('Creating Product object from scrapper')
				product,seller=a_scrapper.get_product_details(product_link,'From Sellers Scrapper')
				logger.info('Got product , seller pair = {} , {} '.format(product,seller))
			# 	# print(product)
			# 	# print(seller)
				logger.info('Add product seller pair to products database')
				database.add_record(product,seller)
				logger.info('product seller pair added to products database')
				time.sleep(3)



def get_seller_page(seller_id):

	random_page=str(random.randint(1,400))
	seller_link='https://www.amazon.ae/s?me='+seller_id+'&page='+random_page

	get_products_links_from_sellers(seller_link,seller_id)

	



def main(args):
	logger.info('Starting crawler')
	database.check_local_or_cloud()
	database.check_tables_exists()
	
	sellers_query=database.get_sellers_for_seller_scrapper()
	sellers=[]
	for seller in sellers_query:
		sellers.append(seller[0])
	
	while True:
		seller_id=random.choice(sellers)
		get_seller_page(seller_id)



if __name__ == 'Sellers_Crawler':
	import sys
	sys.exit(main(sys.argv))
