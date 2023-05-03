import requests

import os
import requests

# API key
API_KEY = ''
# Input File
PHONE_FILE = 'input/phones.txt'

# Create the output directory if it does not exist
if not os.path.exists('output'):
    os.mkdir('output')

# Create the landlines.txt file if it does not exist
landline_file = 'output/landlines.txt'
if not os.path.exists(landline_file):
    with open(landline_file, 'w') as f:
        pass

# Create the mobiles.txt file if it does not exist
mobile_file = 'output/mobiles.txt'
if not os.path.exists(mobile_file):
    with open(mobile_file, 'w') as f:
        pass


def normalize_phone_number(phone_number_input):
    # Remove all non-digit characters from the phone number
    digits = ''.join(filter(str.isdigit, phone_number_input))

    # Check if the phone number starts with a valid country code
    if digits.startswith('1') and len(digits) == 11:
        # Phone number is in North American format, use country code +1
        return '1' + digits[1:]
    elif len(digits) == 10:
        # Phone number is in local format, use country code +1 and national format
        return '1' + digits
    else:
        # Phone number is in an invalid format
        return None


def validate_phone_number(api_key, phone_number_input):
    # Normalize the phone number to international format
    normalized_phone_number = normalize_phone_number(phone_number_input.strip())

    # Check if the phone number is valid
    if normalized_phone_number is None:
        print(f'Invalid phone number format: {phone_number_input.strip()}')
        return
    # Construct the API request URL
    url = f'https://api.apilayer.com/number_verification/validate?number={normalized_phone_number}'

    payload = {}
    headers = {
        "apikey": api_key
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)

    status_code = response.status_code

    # Check if the API request was successful
    if status_code == 200:
        # Parse the API response as JSON
        data = response.json()

        # Determine if the phone number is a landline or mobile number
        if data['line_type'] == 'landline':
            # Write the landline number to the landlines.txt file
            with open(landline_file, 'a') as f:
                f.write(normalized_phone_number + '\n')
            return 'landline'
        elif data['line_type'] == 'mobile':
            # Write the mobile number to the mobiles.txt file
            with open(mobile_file, 'a') as f:
                f.write(normalized_phone_number + '\n')
            return 'mobile'
        else:
            # Unknown line type
            print(f'Unknown line type for number {normalized_phone_number}: {data["line_type"]}')
    else:
        # API request failed
        print(f'Failed to validate phone number {normalized_phone_number}: {status_code}')


# Open the input file and read the phone numbers
with open(PHONE_FILE, 'r') as f:
    phone_numbers = f.readlines()
    num_numbers = len(phone_numbers)

    # Loop through each phone number
    for i, phone_number in enumerate(phone_numbers):
        # Check if the phone number is a landline or mobile number
        result = validate_phone_number(API_KEY, phone_number)

        # Output progress report
        print(f'Checked number {phone_number.strip()}. Result - {result}. Current progress: {i + 1}/{num_numbers}')

print(f'Phone checking complete, checked {num_numbers} numbers')
