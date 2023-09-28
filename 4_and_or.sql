-- and, or, and not operators

select * from customers
where birth_date > '1990-01-01' and city = 'Chicago'; -- compare to changing 'and' to 'or'

select * from customers
where birth_date > '1990-01-01' or city = 'Chicago'; -- compare to changing 'and' to 'or'

-- not

select * from customers
where not (birth_date > '1990-01-01' or city = 'Chicago' and points < 1000); 

-- exercise 3: from order_items table, get the items: for order #6, where total price is >$20, and display the unit price
select * from order_items;
select order_id, quantity, unit_price, quantity*unit_price as total_price from order_items
where order_id = 6 and quantity*unit_price >20; -- I had errors here when I tried to use the "total_price" name. curious why we can't use the name if we've just defined it in the select statement

-- in 

select* from customers
where state = 'VA' or state= 'FL' or state = 'GA'; -- if you have a lot of categories, this gets way too tedious

select * from customers 
where state in ('FL','VA','GA'); -- this is more efficient

-- exercise 4: return products with quantity in stock equal to 49, 38, and 72
select * from products
where quantity_in_stock in (38,49,72);

-- where

select * from customers
where points >= 1000 and points <= 3000; -- again, not very efficient

select * from customers
where points between 1000 and 3000;

-- exercise 5: return customers born between 1/1/1990 and 1/1/2000

select * from customers
where birth_date between '1990-01-01' and '2000-01-01';

-- like 

select * from customers
where last_name like 'b%' -- return customers who's last name starts with b

select * from customers
where last_name like '%b%'; -- return customers who have a 'b' in their last name

-- exercise 6: return customers whose addresses contain 'trail' or 'avenue' or phone numbers end with 9
select * from customers
where address like '%trail%' or address like '%avenue%' or phone like '%9';

-- regexp: regular expression
select * from customers
where last_name regexp 'b'; -- produces the same result as "select * from customers where last_name like '%b%'"

select * from customers
where last_name regexp '^b'; -- customers whose last names start with 'b'

select * from customers
where last_name regexp 'y$'; -- customers whose last names end with 'y'

select * from customers
where last_name regexp'y|s|z'; -- customers whose last names contain 'y' or 's' or 'z'

select * from customers -- customers whose last name contain 'e', but are preceeded by a 'g', 's', or 'i'
where last_name regexp '[gsi]e';

select * from customers
where last_name regexp 'c[ea]'; -- customers whose last name contains 'c' and is followed by 'e' or 'a'

select * from customers
where last_name regexp 's[e-i]'; -- customers whose last name contains 's' and is followed by any letter from 'e' to 'i'

-- summary of regexp
-- ^ is beginning of a string
-- $ is end of a string
-- | is logical OR
-- [a,b,d] is combo of characters before or after a letter

-- exercise 7: return customers whose a) first names are elka or ambur, b) last names end with EY or ON, 
-- c) last names start with MY or contains SE d) last names contain b followed by r or u

select * from customers
where first_name regexp 'Elka|Ambur';

select * from customers
where last_name regexp 'ey$|on$';

select * from customers
where last_name regexp '^my|se';

select * from customers
where last_name regexp 'b[ru]';

