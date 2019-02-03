# Mini-sql-Engine
Following Queries are handled by the Sql_engine

1. Select all records :
Select * from table_name;

2. Aggregate functions: Simple aggregate functions on a single column.Sum, average, max and min. They will be very trivial given that the data is only
numbers:
Select max(col1) from table1;


3. Project Columns(could be any number of columns) from one or more tables :
Select col1, col2 from table_name;

4. Select/project with distinct from one table: (distinct of a pair of values indicates the
pair should be distinct)
Select distinct col1, col2 from table_name;

5. Select with where from one or more tables :
Select col1,col2 from table1,table2 where col1 = 10 AND col2 = 20;

a. In the where queries, there would be a maximum of one AND/OR operator
with no NOT operators.

b. Relational operators that are to be handled in the assignment, the operators
include "< , >, <=, >=, =".

6. Projection of one or more(including all the columns) from two tables with one join
condition :
a. Select * from table1, table2 where table1.col1=table2.col2;
b. Select col1, col2 from table1,table2 where table1.col1=table2.col2;
c. NO REPETITION OF COLUMNS – THE JOINING COLUMN SHOULD BE
PRINTED ONLY ONCE.
