import pandas as pd

# Load both CSV files
df1 = pd.read_csv("extracted_emails.csv")
df2 = pd.read_csv("EmailDB.csv")

# Filter rows in df1 where EmailAddress is NOT in df2
result = df1[~df1["EmailAddress"].isin(df2["EmailAddress"])]

# Save to new CSV
result.to_csv("new.csv", index=False)
