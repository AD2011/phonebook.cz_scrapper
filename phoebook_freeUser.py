import requests
import json
import argparse
import os

TOKEN = "API_TOKEN_HERE"

def get_token(domain, target):
    url = f"https://free.intelx.io:443/phonebook/search?k={TOKEN}"
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
        "target": target,
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
    url = f"https://free.intelx.io:443/phonebook/search/result?k={TOKEN}&id={key}&limit=1000000"
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
        exit('[-] API Limit Exhausted, Upgrade or Change API Key')
    return response.text

def parse_items(items, domain, target_type, output_file):
    items = json.loads(items)['selectors']
    with open(output_file, 'a') as file:
        file.write(f"\n--- {domain} ({target_type}) ---\n")
        for item in items:
            value = item['selectorvalue']
            print(value)
            file.write(value + '\n')
    print(f'\n[+] Added {domain} {target_type} data to {output_file}')
    print("")

def process_domain(domain, target, target_type, output_file):
    key = get_token(domain, target)
    data = make_request(key)
    parse_items(data, domain, target_type, output_file)

def read_domains_from_file(file_path):
    with open(file_path, 'r') as file:
        return [domain.strip() for domain in file.readlines()]

def main():
    parser = argparse.ArgumentParser(description="Phonebook.cz scrapper")
    parser.add_argument("-u", "--url", help="Process a single domain")
    parser.add_argument("-f", "--file", help="File containing list of domains")
    parser.add_argument("-e", "--email", action="store_true", help="Search for emails")
    parser.add_argument("-s", "--subdomains", action="store_true", help="Search for subdomains")
    parser.add_argument("-l", "--links", action="store_true", help="Search for links")
    args = parser.parse_args()

    if not (args.email or args.subdomains or args.links):
        print("Please specify at least one of: --email, --subdomains, or --links")
        return

    targets = []
    process_types = []
    if args.email:
        targets.append((2, "email"))
        process_types.append("email")
    if args.subdomains:
        targets.append((1, "subdomain"))
        process_types.append("subdomain")
    if args.links:
        targets.append((3, "link"))
        process_types.append("link")

    process_suffix = "_".join(process_types)

    if args.url:
        output_file = f"{args.url}_{process_suffix}_output.txt"
        for target, target_type in targets:
            process_domain(args.url, target, target_type, output_file)
    elif args.file:
        domains = read_domains_from_file(args.file)
        output_file = f"{os.path.splitext(args.file)[0]}_{process_suffix}_output.txt"
        for domain in domains:
            print(f"Processing domain: {domain}")
            for target, target_type in targets:
                process_domain(domain, target, target_type, output_file)
    else:
        print("Please provide either a single domain (-u) or a file with multiple domains (-f)")

    if args.url or args.file:
        print(f"\n[+] All results saved to {output_file}")

if __name__ == '__main__':
    print('[+] Running Phonebook.cz scrapper!\n')
    main()
