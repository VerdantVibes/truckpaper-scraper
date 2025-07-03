import json
import csv
import glob
import os
import re
from typing import List, Dict
from bs4 import BeautifulSoup

def extract_specs(specs: List[Dict]) -> Dict[str, str]:
    """Extract specs into a dictionary format"""
    return {spec['Key']: spec['Value'] for spec in specs}

def extract_horsepower(description: str) -> str:
    """Extract horsepower from description"""
    if not description:  # Handle None or empty string case
        return ''
        
    # Pattern to match: number before hp/HP
    match = re.search(r'(\d+)\s*[hH][pP]', description)
    if match:
        return match.group(1)
    return ''

def get_odometer_from_html(listing_id: str) -> str:
    """Get odometer reading from HTML file if it exists"""
    try:
        html_file = f'html_files/listing_{listing_id}.html'  # Changed path format
        if not os.path.exists(html_file):
            print(f"HTML file not found: {html_file}")  # Debug print
            return ''
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find OdometerWorks section and extract Value
        odometer_match = re.search(r'"OdometerWorks":\s*{[^}]*"Value":\s*"([^"]*)"', content)
        if odometer_match:
            value = odometer_match.group(1)
            return value
        else:
            print(f"No odometer match found in file: {html_file}")  # Debug print
                
    except Exception as e:
        print(f"Error reading odometer from HTML for listing {listing_id}: {e}")
    return ''

def get_fuel_type_from_html(listing_id: str) -> str:
    """Get fuel type from HTML file if it exists"""
    try:
        html_file = f'html_files/listing_{listing_id}.html'
        if not os.path.exists(html_file):
            return ''
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find FuelType section and extract Value
        fuel_match = re.search(r'"FuelType":\s*{[^}]*"Value":\s*"([^"]*)"', content)
        if fuel_match:
            return fuel_match.group(1)
                
    except Exception as e:
        print(f"Error reading fuel type from HTML for listing {listing_id}: {e}")
    return ''

def process_listing(listing: Dict, row_number: int) -> Dict:
    """Process a single listing to extract required fields"""
    specs = extract_specs(listing.get('Specs', []))
    location = listing.get('ListingLocation', {})
    description = listing.get('Description', '')
    
    # Extract horsepower once and use it for Engine_HP if not already present
    hp = extract_horsepower(description)
    engine_hp = specs.get('Engine HP', hp) if specs.get('Engine HP') else hp
    
    # Get odometer and fuel type using row number as listing ID
    listing_id = str(row_number)
    odometer = get_odometer_from_html(listing_id)
    engine_type = get_fuel_type_from_html(listing_id)
    
    return {
        'Category': listing.get('DisplayCategoryName', ''),
        'Price': listing.get('Price', ''),
        'Odometer': odometer,
        'Type': listing.get('DisplayCategoryName', ''),
        'Year': listing.get('Year', ''),
        'Model': listing.get('Model', ''),
        'DealerPhone': listing.get('RetailPhoneNumber', ''),
        'SerialNumber': listing.get('SerialNumber', ''),
        'City': location.get('City', ''),
        'State': location.get('State', ''),
        'Country': location.get('Country', ''),
        'PostalCode': location.get('PostalCode', ''),
        'Engine_Manufacturer': specs.get('Engine Manufacturer', ''),
        'Engine_Type': engine_type,
        'Engine_HP': engine_hp,
        'Description': description
    }

def save_to_csv(listings: List[Dict], filename: str = 'combined_listings.csv'):
    """Save processed listings to CSV file"""
    if not listings:
        print("No listings to save")
        return
        
    # Get fields from the first listing
    fields = listings[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(listings)

def main():
    all_listings = []
    row_number = 1  # Initialize row counter
    
    # Get all response_*.json files
    json_files = glob.glob('response_*.json')
    
    # Sort files by page number
    json_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
    
    print(f"Found {len(json_files)} JSON files to process")
    
    for json_file in json_files:
        page = json_file.split('_')[1].split('.')[0]
        print(f"Processing page {page}...")
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'Listings' not in data or not data['Listings']:
                print(f"No listings found in {json_file}")
                continue
                
            # Process each listing with row number
            for listing in data['Listings']:
                processed_listing = process_listing(listing, row_number)
                all_listings.append(processed_listing)
                row_number += 1  # Increment row counter
                
            print(f"Processed {len(data['Listings'])} listings from page {page}")
            
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
            continue

    if all_listings:
        print(f"Found total of {len(all_listings)} listings. Saving to CSV...")
        save_to_csv(all_listings)
        print("Data has been saved to combined_listings.csv")
    else:
        print("No listings found or error occurred")

if __name__ == "__main__":
    main() 