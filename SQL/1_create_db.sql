
-- now from my desktop
-- create database test1_db
-- creating tables

use test_db;
create table students (roll_no int, name varchar(10), age int, phone int);

select *
from students;

insert into students 
values
-- (1, "Jacob", 23, 1111111)
(1, "Jacob", 23, 1111111),
(1, "Finn", 24, 2222222);