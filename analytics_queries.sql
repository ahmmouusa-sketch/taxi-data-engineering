-- =========================================================================
-- Advanced Analytics Queries for Taxi Data Engineering Project
-- =========================================================================

-- 1. تتبع سلوك العميل وحساب الفارق بين الطلب الحالي والطلب السابق لكل عميل باستخدام LAG
SELECT 
    order_id,
    customer_name,
    total_price,
    LAG(total_price, 1, 0) OVER (
        PARTITION BY customer_name 
        ORDER BY order_id
    ) AS previous_order_price,
    -- حساب الفرق في السعر بين الطلب الحالي والطلب السابق
    total_price - LAG(total_price, 1, 0) OVER (
        PARTITION BY customer_name 
        ORDER BY order_id
    ) AS price_difference
FROM fact_sales_processed;


-- 2. حساب المتوسط المتحرك (Rolling Average) لقيمة المشتريات للعملاء لتتبع النمط الاستهلاكي
SELECT 
    order_id,
    customer_name,
    total_price,
    AVG(total_price) OVER (
        PARTITION BY customer_name 
        ORDER BY order_id 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS rolling_avg_3_orders
FROM fact_sales_processed;


-- 3. تصنيف وتجميع المبيعات حسب الـ Category مع حساب إجمالي الإيرادات وعدد الطلبات لكل فئة
SELECT 
    category,
    COUNT(order_id) AS total_orders,
    SUM(total_price) AS category_revenue,
    AVG(total_price) AS avg_order_value
FROM fact_sales_processed
GROUP BY category
ORDER BY category_revenue DESC;
