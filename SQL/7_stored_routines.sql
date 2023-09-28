/* Stored routines is a statement or series of statements that can be stored on the database server.
For example, what if you need to execute a query every day..do you want to rewrite that code every day?
Stored routines are kind of like macro shortcuts but more customized. 
Within stored routines, you have stored procedures and functions.
Functions include built-in functions (like aggregate functions avg(), count(), etc) or user-created ones. */

-- stored routines
-- first: we need a delimiter (for us, it'll be $$) because using a plain semicolon will stop the routine after the first query (when in reality, you might want many queries)

use employees_mod;
drop procedure if exists select_employees;
delimiter $$
create procedure select_employees()
begin
select * from employees limit 1000;
end$$
delimiter ;
call employees_mod.select_employees();

-- exercise: create stored procedure that provides avg salary of all employees
drop procedure if exists avg_salary;
delimiter $$
create procedure avg_salary()
begin
select avg(salary)
from salaries s
inner join employees e on s.emp_no = e.emp_no;
end$$
delimiter ;
call avg_salary;

-- stored procedure that can take an input value
drop procedure if exists emp_salary;
delimiter $$
create procedure emp_salary(in p_emp_no integer)
begin
select e.first_name, e.last_name, s.salary, s.from_date, s.to_date
from employees e 
join salaries s on e.emp_no = s.emp_no
where e.emp_no = p_emp_no;
end$$
delimiter ;
call employees_mod.emp_salary(11300);

-- aggregate function with stored procedure
drop procedure if exists emp_avg_salary;
delimiter $$
create procedure emp_avg_salary(in p_emp_no integer)
begin
select e.first_name, e.last_name, avg(s.salary)
from employees e 
join salaries s on e.emp_no = s.emp_no
where e.emp_no = p_emp_no
group by(e.emp_no);
end$$
delimiter ;
call employees_mod.emp_avg_salary(11300);

-- output parameter
drop procedure if exists emp_avg_salary_out;
delimiter $$
create procedure emp_avg_salary_out(in p_emp_no integer, out p_avg_salary decimal(10,2))
begin
select avg(s.salary) -- we only want to store avg salary, so our select statement is shortened
into p_avg_salary
from employees e 
join salaries s on e.emp_no = s.emp_no
where e.emp_no = p_emp_no;
end$$
delimiter ;
set @p_avg_salary = 0;
call employees_mod.emp_avg_salary_out(11300, @p_avg_salary);
select @p_avg_salary;

-- exercise: paramaters first/last name of individual, return their employee number
drop procedure if exists emp_info;
delimiter $$
create procedure emp_info(in z_first_name varchar(20), in z_last_name varchar(20), out z_emp_no int)
begin
select e.emp_no -- we only want to store avg salary, so our select statement is shortened
into z_emp_no
from employees e 
where e.first_name = z_first_name and e.last_name = z_last_name;
end$$
delimiter ;
set @z_emp_no = 0;
call emp_info('aruna','journel', @z_emp_no); -- input is called an argument, and the output is called the variable
select @z_emp_no; -- I messed up. I should label parameters with p, not some random letter like z

select * from employees limit 10;

-- @ indicates this is a variable. the v is also a good indicator when structuring code
set @v_avg_salary = 0;
call employees_mod.emp_avg_salary_out(11300, @v_avg_salary);
select @v_avg_salary;

-- difference between functions and stored procedures?
/* functions: everything within the parenthesis is "in". The equivalent of "out" aka output is a "return value" statement. */
drop function if exists f_emp_avg_salary;
delimiter $$
create function f_emp_avg_salary (p_emp_no integer) returns decimal(10,2) deterministic -- weird SQL syntax needed to run function
begin
declare v_avg_salary decimal(10,2); -- declare is the equivalent of "set" when creating the variable
select avg(s.salary) -- we only want to store avg salary, so our select statement is shortened
into v_avg_salary
from employees e 
join salaries s on e.emp_no = s.emp_no
where e.emp_no = p_emp_no;
return v_avg_salary;
end$$
delimiter ;
select f_emp_avg_salary(11300);

-- exercise: turn emp_info stored procedure into a function, but returns salary from newest contract date
drop function if exists emp_info;
delimiter $$
create function emp_info(p_first_name varchar(20), p_last_name varchar(20)) returns decimal(10,2) deterministic
begin
declare v_salary decimal(10,2);
declare v_max_from_date date;
select max(from_date) -- we only want to store avg salary, so our select statement is shortened
into v_max_from_date
from salaries s
join employees e on e.emp_no = s.emp_no
where e.first_name = p_first_name and e.last_name = p_last_name;
select s.salary
into v_salary
from salaries s
join employees e on e.emp_no = s.emp_no
where e.first_name = p_first_name
and e.last_name = p_last_name
and s.from_date = v_max_from_date;
return v_salary;
end$$
delimiter ;
select emp_info('aruna','journel'); -- input is called an argument, and the output is called the variable
-- verify
select e.first_name, e.last_name, s.salary, s.from_date
from employees e
join salaries s on e.emp_no = s.emp_no
where e.last_name = 'journel' and e.first_name = 'aruna';

/* Conceptual difference between stored procedure and user-defined function:
1. Stored procedures can have multiple return values, while functions only have one. Thus, if you need more than one value as a result, use a procedure
2. With insert/update/deletes, always use stored procedure
3. You can call a function in a select statement. Impossible to do for stored procedure. */
-- example of #3
set @v_emp_no = 11300;
select emp_no, first_name, last_name, f_emp_avg_salary(@v_emp_no) as avg_salary
from employees
where emp_no = @v_emp_no;