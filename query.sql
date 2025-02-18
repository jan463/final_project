USE final_project;

-- 1
-- find 3 dishes with most calories per serving
SELECT name, calories 
FROM sql_df
ORDER BY calories DESC
LIMIT 3;

-- 2
-- number of top rated recipes from japan
SELECT COUNT(DISTINCT(name))
FROM sql_df
WHERE nations LIKE "%japanese%"
ORDER BY aggregatedrating DESC;

-- 3
-- average calorie count from american desserts
SELECT AVG(calories) AS average_calories
FROM sql_df
WHERE recipecategory LIKE "%dessert%"
AND nations LIKE "%american%";

-- 4
-- find examples of greek soup
SELECT name
FROM sql_df
WHERE recipecategory LIKE "%soup%"
AND nations LIKE "%greek%";

-- 5
-- find examples of irish snacks
SELECT name
FROM sql_df
WHERE recipecategory LIKE "%snack%"
AND nations LIKE "%hawaiian%";


