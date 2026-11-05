
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Get project folder
project_path = Path(__file__).resolve().parent.parent

# Read orders data
orders = pd.read_csv(
    project_path / "data" / "processed" / "orders.csv"
)

# Convert date columns
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"], errors="coerce"
)
orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"], errors="coerce"
)
orders["order_estimated_delivery_date"] = pd.to_datetime(
    orders["order_estimated_delivery_date"], errors="coerce"
)

# Keep orders with valid delivery dates
delivered = orders.dropna(
    subset=[
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
).copy()

# Calculate delivery time in days
delivered["actual_delivery_days"] = (
    delivered["order_delivered_customer_date"]
    - delivered["order_purchase_timestamp"]
).dt.total_seconds() / 86400

delivered["estimated_delivery_days"] = (
    delivered["order_estimated_delivery_date"]
    - delivered["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Calculate average delivery time
average_days = [
    delivered["actual_delivery_days"].mean(),
    delivered["estimated_delivery_days"].mean()
]

# Create chart
plt.figure(figsize=(9, 6))
plt.bar(
    ["Actual Delivery", "Estimated Delivery"],
    average_days,
    edgecolor="black"
)

plt.title("Actual vs Estimated Delivery Time")
plt.xlabel("Delivery Type")
plt.ylabel("Average Delivery Time (Days)")
plt.tight_layout()

# Save chart
output_path = project_path / "reports" / "delivery_performance.png"
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=300)
plt.show()

print("Delivery performance chart created successfully!")
print("Average actual delivery:", round(average_days[0], 2), "days")
print("Average estimated delivery:", round(average_days[1], 2), "days")
print("Saved at:", output_path)
