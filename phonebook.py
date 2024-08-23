import requests
import json
import argparse
import os

TOKEN = "YOUR_TOKEN_HERE"

def get_token(domain):
    url = f"https://2.intelx.io:443/phonebook/search?k={TOKEN}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://phonebook.cz",
        "Dnt": "1",
        "Referer": "https://phonebook.cz/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Te": "trailers"
    }
    json_data = {
        "maxresults": 10000,
        "media": 0,
        "target": 2,
        "term": domain,
        "terminate": [None],
        "timeout": 20
    }
    response = requests.post(url, headers=headers, json=json_data)
    if response.status_code == 402:
        exit('[-] Your IP is rate limited. Try switching your IP address then re-run.')
    return response.text

def make_request(key):
    key = json.loads(key)['id']
    url = f"https://2.intelx.io:443/phonebook/search/result?k={TOKEN}&id={key}&limit=1000000"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Origin": "https://phonebook.cz",
        "Dnt": "1",
        "Referer": "https://phonebook.cz/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Te": "trailers"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 402:
        exit('[-] Your IP is rate limited. Try switching your IP address then re-run.')
    return response.text

def parse_items(items, output_file):
    with open(output_file, 'w') as file:
        items = json.loads(items)['selectors']
        for item in items:
            email = item['selectorvalue']
            print(email)
            file.write(email + '\n')
    print(f'\n[+] Done! Saved to {output_file}')

def process_domain(domain):
    key = get_token(domain)
    emails = make_request(key)
    output_file = f"{domain}_output.txt"
    parse_items(emails, output_file)

def read_domains_from_file(file_path):
    with open(file_path, 'r') as file:
        return [domain.strip() for domain in file.readlines()]

def main():
    parser = argparse.ArgumentParser(description="Phonebook.cz scraper")
    parser.add_argument("-u", "--url", help="Search emails for a single domain")
    parser.add_argument("-l", "--list", help="File containing list of domains")
    args = parser.parse_args()

    if args.url:
        process_domain(args.url)
    elif args.list:
        domains = read_domains_from_file(args.list)
        output_file = os.path.splitext(args.list)[0] + "_email_output.txt"
        with open(output_file, 'w') as out_file:
            for domain in domains:
                print(f"Processing domain: {domain}")
                print("------------------------------")
                key = get_token(domain)
                emails = make_request(key)
                items = json.loads(emails)['selectors']
                for item in items:
                    email = item['selectorvalue']
                    out_file.write(email + '\n')
        print(f'\n[+] Done! Saved to {output_file}')
    else:
        print("Please provide either a single domain (-u) or a file with multiple domains (-l)")

if __name__ == '__main__':
    print('[+] Running phonebook.cz scraper!\n')
    main()