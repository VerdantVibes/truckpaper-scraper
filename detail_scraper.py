import json
import csv
import glob
import os
import requests
import time
from typing import List, Dict
from urllib.parse import urljoin

def collect_detail_urls() -> List[str]:
    """Collect all detail URLs from JSON files and save to CSV"""
    urls = []
    base_url = "https://www.truckpaper.com"
    
    # Get all response_*.json files
    json_files = glob.glob('response_*.json')
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
                
            # Extract detail URLs
            for listing in data['Listings']:
                if 'DetailUrl' in listing and listing['DetailUrl']:
                    full_url = urljoin(base_url, listing['DetailUrl'])
                    urls.append(full_url)
            
            print(f"Found {len(urls)} URLs so far...")
            
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
            continue

    # Save URLs to CSV
    with open('detail_urls.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['URL'])
        for url in urls:
            writer.writerow([url])
    
    print(f"Saved {len(urls)} URLs to detail_urls.csv")
    return urls

def log_failed_url(url: str, sequence: int, error: str):
    """Log failed URLs to a CSV file"""
    file_exists = os.path.exists('failed_urls.csv')
    
    with open('failed_urls.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Sequence', 'URL', 'Error'])
        writer.writerow([sequence, url, error])

def get_html_content(url: str, sequence: int) -> bool:
    """Download HTML content for a given URL"""
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'https://www.truckpaper.com/listings/search?ListingType=For%20Retail',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
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

    # Raw cookie string - you can update this as needed
    cookie_str = 'sandhills-consent={"StrictlyNecessary":true,"Customization":false,"Advertising":false,"Analytics":false,"ShouldResync":true,"ActionDateTime":"2025-06-20T09:24:41.803Z","ConsentStatus":"DENY","WebAgreementID":165}; UserSettingsCookie=screenSize=1920|919; __RequestVerificationToken=QWVGlkJD84vwUrNJOQDs5aJEo8A5jXAj8ymQLcC31YBXskmL4LW96uVpO_ZScIOcD0pVYw2; ASP.NET_SessionId=in3p33xiqhbv315vck0bwyy5; __XSRF-TOKEN=gC21MxWyv7GsFuSL4UQ3opFCkviyIiCTxGsOT1UO9ydma_9FodBlnpfPNcK3TeIRzT-oCEB3HiB2n2OUuaRMMIFWrO7tR8vDiZuGpqwUSyD4t7IQiGLrmYC-__Pca2wRCyzUkh2KhsiKyOIlZkQ094dyum0KVPzNHIcW-w2; reese84=3:eXc0l6vYLbd5baMbr3ktUQ==:Gm9IwpReHrLFOSbWZQqYuBfksfYDuqBv67ghSwVXwpYzs64P4agnnq/DfcTFdnwWVlgHBwB8wlBSOWpwkWgQdV6vTtVBNm9a+TD2D+wIdoKBI8DqGFJLVmDsdFhk6CgHG5IMy+5qT9g0ui5JnZDUCB6lVrKImQBvr88DCU4G0K0UZlczcnAIanLHdmEU49f5hkeChgSQBPDjzJh4J+R68IDjNPs3qYa9hQw7GPkv+aSqtqeEVZLheKeRSUaLV9qigD++8P+njcU2Na9jTaodUh9Lo6oYiL5uwJfBe1hH5f8ZdupdVTBPBlqJvNDHY6IlkXYdT7u3zwDCuc5H0Uy/rAFYnCgdfgOWKVsf4AlYxSMP9G70n14pr37oPsTXJOBj3cOWuNNHIG4pIA0MIT5x+2ZFOnZxBZ04aEg3GNo75kJTQtXd1rgMtqtXf849+g410jorpiZbZ0QXKeRz548be1JxPmSLSupF9OLSvC43/0vMtJXuL2aT9z2lJ9tTA+RU:rQYsGTmwDdBImDoafDDwAnze379RY5fK8VZb2yUV2Sk=; UserID=ID=iiK%2fxlgqP0TtdwXUzhvhosgINh9yxpoThbivahn8catRQeov6QqXntOmSxpoTdKsY92RYeD5WeNKpZt8ZhtABg%3d%3d&LV=LKJQ%2f71Q6oTRt58jbV3d7R2jySrJ4xvPRwUjSPeo160nrrNiKOAjjYf7Bqr90qcZ4eT3AzRhh5egYKAbRhfEFyz7nE3Fb9%2fq; BIGipServerwww.truckpaper.tradesites_http_pool=92383424.20480.0000'

    try:
        # Create html_files directory if it doesn't exist
        os.makedirs('html_files', exist_ok=True)
        
        # Use the raw cookie string directly in the request
        response = requests.get(url, headers=headers, cookies=parse_cookies(cookie_str))
        
        # Handle 404 errors separately
        if response.status_code == 404:
            print(f"URL not found (404): {url}")
            log_failed_url(url, sequence, "404 Not Found")
            return None  # Return None for 404 errors
            
        response.raise_for_status()
        
        # Check for "Pardon Our Interruption" page
        if "Pardon Our Interruption" in response.text:
            print("Detected 'Pardon Our Interruption' page. Access might be blocked.")
            return False
        
        # Save HTML content
        filename = f'html_files/listing_{sequence}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"Successfully saved {filename}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        if not isinstance(e, requests.exceptions.HTTPError) or e.response.status_code != 404:
            return False  # Stop process for non-404 errors
        log_failed_url(url, sequence, str(e))
        return None  # Continue process for 404 errors

def process_url_by_sequence(sequence: int, urls: List[str]):
    """Process URL by sequence number and continue sequentially"""
    total_urls = len(urls)
    
    for current_seq in range(sequence - 1, total_urls):
        current_num = current_seq + 1
        url = urls[current_seq]
        print(f"Processing URL {current_num} of {total_urls}: {url}")
        
        result = get_html_content(url, current_num)
        if result is False:  # Stop on errors except 404
            print(f"Failed to process URL {current_num}. Stopping process...")
            return
        elif result is True:  # Successful download
            time.sleep(2)  # Add delay between successful requests
        # If result is None (404 error), continue to next URL

def main():
    # First, collect all URLs if they haven't been collected yet
    if not os.path.exists('detail_urls.csv'):
        print("Collecting detail URLs...")
        collect_detail_urls()
    
    try:
        # Read URLs from CSV
        with open('detail_urls.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            urls = [row[0] for row in reader]
        
        # Get starting sequence number
        while True:
            try:
                sequence = input("Enter starting sequence number: ")
                sequence = int(sequence)
                if 1 <= sequence <= len(urls):
                    break
                print(f"Please enter a number between 1 and {len(urls)}")
            except ValueError:
                print("Please enter a valid number")
        
        # Process URLs sequentially from the starting sequence
        process_url_by_sequence(sequence, urls)
        print("Process completed.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 