# phonebook.cz Automation for Recon

`phonebook.py` is a powerful Python script that automates the process of gathering email addresses, subdomains and links associated with specific domains using the Phonebook.cz service. This tool is designed for both single domain queries and bulk domain processing, making it versatile for various email intelligence gathering needs.

## Usage

- Get your IntelX API_TOKEN from https://intelx.io/account?tab=developer

- For a single domain:
`python3 phonebook.py -u google.com [OPTIONS]`
- For a file containing multiple domains:
`python3 phonebook.py -f domains.txt [OPTIONS]`

### Options

- `-e` or `--email`: Search for email addresses
- `-s` or `--subdomains`: Search for subdomains
- `-l` or `--links`: Search for links

- You can use multiple options at once. For example:
- `python3 phonebook.py -u example.com -e -s -l`
- `python3 phonebook.py -f domain_list -e -s -l`

## Output

The script will display the discovered information in the console and save all results to a single output file. The output file name will reflect the domain name or filename and option selected

- For single domain: `{domain}_{process}_output.txt`
- For multiple domains: `{input_filename}_{process}_output.txt`

Where `{process}` is a combination of "email", "subdomain", and/or "link" based on the options selected.

## Run as an executable

Make a file at `/usr/bin` or any other folder in `$PATH` and make it executable by running `chmod +x <filename>`

```
#!/bin/sh

exec python3 /<path-to>/phonebook.py "$@"

```
