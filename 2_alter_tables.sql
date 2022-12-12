

-- test this edit
--show how to use not null, unique, etc

use test1_db;

drop table persons;
create table persons (
			ID int not null default 100, -- having a default prevents an error here
            first_name varchar(8) not null,
            last_name varchar(8) null,
            -- null means they can leave it blank, not null means they can't
            age int null,
            unique(ID)
            );

insert into persons(first_name, last_name, age)
values ('Carl', 'Resnick', 25)

select * from persons;

-- Primary Key

create table customers(
			name varchar(10),
            product varchar(10),
            product_id int,
            primary key(product_id)
            );

select * from customers;

-- alter existing table (adding a constraint)

alter table persons
add primary key (ID)


create table passengers(
			first_name varchar(10),
            last_name varchar(10),
            mobile int,
            ticket_number varchar(5)
            );
            
select * from passengers

alter table passengers
add constraint UC_passengers unique(mobile, ticket_number);

alter table passengers
drop index UC_passengers

-- foreign key

create table customers2 (
			customer_id int not null,
            first_name varchar(10),
            last_name varchar(10),
            age int,
            primary key (customer_id)
            );
            
create table orders(
			order_id int not null,
            order_number int not null,
            customer_id int, -- this is from the customers2 table
            primary key (order_id),
            foreign key (customer_id) references customers2 (customer_id)
            );