You are an expert data cleaning assistant.

I will give you a raw list that includes emails, timestamps, images, and junk data. From this, I want you to extract only **valid unique email addresses**, remove any entries ending with `@gmail.com`, and ignore any that are not actual emails (like `.png`, `.jpg`, or malformed addresses).

Once cleaned, I want the output in CSV format with the following headers:

**EmailAddress,FirstName,Comments**

Here’s how to determine the `FirstName`:
- If the email is **generic** (starts with `info@`, `hr@`, `sales@`, `jobs@`, `contact@`, etc.), then use `"Team"` as the first name.
- Otherwise, extract the first name intelligently from the email (e.g., from `john.doe@company.com`, use `John`, or from `aakash.sharma@company.com`, use `Aakash`) - The names would be mostly from India.

Leave the `Comments` field empty.

Please return the output directly in CSV format with headers.

Now here's the raw content:
