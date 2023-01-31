/* Common Table Expression (CTE): tool for obtaining temporary result sets that 
exist within the execution of a given query. 
*/
-- example: how many salary contracts signed by female employees have been valued above..
-- the all-time avg contract salary value of the company?
-- two result sets needed
use employees;

select avg(salary) as avg_salary
from salaries; -- first result set needed. Now put it in one query

with cte as (
select avg(salary) as avg_salary from salaries) -- CTEs are sometimes called "named subqueries" for reasons like this
select
sum(case when s.salary > c.avg_salary then 1 else 0 end) as no_f_salaries_above_avg,
count(s.salary) as total_no_of_salary_contracts
from salaries s
join employees e on s.emp_no = e.emp_no and e.gender = 'F'
cross join cte c;

-- multiple CTEs
with cte1 as (select avg(salary) as avg_salary from salaries),
cte2 as (
select s.emp_no, max(s.salary) as f_highest_salary
from salaries s 
join employees e on e.emp_no = s.emp_no and e.gender = 'F'
group by s.emp_no)
select sum(case when c2.f_highest_salary > c1.avg_salary then 1 else 0 end) as f_highest_salaries_above_avg,
count(e.emp_no) as total_no_female_contracts
from employees e
join cte2 c2 on c2.emp_no = e.emp_no
cross join cte1 c1; -- returns the # of female workers whose highest contract ever was higher than the all-time company average

/* Temporary tables: best used when we need to refer to a specific result set multiple times in our analysis,
particularly when our default database is vast and we want to save time.*/

-- example: a list of highest contract salary values signed by all female employees

select
s.emp_no, max(s.salary) as f_highest_salary
from salaries s 
join employees e on e.emp_no = s.emp_no and e.gender = 'F'
group by s.emp_no;

-- instead of referencing this query every time (and to save computation power), we create a temporary table

create temporary table f_highest_salaries -- as simple as adding this line to the query
select
s.emp_no, max(s.salary) as f_highest_salary
from salaries s 
join employees e on e.emp_no = s.emp_no and e.gender = 'F'
group by s.emp_no;

-- practice referencing it
select *
from f_highest_salaries
where emp_no <= '10010';

drop temporary table if exists f_highest_salaries;

/*Note: temporary tables are locked for use, meaning they can't be used in joins or unions.
There is a workaround though: creating a CTE. */

with cte as (select
s.emp_no, max(s.salary) as f_highest_salary
from salaries s 
join employees e on e.emp_no = s.emp_no and e.gender = 'F'
group by s.emp_no limit 10)
select * from f_highest_salaries f1 join cte c;

-- but CTEs aren't perfect. Here's an example:
create temporary table dates
select 
	now() as current_date_and_time,
    date_sub(now(), interval 1 month) as a_month_earlier,
    date_sub(now(), interval -1 month) as a_year_later;

select *
from dates d1
union select *
from dates d2; -- error: can't reopen table 'd1'

with cte as (select 
	now() as current_date_and_time,
    date_sub(now(), interval 1 month) as a_month_earlier,
    date_sub(now(), interval -1 month) as a_year_later)
select * from dates d1 join cte c; -- now it works

drop table if exists f_highest_salaries;
drop temporary table if exists dates;




