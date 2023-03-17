import mysql.connector

cnx = mysql.connector.connect(user='scott', database='employees')

# Query to get employees who joined in a period defined by two dates
insert_query = (
  "INSERT INTO ebdb.FINRA_TRACE_BOND "
  "LEFT JOIN salaries AS s USING (emp_no) "
  "WHERE to_date = DATE('9999-01-01')"
  "AND e.hire_date BETWEEN DATE(%s) AND DATE(%s)")

insert_query = (
    "INSERT INTO ebdb.FINRA_TRACE_BOND "
    "(date,bondType,total_issues_traded,advances,declines,unchanged,high_52_weeks,low_52_weeks,dollar_volume) "
    "VALUES (<{date: }>,
<{bondType: }>,
<{total_issues_traded: }>,
<{advances: }>,
<{declines: }>,
<{unchanged: }>,
<{high_52_weeks: }>,
<{low_52_weeks: }>,
<{dollar_volume: }>);
)