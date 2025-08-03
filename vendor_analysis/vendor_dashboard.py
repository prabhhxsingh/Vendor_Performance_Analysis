import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setup
sns.set(style='whitegrid')
plt.rcParams['font.size'] = 11

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="prabh",
    database="vendor_performance"
)

# --- QUERIES ---
# 1. Top Vendors by Total Sales
query1 = """
SELECT v.vendor_name, SUM(s.quantity * s.sale_price) AS total_sales
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN vendors v ON p.vendor_id = v.vendor_id
GROUP BY v.vendor_id
ORDER BY total_sales DESC
LIMIT 5;
"""
df1 = pd.read_sql(query1, connection)

# 2. Monthly Sales
query2 = """
SELECT DATE_FORMAT(sale_date, '%Y-%m') AS month, SUM(quantity * sale_price) AS monthly_sales
FROM sales
GROUP BY month
ORDER BY month;
"""
df2 = pd.read_sql(query2, connection)

# 3. Product Category Pie
query3 = "SELECT category, COUNT(*) as count FROM products GROUP BY category;"
df3 = pd.read_sql(query3, connection)

# 4. Vendor Ratings
query4 = "SELECT vendor_name, rating FROM vendors ORDER BY rating DESC;"
df4 = pd.read_sql(query4, connection)

# 5. Top Products by Revenue
query5 = """
SELECT p.product_name, SUM(s.quantity * s.sale_price) AS total_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_revenue DESC
LIMIT 5;
"""
df5 = pd.read_sql(query5, connection)

# --- PLOTTING ---
fig, axs = plt.subplots(2, 3, figsize=(22, 11))
fig.suptitle('📊 Vendor Performance Dashboard', fontsize=20, fontweight='bold', color='darkblue')

# Plot 1: Bar Chart - Top Vendors by Sales
sns.barplot(x='total_sales', y='vendor_name', data=df1, palette='rocket', ax=axs[0, 0])
axs[0, 0].set_title('Top 5 Vendors by Sales 💰', fontsize=13, fontweight='bold')
axs[0, 0].set_xlabel('Total Sales')
axs[0, 0].set_ylabel('Vendor')

# Plot 2: Line Plot - Monthly Sales
sns.lineplot(x='month', y='monthly_sales', data=df2, marker='o', color='darkorange', linewidth=3, markersize=8, ax=axs[0, 1])
axs[0, 1].set_title('Monthly Sales Trend 📈', fontsize=13, fontweight='bold')
axs[0, 1].tick_params(axis='x', rotation=45)
axs[0, 1].set_xlabel('Month')
axs[0, 1].set_ylabel('Sales')

# Plot 3: Pie Chart - Product Categories
if not df3.empty:
    axs[0, 2].pie(df3['count'], labels=df3['category'], autopct='%1.1f%%',
                  startangle=140, colors=sns.color_palette('pastel'))
    axs[0, 2].set_title('Product Categories 📦', fontsize=13, fontweight='bold')
else:
    axs[0, 2].text(0.5, 0.5, 'No Data Available', ha='center', fontsize=12)

# Plot 4: Scatter Plot - Vendor Ratings
if not df4.empty:
    axs[1, 0].scatter(df4['rating'], df4['vendor_name'], color='mediumvioletred', s=100, alpha=0.7)
    axs[1, 0].set_title('Vendor Ratings ⭐ (Scatter)', fontsize=13, fontweight='bold')
    axs[1, 0].set_xlabel('Rating')
    axs[1, 0].set_ylabel('Vendor')
    axs[1, 0].grid(True)
else:
    axs[1, 0].text(0.5, 0.5, 'No Data Available', ha='center', fontsize=12)

# Plot 5: Horizontal Bar Chart - Top Products by Revenue
sns.barplot(x='total_revenue', y='product_name', data=df5, palette='flare', ax=axs[1, 1])
axs[1, 1].set_title('Top Products by Revenue 💰', fontsize=13, fontweight='bold')
axs[1, 1].set_xlabel('Revenue')
axs[1, 1].set_ylabel('Product')

# Plot 6: Heatmap-style Strip Plot - Vendor Rating Heatmap
if not df4.empty:
    df4_sorted = df4.sort_values(by='rating', ascending=True)
    sns.stripplot(x='rating', y='vendor_name', data=df4_sorted, palette='bright', size=10, ax=axs[1, 2])
    axs[1, 2].set_title('Vendor Rating Heatmap 🎯', fontsize=13, fontweight='bold')
    axs[1, 2].set_xlabel('Rating')
    axs[1, 2].set_ylabel('Vendor')
else:
    axs[1, 2].text(0.5, 0.5, 'No Ratings Found', ha='center', fontsize=12)

# Adjust Layout
plt.subplots_adjust(left=0.05, right=0.97, top=0.9, bottom=0.08, wspace=0.3, hspace=0.4)
# ---- Your data visualization code here ---- #

# Export data for Power BI
df1.to_csv("top_vendors.csv", index=False)
df2.to_csv("monthly_sales.csv", index=False)
df3.to_csv("product_categories.csv", index=False)
df4.to_csv("vendor_ratings.csv", index=False)
df5.to_csv("top_products.csv", index=False)
# Save the figure
fig.savefig('vendor_performance_dashboard.png')
plt.show()
# Close DB
connection.close()
