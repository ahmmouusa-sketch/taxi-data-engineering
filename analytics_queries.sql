-- 1. Total revenue and top spending customers per city
SELECT 
    c.city,
    c.customer_name,
    COUNT(f.order_id) as total_orders,
    SUM(f.total_price) as total_spent
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY c.city, c.customer_name
ORDER BY total_spent DESC;

-- 2. Best-selling categories and products with total revenue
SELECT 
    p.category,
    p.product,
    SUM(f.quantity) as units_sold,
    SUM(f.total_price) as total_revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.category, p.product
ORDER BY total_revenue DESC;