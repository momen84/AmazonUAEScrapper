import sqlite3
from sqlite3 import Error
import os
import logging


logging.basicConfig(level=logging.DEBUG, filename='a_scrapping.log',format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


version='V0_9'
db_file_name='amazon%s.db'%version
#Local

local_dir="/home/momen/Desktop/GC/amazon/"

local_dir_dict={'local_db_file':'DB/'+db_file_name,'local_crawler_index_schema_file':'%s/schema/create_indexing_table.sql'%version,
				'local_create_index_record_file':'%s/schema/create_index_record.sql'%version,'local_update_crawler_index_file':'%s/schema/update_index_record.sql'%version,
				'local_products_schema_file':'%s/schema/create_products_table.sql'%version,'local_create_product_schema_file':'%s/schema/create_product.sql'%version,
				'local_sellers_schema_file':'%s/schema/create_sellers_table.sql'%version,'local_create_seller_schema_file':'%s/schema/create_seller.sql'%version,}




local_db_file="/home/momen/Desktop/GC/amazon/DB/amazonv0_7.db"
local_crawler_index_schema_file='/home/momen/Desktop/GC/amazon/V0.9/schema/create_indexing_table.sql'
local_create_index_record_file='/home/momen/Desktop/GC/amazon/V0.9/schema/create_index_record.sql'
local_update_crawler_index_file='/home/momen/Desktop/GC/amazon/V0.9/schema/update_index_record.sql'

local_products_schema_file='/home/momen/Desktop/GC/amazon/V0.9/schema/create_products_table.sql'
local_create_product_schema_file='/home/momen/Desktop/GC/amazon/V0.9/schema/create_product.sql'

local_sellers_schema_file='/home/momen/Desktop/GC/amazon/V0.9/schema/create_sellers_table.sql'
local_create_seller_schema_file='/home/momen/Desktop/GC/amazon/V0.9/schema/create_seller.sql'
#For Flask
local_query_products_schema_file='/home/momen/Desktop/GC/amazon/V0.9/schema/query_total_products_count.sql'
local_query_sellers_schema_file='/home/momen/Desktop/GC/amazon/V0.9/schema/query_total_sellers_count.sql'
local_query_products_statistics_file='/home/momen/Desktop/GC/amazon/V0.9/schema/query_products_statistics.sql'


#Gcloud

gc_dir="/home/momen/amazon/"

gc_dir_dict={'gc_db_file':"DB/amazonv0_7.db",
			'gc_crawler_index_schema_file':'schema/create_indexing_table.sql',
			'gc_create_index_record_file':'schema/create_index_record.sql',
			'gc_update_crawler_index_file':'schema/update_index_record.sql',

			'gc_products_schema_file':'schema/create_products_table.sql',
			'gc_create_product_schema_file':'schema/create_product.sql',

			'gc_sellers_schema_file':'schema/create_sellers_table.sql',
			'gc_create_seller_schema_file':'schema/create_seller.sql'}


gc_db_file="/home/momen/amazon/DB/amazonv0_7.db"
gc_crawler_index_schema_file='/home/momen/amazon/schema/create_indexing_table.sql'
gc_create_index_record_file='/home/momen/amazon/schema/create_index_record.sql'
gc_update_crawler_index_file='/home/momen/amazon/schema/update_index_record.sql'

gc_products_schema_file='/home/momen/amazon/schema/create_products_table.sql'
gc_create_product_schema_file='/home/momen/amazon/schema/create_product.sql'

gc_sellers_schema_file='/home/momen/amazon/schema/create_sellers_table.sql'
gc_create_seller_schema_file='/home/momen/amazon/schema/create_seller.sql'
#for Flask
gc_query_products_schema_file='/home/momen/amazon/schema/query_total_products_count.sql'
gc_query_sellers_schema_file='/home/momen/amazon/schema/query_total_sellers_count.sql'
gc_query_products_statistics_file='/home/momen/amazon/schema/query_products_statistics.sql'

def check_local_or_cloud():
	logger.info('Checking local or cloud')
	working_dir_structure={}
	if os.path.exists("/home/momen/Desktop/GC/amazon/DB/"):
		logging.info('Local setup detected')
		print('Local setup detected')
		# for key,value in local_dir_dict.items():
		# 	working_dir_structure[key]=os.path.join(local_dir,value)
			# key=os.path.join(local_dir,value)

		db_file=local_db_file
		crawler_index_schema_file=local_crawler_index_schema_file
		create_index_record_file=local_create_index_record_file
		update_crawler_index_file=local_update_crawler_index_file
		products_schema_file=local_products_schema_file
		create_product_schema_file=local_create_product_schema_file
		sellers_schema_file=local_sellers_schema_file
		create_seller_schema_file=local_create_seller_schema_file

		query_products_schema_file=local_query_products_schema_file
		query_sellers_schema_file=local_query_sellers_schema_file
		query_products_statistics_file=local_query_products_statistics_file
	else:
		logger.info('Cloud setup detected')
		print('Cloud setup detected')
		# pass
		# for key,value in gc_dir_dict.items():
		# 	working_dir_structure[key]=os.path.join(gc_dir,value)
			# key=os.path.join(local_dir,value)
		
		db_file=gc_db_file
		crawler_index_schema_file=gc_crawler_index_schema_file
		create_index_record_file=gc_create_index_record_file
		update_crawler_index_file=gc_update_crawler_index_file
		products_schema_file=gc_products_schema_file
		create_product_schema_file=gc_create_product_schema_file
		sellers_schema_file=gc_sellers_schema_file
		create_seller_schema_file=gc_create_seller_schema_file

		query_products_schema_file=gc_query_products_schema_file
		query_sellers_schema_file=gc_query_sellers_schema_file
		query_products_statistics_file=gc_query_products_statistics_file
	# print(working_dir_structure)
	# return working_dir_structure.values()
	return db_file,crawler_index_schema_file,create_index_record_file,\
			update_crawler_index_file,products_schema_file,create_product_schema_file,\
			sellers_schema_file,create_seller_schema_file,query_products_schema_file,\
			query_sellers_schema_file,query_products_statistics_file

# print(check_local_or_cloud())
try:

	db_file,crawler_index_schema_file,create_index_record_file,update_crawler_index_file,products_schema_file,\
	create_product_schema_file,sellers_schema_file,create_seller_schema_file,query_products_schema_file,query_sellers_schema_file,query_products_statistics_file=[x for x in check_local_or_cloud()]

except:
	logger.error('Could not setup database')

# print(db_file,crawler_index_schema_file,create_index_record_file,update_crawler_index_file,products_schema_file,create_product_schema_file,sellers_schema_file,create_seller_schema_file)



def create_connection(db_file):
	""" create a database connection to a SQLite database """
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)

	return None
	# finally:
	# 	conn.close()

