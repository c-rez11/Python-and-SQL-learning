-- using the "employees" database

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
