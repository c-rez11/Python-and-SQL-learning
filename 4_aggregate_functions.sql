-- Aggregate functions
-- count()
-- exercise: how many departments are there in the employees database?
Select count(distinct dept_no) from dept_emp;
-- sum()
-- exercise: total amount of money spent on salaries for contracts starting after 1/1/1997
select sum(salary) from salaries where from_date>'1997-01-01';
-- max()
-- highest salary in DB? lowest?
select max(salary) from salaries;
select min(salary) from salaries;
-- avg()
select avg(salary) from salaries; -- avg salary
-- round()
select round(avg(salary),-2) from salaries;

-- ifnull()
select dept_no, ifnull(dept_name, 'department name not provided') as dept_name from departments_duplicate order by dept_no;
-- coalesce(): essentially an ifnull() with 2+ parameters
alter table departments_duplicate -- add new column with null values (to practice)
add column dept_manager varchar(55) after dept_name;
select * from departments_duplicate;
insert into departments_duplicate (dept_no,dept_name,dept_manager) -- add null rows to set up coalesce scenario
values ('d010','','');
update departments_duplicate
	set dept_name = NULL, dept_manager = NULL where dept_no = 'd010';
    
select dept_no, dept_name, coalesce(dept_manager, dept_name,'N/A') as dept_manager from departments_duplicate order by dept_no; /* looks for not null values, finding none in the columns
of dept_name and dept_manager (moving from right to left), it returns 'N/A' in the far right column*/