def query_products_statistics():
	conn = create_connection(db_file)
    # print(product)

	with open(query_products_statistics_file) as query_products_statistics:
		sql_query_products_statistics=query_products_statistics.read()
	with conn:
		try:
			c = conn.cursor()
			c.execute(sql_query_products_statistics)
			return c.fetchall()
		except Error as e:
			print(e)



def query_products():
	conn = create_connection(db_file)
    # print(product)

	with open(query_products_schema_file) as query_products:
		sql_query_products=query_products.read()
	with conn:
		try:
			c = conn.cursor()
			c.execute(sql_query_products)
			return c.fetchone()[0]
		except Error as e:
			print(e)

def query_sellers():
	conn = create_connection(db_file)
    # print(product)

	with open(query_sellers_schema_file) as query_sellers:
		sql_query_sellers=query_sellers.read()
	with conn:
		try:
			c = conn.cursor()
			c.execute(sql_query_sellers)
			return c.fetchone()[0]
		except Error as e:
			print(e)


	
def create_product(product):

	conn = create_connection(db_file)
    # print(product)

	with open(create_product_schema_file) as create_product_schema:
		sql_create_product=create_product_schema.read()
	with conn:
		try:
			c = conn.cursor()
			c.execute(sql_create_product,product)
			
		except Error as e:
			print(e)
	return c.lastrowid

