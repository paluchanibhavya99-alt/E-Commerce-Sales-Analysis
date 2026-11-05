
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Find the main project folder
project_path = Path(__file__).resolve().parent.parent

# Load datasets
orders = pd.read_csv(
    project_path / "data" / "processed" / "orders.csv"
)

sales = pd.read_csv(
    project_path / "data" / "processed" / "sales_details.csv"
)

# Convert purchase date into datetime format
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)

# Remove rows with missing purchase dates
orders = orders.dropna(subset=["order_purchase_timestamp"])

# Merge orders and sales using order_id
merged_data = pd.merge(
    orders[["order_id", "order_purchase_timestamp"]],
    sales[["order_id", "price"]],
    on="order_id",
    how="inner"
)

# Group sales by month
merged_data["month"] = (
    merged_data["order_purchase_timestamp"].dt.to_period("M")
)

monthly_sales = merged_data.groupby("month")["price"].sum()

# Create chart
plt.figure(figsize=(12, 6))
plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker="o"
)

plt.title("Monthly E-Commerce Sales Trend")
plt.xlabel("Month")
plt.ylabel("Product Sales (R$)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Save chart
output_path = project_path / "reports" / "monthly_sales_trend.png"
plt.savefig(output_path, dpi=300)

plt.show()

print("Monthly sales chart created successfully!")
print("Saved at:", output_path)
