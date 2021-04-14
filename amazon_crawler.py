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
import os
import logging
import database
from datetime import datetime
import random


__name__ = "Crawler"
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


	
def get_products_links_0_9(random_cat_link,random_cat_name,random_pref,random_page):

	category_link=random_cat_link
	category_name=random_cat_name
	cat_page_number=random_page
	cat_link_code=random_cat_link
	cat_link_pref=random_pref	
	products_link=random_cat_link+random_pref+'&page='+str(random_page)
	
	scrapped_date_time=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")  # dd/mm/YY H:M:S format
	
	status='Scrapped'
	logger.info('Crawler status for page={}'.format(status))
	crawler_record=(category_name,category_link,products_link,cat_link_code,cat_link_pref,cat_page_number,scrapped_date_time,status)
	# # crawler_record=(category_name,category_link,page_link,cat_link_code,cat_page_number,status)
	logger.info('Crawler record= {}'.format(crawler_record))
	logger.info('Check if crawler record {} in crawler database'.format(crawler_record))
	if database.check_crawler_record(crawler_record) is None:
		logger.info('Crawler record not found in crawler database, creating new crawler record')
		database.create_crawler_record(crawler_record)
		logger.info('Crawler record created successfully')
		try:
			get_products_links(products_link)
			logger.info('Finished get_products_links({})'.format(products_link))
		except:
			print('No products found in {}'.format(products_link))
			logger.info('No products found in {}'.format(products_link))

	else:
		logger.info('Crawler record exists in crawler database, pass')
		print('Crawler record exists = {}'.format(crawler_record))


	


		
		
		

	

def get_category_pages(category_link,category_name):
	logger.info('Start get_category_pages({},{})'.format(category_link,category_name))
	req=requests.get(category_link,headers=headers)

	bsobj=BeautifulSoup(req.text,'lxml')
	all_pages=int(bsobj.find('span',{'id','pagnDisabled'}).get_text())
	print(all_pages)
	
	total_product_in_category=bsobj.find('span',{'id':'s-result-count'}).get_text()
	logger.info('Total products in category = {}, total pages={}'.format(total_product_in_category,all_pages))
	print(total_product_in_category)
	logger.info('Starting to get products links')
	# return all_pages
	visited_pages=set()
	
	for page in range(1,all_pages+1):
		page=random.randint(1,all_pages+1)
		page_link=category_link+'&page='+str(page)
		if page_link in visited_pages:
			pass
		else:
			visited_pages.add(page_link)
			print('='*30)
			print(page_link)
			print('='*30)
			cat_page_number=page_link.split('=')[-1]
			
			cat_link_code=page_link.split('=')[-3].rstrip('&s')
			cat_link_pref=page_link.split('=')[-2].rstrip('&page')
			
			logger.info('Get get_products_links({})'.format(page_link))
			get_products_links(page_link)
			time.sleep(3)
			logger.info('Finished get_products_links({})'.format(page_link))
			scrapped_date_time=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")  # dd/mm/YY H:M:S format
			
			status='Scrapped'
			logger.info('Crawler status for page={}'.format(status))
			crawler_record=(category_name,category_link,page_link,cat_link_code,cat_link_pref,cat_page_number,scrapped_date_time,status)
			# crawler_record=(category_name,category_link,page_link,cat_link_code,cat_page_number,status)
			logger.info('Crawler record= {}'.format(crawler_record))
			logger.info('Check if crawler record {} in crawler database'.format(crawler_record))
			if database.check_crawler_record(crawler_record) is None:
				logger.info('Crawler record not found in crawler database, creating new crawler record')
				database.create_crawler_record(crawler_record)
				logger.info('Crawler record created successfully')
			else:
				logger.info('Crawler record exists in crawler database, pass')
				print('Crawler record exists = {}'.format(crawler_record))


