-- Step 1: Use a CTE to isolate and rank customer purchases to get the latest transaction (Deduplication)
WITH RankedSales AS (
    SELECT 
        customer_id,
        order_id,
        order_date,
        total_amount,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) as rn
    FROM fact_sales
),

-- Step 2: Extract only the most recent transaction for each customer
LatestCustomerPurchases AS (
    SELECT 
        customer_id,
        order_id,
        order_date,
        total_amount
    FROM RankedSales
    WHERE rn = 1
),

-- Step 3: Calculate Monthly Revenue and MoM (Month-over-Month) Growth using Window Functions
MonthlyRevenue AS (
    SELECT 
        DATE_TRUNC('month', order_date) as sales_month,
        SUM(total_amount) as monthly_total
    FROM fact_sales
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT 
    sales_month,
    monthly_total,
    LAG(monthly_total, 1) OVER (ORDER BY sales_month) as previous_month_total,
    ROUND(
        ((monthly_total - LAG(monthly_total, 1) OVER (ORDER BY sales_month)) / 
        NULLIF(LAG(monthly_total, 1) OVER (ORDER BY sales_month), 0)) * 100, 2
    ) as mom_growth_percentage
FROM MonthlyRevenue
ORDER BY sales_month DESC;