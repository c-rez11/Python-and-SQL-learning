use employees_mod;
-- JOINS

-- prep for joins by altering a few tables
-- alter table departments_duplicate
-- drop column dept_manager;
-- select * from departments_duplicate;
-- alter table departments_duplicate
-- change column dept_no dept_no char(4) NULL;
-- alter table departments_duplicate
-- change column dept_name dept_name varchar(40) NULL;


-- create dept_manager_dup table
DROP TABLE IF EXISTS dept_manager_dup;

CREATE TABLE dept_manager_dup (

  emp_no int(11) NOT NULL,

  dept_no char(4) NULL,

  from_date date NOT NULL,

  to_date date NULL

  );

 

INSERT INTO dept_manager_dup

select * from dept_manager;

 

INSERT INTO dept_manager_dup (emp_no, from_date)

VALUES                (999904, '2017-01-01'),

                                (999905, '2017-01-01'),

                               (999906, '2017-01-01'),

                               (999907, '2017-01-01');

 

DELETE FROM dept_manager_dup

WHERE

    dept_no = 'd001';

INSERT INTO departments_duplicate (dept_name)

VALUES                ('Public Relations');

 

DELETE FROM departments_duplicate

WHERE

    dept_no = 'd002'; 
    

select * from departments_duplicate;
select * from dept_manager_dup order by dept_no;
-- INNER JOIN
-- only overlapping rows of the joined tables will show in result
select * from departments_duplicate; -- no values for d002, a few null values in both columns, etc
select * from dept_manager_dup order by dept_no; -- employees with high emp_no have null data

select m.dept_no, m.emp_no, d.dept_name
from dept_manager_dup m -- using aliases "m" and "d" for manager and departments tables respectively
inner join
departments_duplicate d on m.dept_no = d.dept_no
order by m.dept_no;
/* Note that there's no data on d001, d002 or null values for dept_no. Inner join also didn't match null values*/
-- return a list of info all managers' employee number, first/last name, department number, and hire date
select m.emp_no,e.first_name,e.last_name,m.dept_no,e.hire_date
from employees e
inner join dept_manager_dup m on m.emp_no = e.emp_no order by e.emp_no;

-- duplicates
insert into dept_manager_dup
values ('110228','d003','1992-03-21','9999-01-01');
insert into departments_duplicate
values ('d009','Customer Service'); -- these are the added duplicate rows
select * from dept_manager_dup order by dept_no asc;
select * from departments_duplicate order by dept_no asc;

-- doing the inner join from earlier in this code, here's how we filter duplicates:
select m.emp_no, m.dept_no, d.dept_name
from dept_manager_dup m -- using aliases "m" and "d" for manager and departments tables respectively
inner join
departments_duplicate d on m.dept_no = d.dept_no
group by m.emp_no, m.dept_no, d.dept_name
order by m.dept_no; -- not working for some reason
-- remove duplicates
delete from dept_manager_dup
where emp_no = '110228';
delete from departments_duplicate
where dept_no = 'd009';
-- add back initial records
insert into dept_manager_dup
values ('110228','d003','1992-03-21','9999-01-01');
insert into departments_duplicate
values ('d009','Customer Service');

-- left join: keep everything in left table, only overlapping values of right table (think 2/3 of a venn diagram)
select m.emp_no, m.dept_no, d.dept_name
from dept_manager_dup m -- using aliases "m" and "d" for manager and departments tables respectively
left join
departments_duplicate d on m.dept_no = d.dept_no
order by m.dept_no; -- the dept_name null values are values that could not be matched in the deptartment_duplicates table
-- what happens when we switch the table order?
select m.emp_no, d.dept_no, d.dept_name
from departments_duplicate d -- using aliases "m" and "d" for manager and departments tables respectively
left join
dept_manager_dup m on m.dept_no = d.dept_no
order by m.dept_no; -- the null values in emp_no represent that nothing was matched from the dept_manager_dup table
-- find null values where left side couldn't find a right-side match
select m.emp_no, m.dept_no, d.dept_name
from dept_manager_dup m -- using aliases "m" and "d" for manager and departments tables respectively
left join
departments_duplicate d on m.dept_no = d.dept_no
where dept_name is null -- this 'where' clause is the key
order by m.dept_no;