def get_categories():
	logger.info('Starting get_categories()')
	featured=''
	price_low_high='&s=price-asc-rank'
	price_high_low='&s=price-desc-rank'
	review_rank='&s=review-rank'
	newest='&s=date-desc-rank'


	link=all_categories
	# category_choice={'featured':'','price_low_high':'&s=price-asc-rank','price_high_low':'&s=price-desc-rank','review_rank':'&s=review-rank','newest':'&s=date-desc-rank'}
	category_choice_list=[featured,price_low_high,price_high_low,review_rank,newest]
	req=requests.get(link,headers=headers)

	bsobj=BeautifulSoup(req.text,'lxml')
	# for category in bsobj.findAll('div',{'class':'popover-grouping'}):
	# for category in bsobj.findAll('td',{'style':'width: 25%'}):
	visited_cat_link=set()

	for div in bsobj.findAll('div',{'class':'popover-grouping'})[3:]:
		for category in div.findAll('a'):
			category_name=category.get_text().strip()
			rlink=category.attrs['href']
			featured_category_link=base_link+rlink
			print(featured_category_link,',',category_name)
			# print(featured_category_link)
			# if 'Amazon' in category_name:
			# 	logger.info('Amazon word found in get_categories(), pass')
			# 	pass
			# else:
			# 	for pref in category_choice_list:
			# 		pref=random.choice(category_choice_list)
			# 		category_link=featured_category_link+pref
			# 		if category_link in visited_cat_link:
			# 			pass
			# 		else:
			# 			visited_cat_link.add(category_link)
					
			# 			logger.info('Getting pages for prefernce {}'.format(pref))
			# 			category_link=featured_category_link+pref
						# print(category_link)
						# logger.info('Category link {} caught'.format(category_link))
						# logger.info('Starting get_category_pages({},{})'.format(category_link,category_name))
						# get_category_pages(category_link,category_name)
						# logger.info('get_category_pages() finished')
						# print('='*30)
						# logger.info('Sleeping 5 seconds between category gets')
						# time.sleep(5)

def get_categories_0_9():
	logger.info('Starting get_categories_0_9()')
	featured=''
	price_low_high='&s=price-asc-rank'
	price_high_low='&s=price-desc-rank'
	review_rank='&s=review-rank'
	newest='&s=date-desc-rank'

	pref_choice_list=[featured,price_low_high,price_high_low,review_rank,newest]
	all_categories_list=[]
	try:
		with open('/home/momen/amazon/all_categories_links.txt') as categories_links:
			
			for line in categories_links:
				all_categories_list.append(line.strip())
		random_cat_link_and_name=random.choice(all_categories_list)
		random_pref=random.choice(pref_choice_list)
		
	except:
		with open('all_categories_links.txt') as categories_links:
			for line in categories_links:
				all_categories_list.append(line.strip())
		random_cat_link_and_name=random.choice(all_categories_list)
		random_pref=random.choice(pref_choice_list)

	return 	random_cat_link_and_name,random_pref





def main(args):
	logger.info('Starting crawler')
	database.check_local_or_cloud()
	database.check_tables_exists()
	

	visited_cat_link=set()
	try:
		while True:
			
			random_cat_link_and_name,random_pref=get_categories_0_9()
			random_cat_link=random_cat_link_and_name.split(',')[0].strip()
			random_cat_name=random_cat_link_and_name.split(',')[1].strip()
			random_page=str(random.randint(1,400))

			
			products_link=random_cat_link+random_pref+'&page='+str(random_page)
			if not products_link in visited_cat_link:
				visited_cat_link.add(products_link)
				get_products_links_0_9(random_cat_link,random_cat_name,random_pref,random_page)

			else:
				pass
	except KeyboardInterrupt:
		sys.exit()
		print('KeyboardInterrupt !!')
		logger.info('KeyboardInterrupt !!')



	# test_links_from_file()
	# rescrap_from_database()
	# get_categories()


if __name__ == 'Crawler':
	import sys
	sys.exit(main(sys.argv))
