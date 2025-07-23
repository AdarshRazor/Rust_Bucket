import pandas as pd

# Load CSV file
input_file = 'emails/raw_contacts.csv'  # Change this to your actual CSV file name
df = pd.read_csv(input_file)

# Check if 'EmailAddress' column exists
if 'EmailAddress' not in df.columns:
    raise ValueError("Column 'EmailAddress' not found in the CSV.")

# Drop rows where 'EmailAddress' is empty or null
# (after loading and before dropping duplicates)
df = df[df['EmailAddress'].notna() & (df['EmailAddress'].astype(str).str.strip() != '')]

# Drop duplicates (exact email match)
df_unique = df.drop_duplicates(subset=['EmailAddress'])  # type: ignore

# Optional: Reset index
df_unique = df_unique.reset_index(drop=True)

# Save cleaned email list
output_file = 'emails/cleaned_emails.csv'
df_unique.to_csv(output_file, index=False)

print(f"✅ Cleaned emails saved to '{output_file}'. Total unique emails: {len(df_unique)}")
