-- using the "employees" database
use employees;
select first_name, last_name from employees;
select dept_no from departments;

-- where
select * from employees where first_name = 'Denis';

-- and
select * from employees where first_name = 'Denis' and gender = 'M';

-- or
select * from employees where first_name = 'Denis' or first_name = 'Elvis';

-- operator precedence: SQL will always read the AND conditions before the OR
select * from employees where first_name = 'Denis' and gender = 'M' or gender = 'F';
select * from employees where first_name = 'Denis' and (gender = 'M' or gender = 'F'); -- handle operator precedence by adding parenthesis

-- exercise: retrieve a list with all female employees whose first name is either Kelllie or Aruna
select * from employees where gender = 'F' and (first_name = 'Kellie' or first_name = 'Aruna')

-- in, not in: avoids using lots of 'and'/'or' statements
select * from employees where first_name in ('Cathie','Mark','Nathan'); -- this is also a much quicker retrieve for the CPU
-- not in works the same way


-- like, not like

select * from employees where first_name like ('Mar%'); -- the % represents a substitute for a sequence of characters
select * from employees where first_name like ('Mar_'); -- the _ represents the exact amount of characters you're looking for after 'Mar'
select * from employees where first_name like ('%mar%'); -- this allows for names like 'Mark' and 'Omar', as we don't specify where the combo of 'mar' should be in the name

/* exercise 87: Working with the “employees” table, use the LIKE operator to select the data about all individuals, whose first name starts with “Mark”; specify that the name can be succeeded by any sequence of characters.

Retrieve a list with all employees who have been hired in the year 2000.

Retrieve a list with all employees whose employee number is written with 5 characters, and starts with “1000”. */

select * from employees where first_name like ('Mark%');
select * from employees where hire_date like ('2000-%');
select * from employees where emp_no like ('1000_');

-- % _ * are called wildcard characters

-- between

select * from employees where hire_date between '1990-01-01' and '2000-01-01';
-- note: this is INCLUSIVE of the between values. To remove the values of 1/1/1990 and 1/1/2000, use "not between"

-- is not null / is null
select * from employees where first_name is not null;
select * from employees where first_name is null; -- good way to search if you have null values

-- distinct
select distinct gender from employees; -- only distinct values (M,F) are returned

-- aggregate functions like count() and sum()
-- how many employees are in our database?
select count(emp_no) from employees;
-- how many different first names are there?
select count(distinct first_name) from employees;
select count(*) from salaries where salary >= 150000;
-- order by
select * from employees order by first_name desc; -- "asc" is default
select * from employees order by emp_no; -- works for numbers too
select* from employees order by last_name, first_name; -- handles multiple ordering queries

-- group by (IMPORTANT)
-- placed immediately after where clause, and before order by

-- example: how many times does a given first name appear in our database?
select first_name, count(first_name) from employees group by first_name;

-- alias
-- names like count(first_name) are ugly and unprofessional. Use alias to change that
select first_name, count(first_name) as names_count from employees
group by first_name order by first_name
-- exercise 112: Write query with 2 columns. First column: salaries higher than 100k. Second column: # of employees at each of those salaries. Sort by first column.
select salary, count(emp_no) as emps_with_same_salary from salaries where salary >= 100000 group by salary order by salary;

-- having
-- funtions like 'where' function, but used with aggregate functions
select first_name, count(first_name) as names_count from employees group by first_name having count(first_name)>250 order by first_name;

-- exercise: find all employees whose average salary is higher than 120k annually
select *, avg(salary) as average_salary from salaries where avg(salary) > 120000 group by emp_no order by emp_no;
select emp_no, avg(salary) as average_salary from salaries group by emp_no having avg(salary)>120000 order by emp_no; -- can't use * as all-encompassing because emp_no needs to be specifically mentioned because of group by function
-- having and where can be used together, but don't use having with both aggregated and non-aggregated data
-- exercise 119: select employee numbers who have signed more than 1 contract after 1/1/2000.
 select emp_no, count(dept_no) from dept_emp where from_date > '2000-01-01' group by emp_no having count(from_date)>1 order by emp_no;
 -- limit
 select * from employees order by last_name limit 10;