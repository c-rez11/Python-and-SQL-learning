/* Window Functions: performs a calculation for every record in the data set ("current row") 
using other records ("window") associated with the specified one from the table
window = the window over which the given function evaluation will be performed. Acts as set of rows on which the given function will be applied.
aggregate vs non-aggregate window functions (non-aggregate: ranking vs value) */
use employees;

select 
	emp_no,
	salary,
    row_number() over (partition by emp_no order by salary desc) as row_num -- row_number() is a known window function within SQL
    -- if you leave over () as open, it will apply to all rows
    -- partition is basically a "group by" clause
    -- "order by" ranks the return values by salary from highest to lowest
 from salaries; 

-- exercise: assign a row # to all managers, starting from lowest emp_no

select
emp_no,
dept_no,
row_number() over (order by emp_no) as row_num
from dept_manager;

-- exercise: select manager salaries, then add a column ranking the salaries

SELECT
dm.emp_no,
salary,
ROW_NUMBER() OVER (PARTITION BY emp_no ORDER BY salary ASC) AS row_num1,
ROW_NUMBER() OVER (PARTITION BY emp_no ORDER BY salary DESC) AS row_num2   
FROM dept_manager dm
JOIN salaries s ON dm.emp_no = s.emp_no;

-- using the "window" command to do the same thing as the first example in this script
select 
	emp_no,
	salary,
    row_number() over w as row_num
 from salaries
 window w as (partition by emp_no order by salary desc); -- most professionals don't use this method of naming windows unless there are a lot of window functions and repeat usage 
 
 /* group by vs partition by 
 while group by might be more effective for max() and min() functions, partition by allows us to find values that aren't the highest or lowest rank...maybe we want the 2nd-highest salary for each employee.

*/
select a.emp_no, a.salary as max_salary from (
select emp_no, salary, row_number() over w as row_num
from salaries
window w as (partition by emp_no order by salary desc)) a 
where a.row_num = 2; -- easy to return second-highest salary

/* rank() vs dense_rank()
- what if an employee has signed for the same salary, but at different times? How does rank work?

*/
select emp_no, (count(salary) - count(distinct salary)) as diff
from salaries
group by emp_no
having diff > 0
order by emp_no; -- this tells us which scenarios we might have a tied rank if ranking on salary
-- one of these emp_no, 11839, will be used in further queries

select emp_no, salary, rank() over w as rank_num
from salaries
where emp_no = 11839
window w as (partition by emp_no order by salary desc); -- this is rank() in action, where we assign identical ranks to identical values (see rank #3 in the output)
-- in the previous example, there are two ranks of 3 and no rank of 4 (it skips to 5, as it's the 5th-highest salary)
-- if you want the rank to go to 4 instead of 5, use dense_rank() to do so

-- example
select
d.dept_no, 
d.dept_name, 
dm.emp_no,
rank() over w as department_salary_ranking,
s.salary, 
s.from_date as salary_from_date,
s.to_date as salary_to_date,
dm.from_date as dept_manager_from_date,
dm.to_date as dept_manager_to_date
from dept_manager dm
join salaries s on s.emp_no = dm.emp_no
and s.from_date between dm.from_date and dm.to_date
and s.to_date between dm.from_date and dm.to_date -- this ensures that we don't report salaries from the times an employee had a role other than manager while employed at the company
join departments d on d.dept_no = dm.dept_no
window w as (partition by dm.dept_no order by s.salary desc);

-- VALUE window functions: return a value that are based on a value in the database

select * from salaries limit 10;

select
emp_no,
salary,
lag(salary) over w as previous_salary,
lead(salary) over w as next_salary,
salary - lag(salary) over w as diff_salary_previous,
lead(salary) over w - salary as diff_salary_next
from salaries
where emp_no = 10001
window w as (order by salary);

-- example: return lag(2) and lead(2)

select
emp_no,
salary,
lag(salary) over w as previous_salary,
lead(salary) over w as next_salary,
lag(salary,2) over w as previous2_salary,
lead(salary,2) over w as next2_salary
from salaries
-- where to_date > sysdate()
window w as (partition by emp_no order by salary)
limit 1000;

-- AGGREGATE window functions
select s1.emp_no, s.salary, s.from_date, s.to_date
from salaries s
join (select emp_no, max(from_date) as from_date
	from salaries
    group by emp_no) s1 on s.emp_no = s1.emp_no
    where s.to_date > sysdate()
    and s.from_date = s1.from_date;
    
    -- example

select
de2.emp_no, d.dept_name, s2.salary, avg(s2.salary) over w as average_salary_per_department
from 
(select de.emp_no, de.dept_no, de.from_date, de.to_date
from dept_emp de
join
(select emp_no, max(from_date) as from_date
from dept_emp group by emp_no) de1 on de1.emp_no = de.emp_no
where de.to_date > sysdate()
and de.from_date = de1.from_date) de2
join
(select s1.emp_no, s.salary, s.from_date, s.to_date
from salaries s
join (select emp_no, max(from_date) as from_date
	from salaries
    group by emp_no) s1 on s.emp_no = s1.emp_no
    where s.to_date > sysdate()
    and s.from_date = s1.from_date) s2 on s2.emp_no = de2.emp_no
    join departments d on d.dept_no = de2.dept_no
    group by de2.emp_no, d.dept_name
    window w as (partition by de2.dept_no)
    order by de2.emp_no;
