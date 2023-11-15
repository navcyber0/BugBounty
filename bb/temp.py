import os
import json

# Specify the path to the data.json file
data_file_path = os.path.join(os.getcwd(), 'data.json')

# Check if the data.json file exists
if os.path.exists(data_file_path):
    # Read the JSON data from data.json
    with open(data_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Extract the alias values and ipaddr values
    alias_values = []
    ipaddr_values = []
    for domain in data:
        alias_values.extend(data[domain].get('alias', []))
        ipaddr_values.extend(data[domain].get('ipaddr', []))

    # Specify the path to the knockpy_domain.txt file
    domain_output_file_path = os.path.join(os.getcwd(), 'knockpy_domain.txt')

    # Write the alias values to the knockpy_domain.txt file
    with open(domain_output_file_path, 'w') as domain_output_file:
        for alias_value in alias_values:
            domain_output_file.write(alias_value + '\n')

    # Specify the path to the knockpy_ip.txt file
    ip_output_file_path = os.path.join(os.getcwd(), 'knockpy_ip.txt')

    # Write the ipaddr values to the knockpy_ip.txt file
    with open(ip_output_file_path, 'w') as ip_output_file:
        for ipaddr_value in ipaddr_values:
            ip_output_file.write(ipaddr_value + '\n')

    print("Alias values extracted and saved to knockpy_domain.txt.")
    print("IP address values extracted and saved to knockpy_ip.txt.")
else:
    print("data.json file not found.")
