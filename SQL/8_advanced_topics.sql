/* Types of MySQL Variables
local variable: variable that rests between BEGIN and END. SQL doesn't recognize it outside of the function or stored procedure
session variables: variable that exists only for the session in which you're operating
	--defined on the server and lives there
    --visible to the connection being used only
	--ex: 100 users, 100 connections, 100 sessions. Session variable you create will only exist in your session.
*/
-- session variable
set @s_var1 = 3;
select @s_var1; -- if you open a new tab (but same session), it'll still work 
/* global variables: variables that apply across the entire server
examples: .max_connections() --max concurrent connections that can be established on the server)
 and .max_join_size --max memory space alloted for joins created by certain connection
 */
 set global max_connections = 1000;
 set @@global.max_connections = 1; -- this would set this current connection as the only allowed connection
 -- user-defined vs system variables
 
 -- triggers: see other file for in-depth walk-through
 -- exercise: create trigger that checks if hire date is in the future. If so, set as today's date
 delimiter $$
 create trigger trig_check_date
 before insert on employees
 for each row
 begin
	if new.hire_date > date_format(sysdate(),'%y-%m-%d') then
		set new.hire_date = date_format(sysdate(),'%y-%m-%d');
    end if;
end$$

delimiter ;

commit;
insert employees values ('999904','1970-01-31','John','Johnson','M','2025-01-01');
select * from employees
order by emp_no desc limit 10;
rollback;

-- index: how would you find a book in the Library of Alexandria? If books are alphabetized and grouped by subject, it's much easier! Such is indexing
-- no index example:
select * from employees 
where hire_date > '2000-01-01'; -- took my computer 0.141 seconds
-- index time
create index i_hire_date on employees(hire_date);
select * from employees 
where hire_date > '2000-01-01'; -- took my computer 0.000 seconds.. crazy
-- composite indexes: applied to MULTIPLE columns
-- first, it will look up rows based on data in first column (just like regular index)
-- second, based on that output, it will search by the second column
select * from employees
where first_name = 'Georgi' and last_name = 'Facello'; -- took 0.125 sec
create index i_composite on employees(first_name, last_name);
select * from employees
where first_name = 'Georgi' and last_name = 'Facello'; -- took 0.000 sec

show index from employees from employees;
-- problem of index: it takes up storage space. Try to balance speed with storage!!
alter table employees
drop index i_hire_date;

-- case statement
select emp_no, first_name, last_name,
case
	when gender = 'M' then 'male'
    else 'female'
end as gender
from employees;
-- could use an if statement, but in SQL an if statement is binary, while case allows for multiple options
-- all you have to do is add multiple "when" lines for each potential option

-- exercise: look for employee numbers higher than 109990 and identify if they are managers or not
select e.emp_no, e.first_name, e.last_name, 
case
	when d.emp_no is not null then "manager"
    else "not a manager"
end as manager
from employees e
left join dept_manager d on e.emp_no = d.emp_no -- left join is key to seeing where non-managers are. An inner join would only return managers
where e.emp_no > 109990
order by e.emp_no asc;