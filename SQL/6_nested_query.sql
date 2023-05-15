-- subquery, or nested query
-- select first/last name from emp_no that are found in department manager table
select e.first_name, e.last_name
from employees e
where e.emp_no in (select dm.emp_no from dept_manager dm); -- subquery should always be in parenthesis
-- exercise: select all dept managers hired between 1/1/990 and 1/1/1995
select e.emp_no, e.first_name, e.last_name, e.hire_date
from employees e 
where e.emp_no in (select dm.emp_no from dept_manager dm where e.hire_date between '1990-01-01' and '1995-01-01');

-- exists / not exists
select e.first_name, e.last_name
from employees e 
where exists (select * from dept_manager dm where dm.emp_no = e.emp_no);
/* Difference between this and the "in" function? Exists is quicker for large amounts of data because it's just looking for true/false boolean. */
-- exercise: all employees whose job title is "assistant engineer"
select * 
from employees e
where e.emp_no in (select t.emp_no from titles t where t.emp_no = e.emp_no and title = "Assistant Engineer");

-- exercise: assign employee number 110022 as manager for employees 10001-10020 and manager 110039 to employees 10021-10040
select A.*
from (select e.emp_no as employee_ID, min(de.dept_no) as department_code,
(select emp_no
from dept_manager
where emp_no = 110022) as manager_ID
from employees e 
join dept_emp de on e.emp_no = de.emp_no
where e.emp_no <= 10020
group by e.emp_no
order by e.emp_no) as A
union select B.* -- union of these two subsets is our answer
from (select e.emp_no as employee_ID, min(de.dept_no) as department_code,
(select emp_no
from dept_manager
where emp_no = 110039) as manager_ID
from employees e 
join dept_emp de on e.emp_no = de.emp_no
where e.emp_no > 10020
group by e.emp_no
order by e.emp_no
limit 20) as B;

-- exercise
-- setup
drop table if exists emp_manager;
create table emp_manager (
emp_no int(11) not null, dept_no varchar(4) null, manager_no int(11) not null);

-- exercise: fill emp_manager with data about employees, their dept_no, and their manager
-- subsets A and B: same code as above

 -- comment this out unless warranted: insert into emp_manager
select U.*
from 
(select A.*
from (select e.emp_no as employee_ID, min(de.dept_no) as department_code,
(select emp_no
from dept_manager
where emp_no = 110022) as manager_ID
from employees e 
join dept_emp de on e.emp_no = de.emp_no
where e.emp_no <= 10020
group by e.emp_no
order by e.emp_no) as A
union select B.* -- union of these two subsets is our answer
from (select e.emp_no as employee_ID, min(de.dept_no) as department_code,
(select emp_no
from dept_manager
where emp_no = 110039) as manager_ID
from employees e 
join dept_emp de on e.emp_no = de.emp_no
where e.emp_no > 10020
group by e.emp_no
order by e.emp_no
limit 20) as B
union select C.*
from (select e.emp_no as employee_ID, min(de.dept_no) as department_code, 
(select emp_no
from dept_manager
where emp_no = 110022) as manager_ID
from employees e
join dept_emp de on e.emp_no = de.emp_no
where e.emp_no = 110039
group by e.emp_no
order by e.emp_no) as C
union select D.*
from (select e.emp_no as employee_ID, min(de.dept_no) as department_code, 
(select emp_no
from dept_manager
where emp_no = 110039) as manager_ID
from employees e
join dept_emp de on e.emp_no = de.emp_no
where e.emp_no = 110022
group by e.emp_no
order by e.emp_no) as D) as U
order by employee_ID; -- note that the output has two rows for the managers with employee_ID 110022 and 110039

-- self join: a table must join itself. Use when a column in a table is referenced in the same table
select * from emp_manager
order by emp_manager.emp_no;
select e1.*
from emp_manager e1
join emp_manager e2 on e1.emp_no = e2.manager_no;

-- SQL views: basically a view into the base table.
select *
from dept_emp; -- issue: multiple start dates for employees who switch roles, become managers, etc.
select emp_no, count(emp_no) as num
from dept_emp 
group by emp_no
having num > 1; -- shows list of such employees with multiple start dates

create or replace view v_dept_emp_latest_date as 
select emp_no, max(from_date) as from_date, max(to_date) as to_date
from dept_emp 
group by emp_no;
-- now we can see that view by calling it like this:
select * from employees.v_dept_emp_latest_date;
-- exercise: create view to extract avg salary of all managers. Round to nearest cent.
select round(avg(salary),2) as average_salary
from salaries s 
inner join dept_manager d on d.emp_no = s.emp_no;
