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

    cookies = {
        'UserSettingsCookie': 'screenSize=1920|919',
        'sandhills-consent': '{"StrictlyNecessary":true,"Customization":false,"Advertising":false,"Analytics":false,"ShouldResync":true,"ActionDateTime":"2025-06-20T09:24:41.803Z","ConsentStatus":"DENY","WebAgreementID":165}',
        '__RequestVerificationToken': 'p-34dOmgAm660j5p4GCSECaCCVEt7uOhkjIK8GXThETS0mdmw9oJnVXnRitKbkRIBcmmBw2',
        '__XSRF-TOKEN': 'TSIxDDv3qFnGVmvIDFZtiWO2dpa8--gqYTCtlTRCeQnxrxsn-zaRWK8IgEebiq3106scyfi1rYGCE8UqZHqqjj4j1-mHDzOv1pTYlVnZh7uWhNuJWVoS8zdujax8CgsiDaCSn7Hg037eFbEZjf8XAbwCevmhkTWZ_VAckA2',
        'ASP.NET_SessionId': 'imdpjjl2nb4hy2qneau2qcb5',
        'reese84': '3:2G0sNU01E7hJeR532hd7BQ==:I+q88yHlxLnBEhS6b8vyF2Yg7jEg6OYXmORaRXnxQnYevghGKWB66D6ZTG71vEXW3jMNcvgOfalCxGo+qSlC05nb0sh9MhZR4gqzna6dRtb3gdNnDEOBaAa7//j+NpWCVcTXcPUTdJYCn/HBDN5B7Ys7obD4DcPpaqf2IieykcAHAtCO4gKzkHV2jk+tYJt6vtB1cTj+W1lMdpXeijWJ4YuxvqrAZxRQjRb7JIkCPpwrXFOK6BSQfQ72ovkA4MuXhuhPnKpmuabMuey0s38DyHsarW0jDYdhcHP6SF1NK3jwSu8bPirS1BZJtR8bydQf5uhZVefYqcuyYcIreM0GCfkDHIEkZgyg05FBf/GMPYGc24tGfvXHJG8uga1MtxtMm5uDOpOWDVUoC0/zznJy8DKW06xoyULgC4pga41RlIRcRk3icPk9FBACrcFo7TGlsoLZL1DIsm+OKrD1bLxE1k46HbWF6032gMAJMjScwdOS1VNtvUsfd9KVBeJo03U/FA73nEIcb+LQQOPsKlfQxw==:OxKHONbOX9CbeukfLTwtxaoUqelx9sge2Ibpc7H09yA=',
        'UserID': 'ID=iiK%2fxlgqP0TtdwXUzhvhosgINh9yxpoThbivahn8catRQeov6QqXntOmSxpoTdKsY92RYeD5WeNKpZt8ZhtABg%3d%3d&LV=Irm0i7%2fOpca5CpBHT2RKoIJzGKrRFysDR%2fjbmGHM5dqZu9lTv8TuIMBcC8WX1hyApXy272cxdJYsbaA29ktcU83PlnjR5aJB',
        'BIGipServerwww.truckpaper.tradesites_http_pool': '4265650368.20480.0000'
    }

    params = {
        'ListingType': 'For Retail',
        'sort': '1',
        'page': str(page),
        'lang': 'en-US'
    }

    try:
        response = requests.get(url, headers=headers, params=params, cookies=cookies)
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