def create_seller(seller):
	conn = create_connection(db_file)
	# print(seller)
	with open(create_seller_schema_file) as create_seller_schema:
		sql_create_seller=create_seller_schema.read()
	with conn:
		try:
			c = conn.cursor()
			c.execute(sql_create_seller, seller)
		except Error as e:
			print(e)
	# conn.commit()

	return c.lastrowid

def create_products_table():#, create_table_sql):
	
	conn = create_connection(db_file)
	with open(products_schema_file) as products_schema:
		sql_create_products_table=products_schema.read()
	try:
		c = conn.cursor()
		c.execute(sql_create_products_table)
	except Error as e:
		print(e)



def create_sellers_table():#, create_table_sql):
	conn = create_connection(db_file)
	with open(sellers_schema_file) as sellers_schema:
		sql_create_sellers_table=sellers_schema.read()
	try:
		c = conn.cursor()
		c.execute(sql_create_sellers_table)
	except Error as e:
		print(e)

def create_crawler_table():
	conn = create_connection(db_file)
	with open(crawler_index_schema_file) as crawler_schema:
		sql_crawler_index_table=crawler_schema.read()
	try:
		c = conn.cursor()
		c.execute(sql_crawler_index_table)

	except Error as e:
		print(e)



def create_crawler_record(crawler_record):
	# print(crawler_record)
	conn = create_connection(db_file)
	with open(create_index_record_file) as create_record:
		create_index_record=create_record.read()
	try:
		with conn:
			c = conn.cursor()
			c.execute(create_index_record,crawler_record)
	except Error as e:
		print(e)

def check_crawler_record(crawler_record):
	conn = create_connection(db_file)
	print('='*20+'Crawler Record'+'='*20)
	print(crawler_record)
	print('='*20)
	# print(query)
	with conn:
		c = conn.cursor()
		#c.execute(''' SELECT cat_link FROM crawler_index ORDER BY id DESC LIMIT 1;''')
		c.execute('''SELECT cat_link_code FROM crawler_index where cat_link_code =? and cat_page_number=? order by id asc limit 1;''',(crawler_record[3],crawler_record[4]))
		# print(c.fetchone())
		try:
			return c.fetchone()[0]
		except:
			return None


def check_last_crawler_link():
	conn = create_connection(db_file)
	with conn:
		c = conn.cursor()
		#c.execute(''' SELECT cat_link FROM crawler_index ORDER BY id DESC LIMIT 1;''')
		c.execute('''SELECT main_cat_link FROM crawler_index where status is 'Not scrapped' order by id desc limit 1;''')
		# print(c.fetchone())
		try:
			return c.fetchone()[0]
		except:
			return None


def update_crawler_index(crawler_record):
	conn = create_connection(db_file)
	cat_link=crawler_record[1]
	status='Scrapped'
	with open(update_crawler_index_file) as update_index:
		update_index_record=update_index.read()
	try:
		with conn:
			c = conn.cursor()
			c.execute(update_index_record,(crawler_record[1],crawler_record[2]))
	except Error as e:
		print(e)

def rescrap_get_links():
	conn = create_connection(db_file)

	with conn:
		c = conn.cursor()
		c.execute(''' SELECT p_link FROM products''')
		return c.fetchall()
		
	

