
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Get project folder
project_path = Path(__file__).resolve().parent.parent

# Read payments data
payments = pd.read_csv(
    project_path / "data" / "processed" / "payments.csv"
)

# Calculate total value for each payment method
payment_data = payments.groupby("payment_type")["payment_value"].sum()

# Create chart
plt.figure(figsize=(9, 6))
payment_data.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Payment Method Distribution")
plt.ylabel("")
plt.tight_layout()

# Save chart
output_path = project_path / "reports" / "payment_method_distribution.png"
plt.savefig(output_path, dpi=300)
plt.show()

print("Payment method chart created successfully!")
print("Saved at:", output_path)
