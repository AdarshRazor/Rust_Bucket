import json
import random
import os
from typing import Dict, Any

# Sample file names (update as needed)
JSON_FILES = [
    '../docs/properties1.json',
    '../docs/properties2.json',
    '../docs/properties3.json',
]

MOCK_AMENITIES = ['has_pool', 'has_garage', 'has_garden']

def load_and_merge_properties(json_files):
    merged: Dict[str, Dict[str, Any]] = {}
    for file in json_files:
        if not os.path.exists(file):
            print(f'Warning: {file} not found, skipping.')
            continue
        with open(file, 'r') as f:
            data = json.load(f)
            for prop in data:
                prop_id = str(prop['id'])
                if prop_id not in merged:
                    merged[prop_id] = prop
                else:
                    merged[prop_id].update(prop)
    return list(merged.values())

def augment_with_mocked_fields(properties):
    for prop in properties:
        prop['school_rating'] = round(random.uniform(1, 10), 1)
        prop['commute_time'] = random.choice([10, 20, 30, 40, 50])  # in minutes
        prop['year_built'] = random.randint(1950, 2022)
        for amenity in MOCK_AMENITIES:
            prop[amenity] = random.choice([True, False])
    return properties

def main():
    properties = load_and_merge_properties(JSON_FILES)
    print(f'Loaded {len(properties)} unique properties.')
    properties = augment_with_mocked_fields(properties)
    with open('../docs/merged_properties.json', 'w') as f:
        json.dump(properties, f, indent=2)
    print('Merged and augmented properties saved to ../docs/merged_properties.json')

if __name__ == '__main__':
    main() 