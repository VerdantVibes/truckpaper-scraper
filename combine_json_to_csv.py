import json
import csv
import glob
import os
from typing import List, Dict

def extract_specs(specs: List[Dict]) -> Dict[str, str]:
    """Extract specs into a dictionary format"""
    return {spec['Key']: spec['Value'] for spec in specs}

def process_listing(listing: Dict) -> Dict:
    """Process a single listing to extract required fields"""
    specs = extract_specs(listing.get('Specs', []))
    location = listing.get('ListingLocation', {})
    
    return {
        'Category': listing.get('DisplayCategoryName', ''),
        'Manufacturer': listing.get('ManufacturerName', ''),
        'SerialNumber': listing.get('SerialNumber', ''),
        'Dealer': listing.get('Dealer', ''),
        'DealerPhone': listing.get('RetailPhoneNumber', ''),
        'City': location.get('City', ''),
        'State': location.get('State', ''),
        'Country': location.get('Country', ''),
        'PostalCode': location.get('PostalCode', ''),
        'Description': listing.get('Description', ''),
        'Price': listing.get('Price', ''),
        'PaymentsAsLowAs': listing.get('Widgets', {}).get('PaymentsAsLowAs', ''),
        'UpdatedOn': listing.get('FormattedUpdatedOnTime', ''),
        'Upper_Hours': specs.get('Upper Hours', ''),
        'Lift_Capacity': specs.get('Lift Capacity', ''),
        'Stock_Number': specs.get('Stock Number', ''),
        'Transmission': specs.get('Transmission', ''),
        'Max_Boom_Length': specs.get('Max Main Boom Length', ''),
        'Winch': specs.get('Winch', ''),
        'Engine_Manufacturer': specs.get('Engine Manufacturer', '')
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
                
            # Process each listing
            processed_listings = [process_listing(listing) for listing in data['Listings']]
            all_listings.extend(processed_listings)
            print(f"Processed {len(processed_listings)} listings from page {page}")
            
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