def check_tables_exists():
	logger.info('Check database tables')
	conn = create_connection(db_file)

	with conn:
		c = conn.cursor()
		c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='products' ''')
		
					
		#if the count is 1, then table exists
		if c.fetchone()[0]==1 :#and c2.fetchone()[0]==1:
			print('Products table exists.')
			logger.info('Products table exists.')
		else:
			logger.info('Products table does not exist , Creating products table')
			create_products_table()
			print('Products table created')
			logger.info('products table created')
			
	
		c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='sellers' ''')
		
		if c.fetchone()[0]==1 :
			print('Sellers Table exists.')
			logger.info('Sellers table exists.')
			
		else:
			logger.info('Sellers table does not exist , Creating sellers table')
			create_sellers_table()
			print('Sellers table created')
			logger.info('sellers table created')


		c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='crawler_index' ''')
		
		if c.fetchone()[0]==1 :
			logger.info('Crawler table exists.')
			print('Crawler index Table exists.')
	
		else:
			logger.info('Crawler table does not exist , Creating sellers table')
			create_crawler_table()
			print('Crawler Index table created')
			logger.info('crawler_index table created')
	# return db_file

def check_product_exists_bulk(bulk_asin):
	# print(bulk_asin)
	conn = create_connection(db_file)
	c=conn.cursor()
	c.execute(''' SELECT p_ASIN FROM products WHERE p_ASIN in (%s)''' %','.join('?'*len(bulk_asin)),bulk_asin)
	

	# if c.fetchall() is None:
	return c.fetchall()
		# return 'Add All'
	# elif c.fetchall() is not None:
		# print(c.fetchall())
		# return c.fetchall()
		
		# c.execute(''' SELECT p_ASIN FROM products WHERE p_ASIN not in (%s)''' %','.join('?'*len(bulk_asin)),bulk_asin)
		# print(c.fetchall())
		# for asin in bulk_asin:
		# 	check_product_exists(asin)
		# 	if check_product=='Add':
		# 		logger.info('check_product={}'.format(check_product))
		# 		with conn:
		# 			logger.info('New product, adding to database')
		# 			product_id = create_product(product)
		# 			print("Added {} products".format(product_id))
		# 			logger.info('New product successfully added to database')

def check_product_exists(asin):
	conn = create_connection(db_file)
	c=conn.cursor()
	c.execute(''' SELECT * FROM products WHERE p_ASIN=?''',(asin,))
	# print(c.fetchone())
	if c.fetchone() is None:
	# if c.fetchone()[0]==0 or c.fetchone()[0] is None:
		return 'Add'
	else:
		return 'Do not add'

def check_seller_exists(seller_id):
	# print(seller_id)
	conn = create_connection(db_file)
	c=conn.cursor()
	c.execute(''' SELECT * FROM sellers WHERE seller_id=?''',(seller_id,))
	# print(c.fetchone())
	if c.fetchone() is None:
	# if c.fetchone()[0]==0 or c.fetchone()[0] is None:
		return 'Add'
	else:
		return 'Do not add'

def get_sellers_for_seller_scrapper():
	conn = create_connection(db_file)
	c=conn.cursor()
	c.execute(''' SELECT p_seller_id FROM products where p_seller_id not null''')
	# print(c.fetchone())
	return c.fetchall()
	


def add_record(product,seller):
	logger.info('Adding all product/seller pair to products database')
	conn = create_connection(db_file)
	asin=product[1]
	seller_id=seller[-1]
	# print(seller_id)
	if conn is not None:
		# logger.info('check_product_exists({})'.format(asin))
		# check_product=check_product_exists(asin)
		# logger.info('check_seller_exists({})'.format(seller_id))
		check_seller=check_seller_exists(seller_id)
		# if check_product=='Add':
		# 	logger.info('check_product={}'.format(check_product))
		with conn:

		# product = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
			# product=('Xiaomi Mi 9T 6GB 128GB LTE Smartphone - Glacier Blue','B07TPF69RZ',1299.00,1296.00,'https://www.amazon.ae/gp/offer-listing/B07TPF69RZ/ref=dp_olp_new?ie=UTF8&condition=new')
			logger.info('New product, adding to database')
			product_id = create_product(product)
			print("Added {} products".format(product_id))
			logger.info('New product successfully added to database')
		# elif check_product=='Do not add':
		# 	logger.info('check_product={}'.format(check_product))
		# 	logger.info('product existing in database....pass')
		# 	print('Product {} exists'.format(asin))
		
		if check_seller=='Add':
			with conn:
				logger.info('check_seller={}'.format(check_seller))
			# product = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
				# product=('Xiaomi Mi 9T 6GB 128GB LTE Smartphone - Glacier Blue','B07TPF69RZ',1299.00,1296.00,'https://www.amazon.ae/gp/offer-listing/B07TPF69RZ/ref=dp_olp_new?ie=UTF8&condition=new')
				seller_count = create_seller(seller)
				logger.info('New seller, adding to database')
				print("Added {} sellers".format(seller_count))
				logger.info('New seller successfully added to database')
		elif check_seller=='Do not add':
			print('Seller {} exists'.format(seller_id))

	
	else:
		logger.error("Error! cannot create the database connection.")
		print("Error! cannot create the database connection.")



