# phonebook.cz Automation for Email Recon

## Description

`phonebook.py` is a powerful Python script that automates the process of gathering email addresses associated with specific domains using the Phonebook.cz service. This tool is designed for both single domain queries and bulk domain processing, making it versatile for various email intelligence gathering needs.

## Requirements

- Python 3.6+
- `requests` library

## Usage

- Get your IntelX API_TOKEN from https://intelx.io/account?tab=developer

- For a single domain:
`python3 phonebook.py -u google.com`
- For a file containing multiple domains:
`python3 phonebook.py -l domains.txt`

- Ouput will be stored in the format `domain_email_output.txt` or `filename_email_output.txt`
