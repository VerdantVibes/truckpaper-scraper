import requests
import csv
import json
import time
from typing import List, Dict, Optional

def get_listings(page: int = 1) -> Optional[Dict]:
    url = 'https://www.truckpaper.com/ajax/listings/ajaxsearch'
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'referer': 'https://www.truckpaper.com/listings/search?ListingType=For%20Retail&page=357',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'x-xsrf-token': 'UMsT-QOB1bhM9hvwIBt0ysigEMcWpAaNWcyzEb2-yVKqw_SW7JRloGrN05lz_ixEoB29owPhxEw7LouvAYnf1CxNEn0etMcK64X3Vt4qdnJNF9mUdZ7zZvCSJ08uFKCBcEPFSNiadl6aknTdxHzCC_MPBilY4vBZySLR1SJG-gcRZY1LGsqn4V-xW_41'
    }

    # Function to parse cookie string into dictionary
    def parse_cookies(cookie_str):
        cookies = {}
        pairs = cookie_str.split(';')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                cookies[key.strip()] = value.strip()
        return cookies

    # Raw cookie string
    cookie_str = 'UserSettingsCookie=screenSize=1920|919; reese84=3:SAqMoht065PGqPreIU6nUg==:xFxGA4tTlzafEeIp0ZuqV7zt3saIvonVRzwOibpVNq4kAShwg48tXVZj8RJPA8P2D3Ubr6XFlqAgOOz2qz5uKcB2rPFWJuzAMv9VMmaT40DNR2BPPhKtbam7uvZjrRIVazw2C/tCCRitY/j/VpgOwlrqkwlbcKW40SDy1w5PqccaibM4vdwM4mLNW5axSRayXlubTjzy+0rUzmDTg72a8FP0c274TqJzKreuVPeNTw/M9rRRZmXv5YDmLnsBmhgquLVaCGTnwgmysOVBSy9R8IostQteDC8QTtsZVbQblNqmD63Im7itU8mU6DBomcGrh8TSEeFQScIKwmLgWYGqGPVeRFq5lG9nk3r2salK08lVh0gM0b2hgTXA4vOPN7RD7a23JAwg75OPp+aDCrRORG+3TnBzOhZWY8UidMmpTN9KpQUGit0N6MBIew94WAaEgdb+ECtvmQMe9xh5ExAKc1WkL0VoXp/3MzKIV4TG8KtwxkROQVb8rozTzLtbqXh943WnWj3v4c/vJ6opjzad3g==:JvQT/EftCXyhcPuFlRyYEQKo9XjAkyxhl+HWnxv13Jg=; UserID=ID=iiK%2fxlgqP0TtdwXUzhvhosgINh9yxpoThbivahn8catRQeov6QqXntOmSxpoTdKsY92RYeD5WeNKpZt8ZhtABg%3d%3d&LV=eLb7QIw%2fod8KJdD%2bskaHT7Cq69UGV%2bX7pnI7YkCMnXyekPOVcnLlUY3DAdsJZ0ufN8Tn3Jt2CH1gAAeN7yHiNdS4MqnzTIxg; __RequestVerificationToken=3UlC9clBXf2cjfg9tOvlR7HHnoPqZM5vbAuFNT9kRZ2Egi3Ab_lefJ1wzEzfkauDw75ThQ2; __XSRF-TOKEN=zI-XmdNdHgylHLx5rTCYlrB22Ph4l7soRPMZMcRVRtAxDPKAszb2BSNn7z3JYZYilSiKVbs74-kKF3jS2XpyyeFlliqnp5frqmpu4fvgcjw7stCkKh5uXrAW2LWekhoSk864XZ1J9oUeLX3zuIF4W3OF12bgl5Znc1wpRQ2; BIGipServerwww.truckpaper.tradesites_http_pool=759343296.20480.0000; sandhills-consent={"StrictlyNecessary":true,"Customization":false,"Advertising":false,"Analytics":false,"ShouldResync":true,"ActionDateTime":"2025-07-21T02:36:45.618Z","ConsentStatus":"DENY","WebAgreementID":165}'

    params = {
        'ListingType': 'For Retail',
        'sort': '1',
        'page': str(page),
        'lang': 'en-US'
    }

    try:
        response = requests.get(url, headers=headers, params=params, cookies=parse_cookies(cookie_str))
        response.raise_for_status()
        
        # Save raw response for debugging (optional)
        with open(f'response_{page}.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
            
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

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

def save_to_csv(listings: List[Dict], filename: str = 'listings.csv'):
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
    page = 358  # Start from page 358
    
    while True:
        print(f"Fetching page {page}...")
        data = get_listings(page)
        
        if not data:
            print("Failed to fetch data. Stopping.")
            break
            
        if 'Listings' not in data or not data['Listings']:
            print("No more listings found. Stopping.")
            break
            
        # Process each listing
        processed_listings = [process_listing(listing) for listing in data['Listings']]
        all_listings.extend(processed_listings)
        print(f"Processed {len(processed_listings)} listings from page {page}")
        
        page += 1
        # Add a small delay between requests to be respectful to the server
        time.sleep(2)

    if all_listings:
        print(f"Found total of {len(all_listings)} listings. Saving to CSV...")
        save_to_csv(all_listings)
        print("Data has been saved to listings.csv")
    else:
        print("No listings found or error occurred")

if __name__ == "__main__":
    main() 