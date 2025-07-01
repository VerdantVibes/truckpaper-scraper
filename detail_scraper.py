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

def get_html_content(url: str, sequence: int) -> bool:
    """Download HTML content for a given URL"""
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
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

    cookies = {
        'sandhills-consent': '{"StrictlyNecessary":true,"Customization":false,"Advertising":false,"Analytics":false,"ShouldResync":true,"ActionDateTime":"2025-06-20T09:24:41.803Z","ConsentStatus":"DENY","WebAgreementID":165}',
        'UserSettingsCookie': 'screenSize=1920|919',
        '__RequestVerificationToken': 'QwmNWUhiDZ8egYKvx1JHLhd9tuJvsJbHAzeiAMCQqCBiI80VR81NGIdN1KMRpz5gtbXkLQ2',
        '__XSRF-TOKEN': 'F8D2h-7GvHLKFbrH-ALlm68k_hPqd4iAVHTsOPIUD_NEwfvvDe5_wMMyghPD2YlDyAZwmng47bZVwen6wKtACOn24xryrE9VB91n5JLfp9153rUs-BCoO29YhprLEbYSpLufnBkpWcHIrg1Zc7bMgshnFvUkvMAjDnxvjQ2',
        'ASP.NET_SessionId': 'b0vyfgbod2tiqzqzfqdbaliu',
        'BIGipServerwww.truckpaper.tradesites_http_pool': '1820502208.20480.0000',
        'reese84': '3:iAm/99UiMmlfshXmsgCreA==:ob55eymgUeRd+tbSjXEY5dMHVrTCyFpyX/T0Zi7zn2ZoB3MW1+vGbwy9YTOzQsEIoob1+eYBmaYeIPkim6EnQyotxkPVdtpzklp8GubDooFwZXQp0NICafbC3iXJPjGU4AVZNbAvkaEUM+iWX/p6VzPI+KIMxO/BVJdvMPMWfBAYPQaZALQkJnwVUoJiUkKt6CIAEWyY5aeMljerbiHakFIXud5qcYr97CCPMUitDhGNx2bY43jxPM/y+Do+Vp7VBNByQ7Km2da0nn+1EbVTGIesQupfDBHdnlDmARFyszruQYnx9kDhbB34HJOlw+fPZuuB1xaD+j80BF/M/ISKD1xJboYegEe889Sb5AG/EXAY0wkeldn8JM3HiowuEY1epNDvWQERkd4WF8eXFAFaGwkWoUmhw6dm0ZJg+MSHMrSf1X/cvS6VCa/puhkD96Hp8yTcGNbmy8GIrSCGjwEiEPweoa143kKJ5qUUw0dUmRB1EC/V9BLjzVVIW/q4xAi8jyY1xgRsA7j600pDB34Ztg==:x2lW3gGD6Zhxyjh/BUvyWbxDlgiYfAAVsl9NPiTvyDo=',
        'UserID': 'ID=iiK%2fxlgqP0TtdwXUzhvhosgINh9yxpoThbivahn8catRQeov6QqXntOmSxpoTdKsY92RYeD5WeNKpZt8ZhtABg%3d%3d&LV=nLFEqqhaVBsEgI1Gf%2fPnTwR89tiVAwD283Mu54DepbU8Jp1lchu6QZWnmNlj5VLnLQ9GNjXE4zSRfklHGLcvyAiS571Ktueb'
    }

    try:
        # Create html_files directory if it doesn't exist
        os.makedirs('html_files', exist_ok=True)
        
        response = requests.get(url, headers=headers, cookies=cookies)
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
        
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def process_url_by_sequence(sequence: int, urls: List[str]):
    """Process URL by sequence number and continue sequentially"""
    total_urls = len(urls)
    
    for current_seq in range(sequence - 1, total_urls):
        current_num = current_seq + 1
        url = urls[current_seq]
        print(f"Processing URL {current_num} of {total_urls}: {url}")
        
        if get_html_content(url, current_num):
            time.sleep(2)  # Add delay between successful requests
        else:
            print(f"Failed to process URL {current_num}. Stopping process...")
            return  # Stop processing on first failure

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