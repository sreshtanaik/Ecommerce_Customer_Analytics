CREATE DATABASE ecommerce_customer_analytics;

USE ecommerce_customer_analytics;

CREATE TABLE online_retail (
    invoice VARCHAR(20),
    stock_code VARCHAR(50),
    description TEXT,
    quantity INT,
    invoice_date DATETIME,
    price DECIMAL(12,4),
    customer_id INT,
    country VARCHAR(100),
    revenue DECIMAL(15,4)
);

LOAD DATA LOCAL INFILE 'C:/Projects/Mysql_data/online_retail_cleaned.csv'
INTO TABLE online_retail
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

TRUNCATE TABLE online_retail;

ALTER TABLE online_retail
MODIFY price DOUBLE,
MODIFY revenue DOUBLE;

SELECT COUNT(*) AS total_rows
FROM online_retail;

SELECT
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(
        SUM(revenue) / COUNT(DISTINCT invoice),
        2
    ) AS average_order_value,
    ROUND(
        SUM(revenue) / COUNT(DISTINCT customer_id),
        2
    ) AS revenue_per_customer
FROM online_retail;

WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT invoice) AS order_count
    FROM online_retail
    GROUP BY customer_id
)

SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    SUM(CASE WHEN order_count = 1 THEN 1 ELSE 0 END) AS one_time_customers,
    ROUND(
        SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END)
        / COUNT(*) * 100,
        2
    ) AS repeat_customer_rate
FROM customer_orders;

SELECT
    country,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT invoice) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(
        SUM(revenue) / COUNT(DISTINCT invoice),
        2
    ) AS average_order_value
FROM online_retail
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 10;

SELECT
    description AS product,
    SUM(quantity) AS units_sold,
    COUNT(DISTINCT invoice) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM online_retail
GROUP BY description
ORDER BY total_revenue DESC
LIMIT 10;

SELECT
    YEAR(invoice_date) AS year,
    MONTH(invoice_date) AS month_number,
    MONTHNAME(invoice_date) AS month,
    ROUND(SUM(revenue), 2) AS total_revenue,
    COUNT(DISTINCT invoice) AS total_orders,
    COUNT(DISTINCT customer_id) AS active_customers
FROM online_retail
GROUP BY
    YEAR(invoice_date),
    MONTH(invoice_date),
    MONTHNAME(invoice_date)
ORDER BY year, month_number;

SELECT
    customer_id,
    COUNT(DISTINCT invoice) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue) / COUNT(DISTINCT invoice), 2) AS average_order_value,
    MAX(invoice_date) AS last_purchase_date
FROM online_retail
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10;