import json

# Read the file
with open("result.txt", "r") as file:
    lines = file.readlines()

# Extract links and create JSON structure
jobs = []
for line in lines:
    line = line.strip()
    if line:
        # Split by first period and space, then take the URL
        parts = line.split(". ", 1)
        if len(parts) == 2:
            job_id = int(parts[0])
            url = parts[1]
            jobs.append({"id": job_id, "url": url})

# Write to JSON file
with open("jobs.json", "w") as json_file:
    json.dump(jobs, json_file, indent=2)

print("Conversion complete. Output written to jobs.json")
