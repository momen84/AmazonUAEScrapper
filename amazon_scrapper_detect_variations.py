
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
import hashlib
from datetime import datetime
import logging
from pprint import pprint
##commented for testing
_name__ = "Scrapper"
logging.basicConfig(level=logging.DEBUG,filename='a_file_scrapping.log', format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)



user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent}
rest_time=5
all_categories='https://www.amazon.ae/gp/site-directory?ie=UTF8&ref_=nav_shopall_fullstore'
base_link='https://www.amazon.ae'


class Product_1(object):
	def __init__(self,product,right_col,link):
		# print(right_col.find('span',{'class','a-color-price'}))

		variants_div=product.find('div',{'id':'twister_feature_div'}).find('div',{'id':'twisterContainer'})

		if variants_div:
			for x in variants_div.findAll('div',id=re.compile(r'variation')):
				if x.attrs['id']=='variation_digital_storage_capacity':
					# print(x.get_text().strip())
					# size_variants=';'.join([l for l in x.get_text().strip('\n')])
					size_variants=x.get_text().strip('\n').lstrip('\n').rstrip('\n').replace('\n','').strip()
					self.size_variants=size_variants
				elif x.attrs['id']=='variation_size_name':
					if x.findAll('option'):
						# for y in x.findAll('option')[1:]:

							# print(y.get_text().strip())
				
						size_variants=';'.join([n.get_text().strip() for n in x.findAll('option')[1:]])
						self.size_variants=size_variants
					elif not x.findAll('li'):
						size_variants=x.get_text().strip().replace('\n','')
						# for y in  x.findAll('li'):
							# print(y.get_text().strip('Click to select'))
						self.size_variants=size_variants
					elif x.findAll('li'):
						size_variants=';'.join([n.get_text().replace('Click to select ','').strip('\n') for n in x.findAll('li')])

					# else:
					# 	self.size_variants=None
						self.size_variants=size_variants
				else:
					self.size_variants=None
				
				if x.attrs['id']=='variation_color_name':
					if x.findAll('li'):
						color_variants=';'.join([m.attrs['title'].replace('Click to select ','') for m in x.findAll('li')])
						self.color_variants=color_variants	
					elif not x.findAll('li'):
						color_variants=x.span.get_text().strip().replace('\n','')
						self.color_variants=color_variants
				else:
					self.color_variants=None
				
				if x.attrs['id']=='variation_style_name':
					if x.findAll('li'):
						style_variants=';'.join([n.get_text().replace('Click to select ','').strip('\n') for n in x.findAll('li')])
						self.style_variants=style_variants
					else:
						style_variants=x.get_text().strip('\n').lstrip('\n').rstrip('\n').replace('\n','').strip()
						self.style_variants=style_variants
				else:
					self.style_variants=None
				
		
			
		else:
			# self.remarks=None
			self.size_variants=None
			self.color_variants=None
			self.style_variants=None
		# print(self.size_variants)
		self.remarks='{} variants available'.format((self.size_variants,self.color_variants,self.style_variants))
		customer_reviews=product.find('div',{'id':"averageCustomerReviews"})
		if customer_reviews:
			try:
				self.reviews=customer_reviews.find('span',{'id':"acrPopover"}).get_text().strip()
			except:
				self.reviews=customer_reviews.find('span',{'id':"acrCustomerWriteReviewText"}).get_text().strip()
		
		else:
			self.reviews=None
		
	
		if self.reviews =='Be the first to review this item':
			self.review_count=0
		else:
			try:
			# self.no_of_reviews=int(customer_reviews.find('span',{'id':"acrCustomerReviewText"}).get_text().strip().replace(' customer reviews',''))
				self.review_count=int(customer_reviews.find('span',{'id':"acrCustomerReviewText"}).get_text().strip().split(' ')[0])
			except:
				self.review_count=0

		self.title=product.find('span',{'id':'productTitle'}).get_text().strip()
		# except:
		# 	self.title=link.strip('https://www.amazon.ae/').split('/')[0].replace('-',' ')

		self.ASIN=link.split('dp/')[1].split('/ref')[0]
		self.link=link


		try:
			self.availability=product.find('div',{'id':'availability_feature_div'}).span.get_text().strip()


		except AttributeError:
			
			self.availability='Available with Variants'

		try:
			self.other_offers_link=base_link+product.find('span',{'class':'olp-padding-right'}).find('a').attrs['href']
			self.other_offers_count=int(product.find('span',{'class':'olp-padding-right'}).find('a').get_text().strip().split()[0])
		except:
			self.other_offers_link=None
			self.other_offers_count=None
		
		try:
			self.page_seller=product.find('a',{'id':"sellerProfileTriggerId"}).get_text()
			self.page_seller_link=base_link+product.find('a',{'id':"sellerProfileTriggerId"}).attrs['href']
			self.seller_id=product.find('a',{'id':"sellerProfileTriggerId"}).attrs['href'].split('seller=')[1].replace('&isAmazonFulfilled=1','')
		except:
			try:
				self.page_seller=product.find('div',{'id':"merchant-info"}).get_text().strip().replace('Ships from and sold by ','')
				self.page_seller_link='https://amazon.ae'
				self.seller_id='amazon_ae'
			except:
				self.page_seller=None
				self.page_seller_link=None
				self.seller_id=None


		try:
			self.list_price=float(product.find('span',class_=re.compile(r'a-text-strike')).get_text().strip().replace('AED','').replace(',',''))
		# self.list_price=float(product.find('span',{'class':'priceBlockStrikePriceString a-text-strike'}).get_text().strip().replace('AED','').replace(',',''))
		

		except:
			self.list_price=None
		
		


		page_price_1=product.find('span',id=re.compile(r"priceblock"))
		if page_price_1:
			# print('page_price_1 {}'.format(page_price_1))
			self.page_price=page_price_1.get_text().replace('AED','').replace(',','')
			if '-' in self.page_price:
				self.page_price=float(self.page_price.split('-')[1].replace('AED','').replace(',',''))
			else:
				self.page_price=float(self.page_price)
		elif not page_price_1:

			# try:
			# page_price=product.find('span',{'class':'olp-padding-right'}).find('span',{'class':'a-color-price'})
			page_price_2=product.find('span',{'class':'a-color-price'})
			# print('page_price_2 {}'.format(page_price_2))
			if page_price_2:
					# try:
				self.page_price=float(page_price_2.get_text().replace('AED','').replace(',',''))

			else:
				page_price_3=right_col.find('span',{'class','a-color-price'})
				# print('page_price_3 {}'.format(page_price_3))
				if page_price_3:
					# try:
					self.page_price=right_col.find('span',{'class','a-color-price'}).get_text().replace('AED','').replace(',','')		
				else:
					self.page_price=None


		else:
			self.page_price=None
		

	

def parse_product_lxml_parser(req_text):
	bsobj=BeautifulSoup(req_text,'lxml')
	product_cat_section=bsobj.findAll('a',{'class':'a-link-normal a-color-tertiary'})
	product_category=[]
	for x in product_cat_section:
		product_category.append(x.get_text().strip())
	product_category='>'.join(product_category)
	product_page=bsobj.find('div',{'id':'centerCol'})
	right_col=bsobj.find('div',{'id':'rightCol'})
	# print(product_page)
	# print(right_col.find('span',{'class','a-color-price'}))
	return product_category,product_page,right_col

def parse_product_html_parser(req_text):
	bsobj=BeautifulSoup(req_text,'html.parser')
	product_cat_section=bsobj.findAll('a',{'class':'a-link-normal a-color-tertiary'})
	product_category=[]
	for x in product_cat_section:
		product_category.append(x.get_text().strip())
	product_category='>'.join(product_category)
	product_page=bsobj.find('div',{'id':'centerCol'})
	right_col=bsobj.find('div',{'id':'rightCol'})
	# print(right_col.find('span',{'class','a-color-price'}))

	return product_category,product_page,right_col



def get_product_details(link,cat_link):
	
	time.sleep(3)
	req=requests.get(link,headers=headers)
	logger.info('Link {} has response = {}'.format(link,req.status_code))
	if req.status_code==200:
		try:
			product_category,product_page,right_col=parse_product_lxml_parser(req.text)
			product=Product_1(product_page,right_col,link)#,product_details)
			p_scrapped_date_time=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

		##commented for testing
			product2database=(product.title,
							product.ASIN,
							product_category,
							cat_link,
							product.list_price,
							product.page_price,
							product.link,
							product.other_offers_link,
							product.other_offers_count,
							product.reviews,
							product.review_count,
							product.seller_id,
							product.availability,
							product.remarks,
							product.color_variants,
							product.size_variants,
							product.style_variants,
							p_scrapped_date_time)
			# print(product2database)
			seller2database=(product.page_seller,product.page_seller_link,product.seller_id)
			
			# logger.info('Product={} \n Seller={}'.format(product2database,seller2database))
			logger.info(vars(product))
			print('From lxml.parser')
			# if len(vars(product).keys())==0:
			# 	return 0
			# else:

			pprint(vars(product))
			# return(vars(product))
			logger.info(vars(product))
			return product2database,seller2database
			# return product.page_price
		except AttributeError:# product_category is None or product_page is None:
		# 	pass
			product_category,product_page,right_col=parse_product_html_parser(req.text)
			product=Product_1(product_page,right_col,link)#,product_details)
			p_scrapped_date_time=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

			product2database=(product.title,
							product.ASIN,
							product_category,
							cat_link,
							product.list_price,
							product.page_price,
							product.link,
							product.other_offers_link,
							product.other_offers_count,
							product.reviews,
							product.review_count,
							product.seller_id,
							product.availability,
							product.remarks,
							product.color_variants,
							product.size_variants,
							product.style_variants,
							p_scrapped_date_time)
			# print(product2database)
			seller2database=(product.page_seller,product.page_seller_link,product.seller_id)
			
			# logger.info('Product={} \n Seller={}'.format(product2database,seller2database))
			logger.info(vars(product))
			print('From html.parser')
			# if len(vars(product).keys())==0:
			# 	return 0
			# else:

			pprint(vars(product))
			# return(vars(product))
			return product2database,seller2database

		except TypeError:
			logger.info('Nothin found in : {}'.format(link))
			
			# # product2database=(product.title,product.ASIN,product_category,cat_link,product.list_price,product.page_price,product.stars,product.no_of_reviews,
			# # 				product.link,product.other_offers_link,product.other_offers_count,product.seller_id,product.availability,product.remarks,p_scrapped_date_time)
			# # seller2database=(product.page_seller,product.page_seller_link,product.seller_id)
			# # logger.info('Product={} \n Seller={}'.format(product2database,seller2database))
			# print('From lxml')
			# logger.info(vars(product))
			# return(vars(product))

			# return product2database,seller2database
			# return product.page_price



# get_product_details('https://www.amazon.ae/dp/B07N6Q2T72','')
# print('='*30)
# get_product_details('https://www.amazon.ae/Samsung-Galaxy-M20-Dual-SIM/dp/B07QZ3VP6Z/','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07TV7KMGH','') #MKLLYNG Newborn
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07SNG23JW','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07QZ3VP6Z','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B01H2RBQUG','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07JFQKR5G','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B01NA0JSVC','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07NDRG8RY','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07SW7FZLP','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B0795DZFQV','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B076CWS8C6','')
# print('='*30)

# get_product_details('https://www.amazon.ae/dp/B07B48YDNX','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07F1RRQXQ','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B01KNVF4SI','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07MTW7C9R','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B019FPLDIS','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B01LWIKZB3','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07GZ5MXCC','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07PZSNLV2','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B01G61RLBM','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B01KF0FJX2','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B074DYBQ9L','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07M835HJM','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07N6Q2T72','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07NTYFV69','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07Q24W4CW','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B07P13J8DK','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B01B1WBDYM','')
# print('='*30)
# get_product_details('https://www.amazon.ae/dp/B014H2T84K','') #no desktop_unifiedPrice
