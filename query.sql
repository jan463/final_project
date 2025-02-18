USE final_project;

-- 1
-- find 5 dishes with most calories per serving
SELECT name, calories FROM sql_df
ORDER BY calories DESC
LIMIT 10;