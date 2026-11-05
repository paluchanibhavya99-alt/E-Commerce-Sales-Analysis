
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Get project folder
project_path = Path(__file__).resolve().parent.parent

# Read reviews data
reviews = pd.read_csv(
    project_path / "data" / "processed" / "reviews.csv"
)

# Count customer ratings
rating_counts = reviews["review_score"].value_counts().sort_index()

# Create bar chart
plt.figure(figsize=(9, 6))
rating_counts.plot(kind="bar", edgecolor="black")

plt.title("Customer Review Ratings")
plt.xlabel("Rating (Stars)")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=0)
plt.tight_layout()

# Save chart
output_path = project_path / "reports" / "customer_review_ratings.png"
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=300)
plt.show()

print("Customer review chart created successfully!")
print("Saved at:", output_path)
