import csv
import sys

input_file = r"C:\Users\LOQ\OneDrive\Desktop\mini project\ekajalakkam-main\ekajalakkam-main\data\complaints_expanded.csv"
output_file = r"C:\Users\LOQ\OneDrive\Desktop\mini project\ekajalakkam-main\ekajalakkam-main\data\final_50k_complaints.csv"

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Written {len(rows)} rows to {output_file}")
print("First 3 rows:")
for row in rows[:3]:
    print(','.join(row))
print("...")
print("Last 3 rows:")
for row in rows[-3:]:
    print(','.join(row))