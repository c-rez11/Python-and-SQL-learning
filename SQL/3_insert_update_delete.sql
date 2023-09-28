use employees_mod;
select * from employees limit 10;

insert into employees
(
	emp_no,
    birth_date,
    first_name,
    last_name,
    gender,
    hire_date
    )
values
(
	999901,
    '2022-12-31',
    'Carlitos',
    'Peress',
    'M',
    '2021-10-01'
    );

select * from employees order by emp_no desc limit 10;

-- insert data into a new table
-- let's duplicate the departments table
create table departments_duplicate (
	dept_no char(4) not null,
    dept_name varchar(40));

insert into departments_duplicate (
	dept_no,
    dept_name)
select * from departments;

select * from departments_duplicate;

-- update
-- would need to turn off safe updating that exists in MySQL
update employees
set first_name = 'Stella', last_name = 'Parkinson', birth_date = '1990-12-31', gender = 'F' where emp_no = 999901;

-- delete
delete from employees where emp_no = 999903; -- note: for both update and delete, it's important to use the 'where' clause to avoid affecting all the data
-- note that if we created the table with 'on delete cascade', it will wipe all data about a given row if that row is deleted

-- drop vs truncate vs delete
-- drop: removes something, all it's indexes, data structures, etc
-- truncate: functions like delete without a where clause. All data is dropped, but data structure remains
-- delete: removes data line-by-line

