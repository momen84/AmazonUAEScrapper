 CREATE TABLE IF NOT EXISTS products (
                                        id integer PRIMARY KEY,
                                        p_name text NOT NULL,
                                        p_ASIN text NOT NULL UNIQUE ON CONFLICT IGNORE,
                                        p_category text,
                                        cat_page text,
                                        p_list_price real,
                                        p_page_price real,
                                        p_link text,
                                        p_other_offers_link text,
                                        p_other_offers_count integer,
                                        p_reviews text,
                                        p_review_count integer,
                                        p_seller_id text,
										p_availability text,
                                        p_remarks text,
										p_color_variants text,
										p_size_varinats text,
										p_style_variants text,
										p_scrapped_date_time text
                                    );


