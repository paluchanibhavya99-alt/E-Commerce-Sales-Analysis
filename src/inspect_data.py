
import csv
from pathlib import Path

# Locate the raw dataset folder
DATA_FOLDER = Path(__file__).resolve().parent.parent / "data" / "raw"

# List all CSV files
csv_files = list(DATA_FOLDER.glob("*.csv"))

print("=" * 65)
print("       E-COMMERCE DATASET EXPLORATION")
print("=" * 65)

print(f"\nTotal CSV files found: {len(csv_files)}")

# Inspect each CSV file
for file_path in sorted(csv_files):

    print("\n" + "-" * 65)
    print(f"FILE NAME: {file_path.name}")
    print("-" * 65)

    with open(file_path, "r", encoding="utf-8-sig",
              newline="") as file:

        reader = csv.DictReader(file)

        # Display column names
        columns = reader.fieldnames
        print("\nCOLUMNS:")
        print(columns)

        # Display first two records
        sample_records = []

        for _ in range(2):
            row = next(reader, None)
            if row is not None:
                sample_records.append(row)

        print("\nSAMPLE RECORDS:")

        for record in sample_records:
            print(record)

        # Count total records
        remaining_records = sum(1 for _ in reader)
        total_records = len(sample_records) + remaining_records

        print(f"\nTOTAL RECORDS: {total_records}")

print("\n" + "=" * 65)
print("DATASET EXPLORATION COMPLETED")
print("=" * 65)
