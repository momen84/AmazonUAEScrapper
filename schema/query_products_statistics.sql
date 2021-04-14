select p_category,count(p_ASIN) from products group by p_category order by count(p_ASIN) desc;
