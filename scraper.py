import requests
import csv
import json

def get_dealers(page=230):
    url = f'https://www.truckpaper.com/ajax/dealer/search'
    
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.truckpaper.com',
        'priority': 'u=1, i',
        'referer': 'https://www.truckpaper.com/dealer/directory/trucks-and-trailers-dealers/?Country=178&Page=238',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'x-xsrf-token': 'cwBllkj_q2HidIXseeqVp-wYeFER3IHyjrQn-HbB4IRlQAykQfOLAvJshKAt55ZH9YaXplldnGJiCpKgRhD-X8KstqF6m4ljj-MtFHHC7wNmhYISjmEWQKrsGfWyKZvioCas9-sEeQdRU0wY89HKyLRgfGWQImOzgrnWkUpwLGofoF7-B83p8qVo95A1'
    }

    cookies = {
        '__RequestVerificationToken': 'oDl6UI3m5b9-XR4i_N2wzn_VXK3afduSaGutWPTrB4dEojqcmIo7S84GUlGF8cBl3ngNIQ2',
        'ASP.NET_SessionId': 'sh235okdqxnbeaknkw1bohr3',
        'UserSettingsCookie': 'screenSize=1920|919',
        'sandhills-consent': '{"StrictlyNecessary":true,"Customization":false,"Advertising":false,"Analytics":false,"ShouldResync":true,"ActionDateTime":"2025-06-20T09:24:41.803Z","ConsentStatus":"DENY","WebAgreementID":165}',
        '__XSRF-TOKEN': 'i_sg8eiEf0cJfg2IDc9PhdcTmd5YfhAEyzQ560b69SuCGZ-moX85W8jXRNfSqRJVRHtVyteiNg5ae2A604iE-xK7y_cFjk0WLbwmN34cy5FMFili-KE73FYlwVJx1AVjIf6d9rN-SHXB4VPvSA4kNWUF3t_m_RvYBPEkNQ2',
        'reese84': '3:luqhphLKFeE3oxwA8wquYQ==:ED1oOfyg/dMqY5XuYMOYVzn1upS3LFLOisjGrKZ4pd8uanebjo7XqkZ9zHuiVhdXoy8mOnAPjKCwe5X9Zml3lBbRvIoHQfP+AdnG475i5cZfBOrjhbZiyKhbgJP6ukxSxH05/BuuF2NqrImfWYSmL5dZpO9gx+KYCHxwk0QsBDPf/EJzAdbgSeWqTYGVy2iBN2irIxkJicNrwW6lZ9QL3N6efSPiBI+M9AimEwPZJyr/qE0QTq61HTh3ZQv7gsd+9lOpsMGZjS6qQixtcZLVX2ZptKT4MwjajNUlRQfzj/yMHRXfEMx60qchuxEtzv3rPLiW8fSDlSVDg+f/1kzjNowyuCS+YKTAiJXnsRQa0QWy8yYPN8Q1Yxa30THYlXvdWppFLd7a54AnsIdeinvC68SbhXy2WlUi6o49ZJ52/Al3iIO/LsqMH3MWh6+lsfAwQx28BkID0+ArkXir6qcT3g==:pwCDu7FC2GlGDO935Qgf5JXmAm2gpMd9zHaXx/kDv2k=',
        'UserID': 'ID=iiK%2fxlgqP0TtdwXUzhvhosgINh9yxpoThbivahn8catRQeov6QqXntOmSxpoTdKsY92RYeD5WeNKpZt8ZhtABg%3d%3d&LV=AbwOM36xIaan4lAkM3xjHH69GoXNYFvUAhIcnbboojZP15MVMkWzz8bljBV0mmrjNbDpXbTGagq61B6jUPfrklKjGlkOOD9a',
        'BIGipServerwww.truckpaper.tradesites_http_pool': '92383424.20480.0000'
    }

    params = {
        'Country': '178',
        'Page': str(page),
        'lang': 'en-US'
    }

    data = {
        '__RequestVerificationToken': 'xTrgHOP2ec67bHHZKDG6tgwkl7QC39sCSXI3M0WUw9A1eO2fJ7Yskg-zu3S4oTtDKhOIww2'
    }

    try:
        response = requests.post(url, headers=headers, params=params, cookies=cookies, data=data)
        response.raise_for_status()
        try:
            with open(f'response_{page}.json', 'w') as f:
                json.dump(response.json(), f, indent=4)
        except Exception as e:
            print(f"Error saving JSON: {e}")
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def save_to_csv(dealers, filename='dealers.csv'):
    # Define the fields we want to save
    fields = ['DealerName', 'DealerAddress', 'DealerCityStatePostal', 'FormattedDealerPhoneNumber']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        
        # Write the header
        writer.writeheader()
        
        # Write dealer data
        for dealer in dealers:
            row = {field: dealer.get(field, '') for field in fields}
            writer.writerow(row)

def main():
    all_dealers = []
    page = 230  # Start from page 230
    
    while True:
        print(f"Fetching page {page}...")
        data = get_dealers(page)
        
        if not data or 'Dealers' not in data or not data['Dealers']:
            break
            
        all_dealers.extend(data['Dealers'])
        page += 1

    if all_dealers:
        print(f"Found {len(all_dealers)} dealers. Saving to CSV...")
        save_to_csv(all_dealers)
        print("Data has been saved to dealers.csv")
    else:
        print("No dealers found or error occurred")

if __name__ == "__main__":
    main() 