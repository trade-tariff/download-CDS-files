import requests
import sys
import os
import wget
from dotenv import load_dotenv


# Get credentials
load_dotenv('.env')

domain = os.getenv('domain')
client_secret = os.getenv('client_secret')
client_id = os.getenv('client_id')

# Request auth token
url = domain + "oauth/token"
payload = "client_secret={}&client_id={}&grant_type=client_credentials".format(client_secret, client_id)
headers = {"content-type": "application/x-www-form-urlencoded"}
response = requests.request("POST", url, data = payload, headers = headers)
if response.status_code != 200:
    print(response.text)
    sys.exit()

my_array = response.json()
access_token = my_array["access_token"]

# Access data
url = domain + "bulk-data-download/list/TARIFF-DAILY"
headers = {
    "User-Agent": "Trade Tariff Backend",
    "Accept": "application/vnd.hmrc.1.0+json",
    "Authorization": "Bearer " + access_token
}
response = requests.request("GET", url, headers=headers)
print(response.text)
print(response.status_code)

for file_entry in response.json():
    filename = file_entry['filename']
    download_url = file_entry['downloadURL']
    print(f'Downloading {filename}...')
    wget.download(download_url, out='.', bar=None)
