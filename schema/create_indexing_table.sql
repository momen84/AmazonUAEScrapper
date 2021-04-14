CREATE TABLE IF NOT EXISTS crawler_index (
									id integer PRIMARY KEY,
									cat_name text,
									main_cat_link text,
									cat_link text,
									cat_link_code text,
									cat_link_pref text,
									cat_page_number integer,
									scrapped_date_time text,
									status text
								
								);