/* Exercise: Join the 'employees' and the 'dept_manager' tables to return a subset of all the employees whose last name is Markovitch. 
See if the output contains a manager with that name.*/
select * from dept_manager order by dept_no asc;
select * from employees;
select e.emp_no, e.first_name, e.last_name, m.dept_no
from employees e
left join
dept_manager m on e.emp_no = m.emp_no
where last_name = "Markovitch" -- alternative: add "and dept_no is not null" to get just the managers with Markovitch as last name
order by m.dept_no desc, emp_no;

/* Note about using 'where' rather than 'join': 'join' is much faster compute
-- exercise: use slower method 'where' */
select e.emp_no, e.first_name, e.last_name, e.hire_date, m.dept_no
from dept_manager m, employees e
where e.emp_no = m.emp_no
order by m.dept_no;

-- pause: prevent error code 1055 by running following code:
set @@global.sql_mode := replace(@@global.sql_mode, 'only_full_group_by','');

-- exercise: select first/last name, hire date, and job title of all employees named Margareta Markovitch
-- not sure where job title comes from, so commenting out
-- select e.first_name, e.last_name, t.from_date, t.title
-- from employees e
-- join
-- titles t on e.emp_no = t.emp_no
-- where e.first_name = 'Margareta' and e.last_name = 'Markovitch'
-- order by e.emp_no desc;

-- cross join: connects ALL values, not just those that match. Think a completely filled-in venn diagram
select dm.*, d.*
from dept_manager dm
cross join
departments d
order by dm.emp_no, d.dept_no;
-- exercise: return a list with all possible combos between managers and dept #9
select dm.*,d.*
from dept_manager dm
cross join departments d
where d.dept_no = 'd009'
order by dm.emp_no,d.dept_no;
-- join with aggregate functions: find avg salary by gender
select e.gender, avg(s.salary) as average_salary
from employees e
inner join
salaries s on e.emp_no = s.emp_no
group by gender;
-- join 3+ tables
select e.first_name, e.last_name, e.hire_date, m.from_date, d.dept_name
from employees e
inner join
dept_manager m on e.emp_no = m.emp_no
join
departments d on m.dept_no = d.dept_no;
-- managers' first/last name, hire date, job title, start date, and dept name
select e.first_name, e.last_name, e.hire_date, e.hire_date, m.from_date, d.dept_name
from employees e
inner join
dept_manager m on e.emp_no = m.emp_no
inner join
departments d on m.dept_no = d.dept_no;
-- join tips and tricks
/* You don't have to use primary/foreign keys to join. When looking at a picture of all your connected SQL tables, you can "skip" connections and jump straight to similar columns*/
select d.dept_name, avg(salary)
from departments d
join dept_manager m on d.dept_no = m.dept_no
join salaries s on m.emp_no = s.emp_no
group by d.dept_name;
-- exercise: how many male/female managers do we have in employees database?
select e.gender, count(e.emp_no) as number_of_managers
from employees e
inner join dept_manager d on d.emp_no = e.emp_no
group by e.gender;

-- union

drop table if exists employees_dup; -- prep for example
create table employees_dup (
emp_no int(11),
birth_date date,
first_name varchar(14),
last_name varchar(16),
gender enum('M','F'),
hire_date date);

insert into employees_dup -- duplicate structure of the employees table
select e.* from employees e 
limit 20;

select * from employees_dup;
-- union all: used to cobine a few select statements in a single output. However, the tables must have the same columns and data structure

select e.emp_no, e.first_name, e.last_name, null as dept_no, null as from_date -- nulls must be added to have the same data structure across the two tables
from employees_dup e 
where e.emp_no = 10001
union all select
null as emp_no, null as first_name, null as last_name, m.dept_no, m.from_date -- same thing with nulls here
from dept_manager m;
-- union vs union all: union displays only distinct values. Union all is better for speed/performance

select * from employees;