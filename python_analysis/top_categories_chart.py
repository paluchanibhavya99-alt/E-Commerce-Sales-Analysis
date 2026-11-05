
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Get project folder
project_path = Path(__file__).resolve().parent.parent

# Load sales dataset
sales = pd.read_csv(
    project_path / "data" / "processed" / "sales_details.csv"
)

# Calculate revenue by product category
category_sales = (
    sales.groupby("product_category_name_english")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Create chart
plt.figure(figsize=(12, 7))

category_sales.sort_values().plot(
    kind="barh",
    edgecolor="black"
)

plt.title("Top 10 Product Categories by Sales")
plt.xlabel("Total Sales (R$)")
plt.ylabel("Product Category")
plt.tight_layout()

# Save chart
output_path = project_path / "reports" / "top_10_categories.png"
plt.savefig(output_path, dpi=300)

plt.show()

print("Top 10 categories chart created successfully!")
print("Saved at:", output_path)
