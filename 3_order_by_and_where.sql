use sql_store;

select * from customers;
select first_name, last_name, points
from customers;

-- order by 

select first_name, last_name, points
from customers
order by points desc;

-- where
-- select all customers born after 1989 with points highest to lowest
select first_name, last_name, points, birth_date
from customers
where birth_date < '1990-01-01' -- dates need to be shown like this
order by points desc;

-- we can alter fields as well

select first_name, last_name, points, points/100, birth_date -- will produce a column of points divided by 100
from customers;

-- aliasing (name the new altered column)

select first_name, last_name, points, points/100 as divide_by_100, birth_date 
from customers;

select * from order_items;
-- give customers a 5% discount
select product_id, quantity, unit_price, quantity*unit_price as price,
round(quantity*unit_price*0.95,2) as discounted_price
from order_items;

-- exercise 1: write a query to return all the products in the database, their name, unit price, and 5% discount

select * from products;
select name, unit_price, round(unit_price*.95,2) as discounted_unit_price
from products;

-- distinct 

select distinct state from customers; -- compare this to removing "distinct" and you'll see that states like FL appear twice

-- where clauses in detail

select * from customers
where points > 2000; -- this is called a comparison operator. there's < <= > >= !=

select * from customers where state = 'VA';

-- exercise 2: return orders made before 2019

select * from orders;
select * from orders where order_date < '2019-01-01';