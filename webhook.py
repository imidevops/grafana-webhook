from flask import Flask, request
import requests
import re

APP = Flask(__name__)

def extract_ip_addresses_from_file(file_path):
    ip_addresses_with_services = []
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

    with open(file_path, 'r') as file:
        for line in file:
            ip_address = re.search(ip_pattern, line).group()
            service_name = line.strip().split(',', 1)[1]
            ip_addresses_with_services.append((ip_address, service_name))

    return ip_addresses_with_services

@APP.route('/sendsms', methods=['POST'])
def sendsms():
    number = "+" + request.args.get('number')
    print(number)
    message = request.json["message"]
    print(message)

    data = message

    blocks = data.strip().split('\n\n')
    ips = []
    values = []
    alert_template = ""

    for block in blocks:
        # Extract IP address from the alert block
        ip_match = re.search(r'instance = (\d+\.\d+\.\d+\.\d+):9100', block)
        if ip_match:
            ip = ip_match.group(1)
            ips.append(ip)

        # Extract the value from the alert block
        value_match = re.search(r'Value: B=([\d\.]+)', block)
        if value_match:
            value = round(float(value_match.group(1)))
            values.append(value)

        # Extract alert template
        alert_match = re.search(r'(Grafana_Alert .+)', block)
        if alert_match:
            alert_template = alert_match.group(1).replace("= ", "\n")  # Replace '=' with a newline

    if alert_template:
        # Get the IPs and services from the file
        ip_services = extract_ip_addresses_from_file('./servers.txt')

        # Match the IPs from the alert with the corresponding services from the file
        matched_alerts = []
        for alert_ip, value in zip(ips, values):
            # Find the corresponding service for the alert IP
            for file_ip, service in ip_services:
                if file_ip == alert_ip:
                    matched_alerts.append('{} "{}" is {}'.format(alert_ip, service, value))
                    break

        # Create the final alert message
        alert_message = alert_template + "\n" + "\n".join(matched_alerts)
        output = f'{alert_message}'
        print(output)
    else:
        output = "No Grafana_Alert template found."
        print(output)

    # Prepare the text for the URL
    Text = output.replace(" ", "+")
    print(Text)

#    noc = ['03038413937', '03214515305']
    noc=['03235515598','03038413937']
    for MSISDNS in noc:
        url = "http://*****:13013/cgi-bin/sendsms?username=******&password=******from=5188&to={}&text={}&MT&charset=utf-8".format(MSISDNS, Text)
        print(url)
        requests.get(url, verify=False, timeout=5)

    return 'Hello, World!'

APP.run()
