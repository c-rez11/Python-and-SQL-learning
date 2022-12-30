create database if not exists sales;

use sales; 

-- String Data Types
-- char(5) signifies a variable with a fixed character count of 5
-- varchar(5) signifies a variable with a max character count of 5, but can be lower. Varchar is about 50% faster than char
-- enum('M','F') defines a set list of options, and will produce an error if one of the defined options is not input

-- Integer Data Types
-- different byte sizes depending on the range of integers we want. For example, "tinyint" has storage of 1 byte and has a range of ~250 integers, 
-- while "int" has a storage of 4 bytes and has a range of 4 billion integers

-- Blob: allows storage of certain file types (Excel docs, jpegs, etc) within the DB

-- create table 
-- need format: (column_1 data_type constraints, column_2 data_type constraints)
drop table sales -- added this once table was initially created
create table sales
(
	purchase_number int not null primary key auto_increment, -- auto-increment creates automatic spacing (1,2,3 etc)
    date_of_purchase date not null,
    customer_id int,
    item_code varchar(10) not null,
    primary key (purchase_number),
/* foreign key (customer_id) references customers(customer_id) on delete cascade -- this comment is used by SQL pros. It means that if a specific value from the parent table's primary key 
	has been deleted, all the records from the child table referring to this value will be removed as well.
    );*/
    
alter table sales
add foreign key (customer_id) references customers(customer_id) on delete cascade; -- this is the better way to do the commented-out same thing above

alter table sales
drop foreign key sales_ibfk_1;

create table customers
(
	customer_id INT auto_increment,
    first_name varchar(255),
    last_name varchar(255),
    email_address varchar(255),
    number_of_complaints int,
    primary key (customer_id)
    -- unique key (email_address)
    );

alter table customers
change column number_of_complaints number_of_complaints int default 0;

insert into customers (first_name, last_name, gender)
values ('Peter','Figaro','M');

    
    -- exercise 54: add the following
alter table customers
add column gender enum('M','F') after last_name;
    
insert into customers (first_name, last_name, gender, email_address, number_of_complaints)
values('John', 'McKinley', 'M', 'john.mckinley@365careers.com',0);

select * from customers;
    
    
    
alter table customers -- drop unique key
drop index email_address;
    
create table items
(
	item_code varchar(255),
    item varchar(255),
    unit_price numeric(10,2),
    company_id varchar(255),
    primary key (item_code)
    );
    
create table companies
(
	company_id varchar(255),
    company_name varchar(255) not null,
    headquarters_phone_number varchar(255) default "X",
    primary key (company_id),
    unique key (headquarters_phone_number)
    );
    
drop table sales;
drop table customers;
drop table items;
drop table companies;