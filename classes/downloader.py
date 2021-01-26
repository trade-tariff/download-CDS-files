import requests
import sys
import os
import wget
from dotenv import load_dotenv
import zipfile
from shutil import copyfile
from classes.cds_file import CdsFile


class Downloader(object):
    def __init__(self):
        # Get credentials
        load_dotenv('.env')
        self.domain = os.getenv('domain')
        self.client_secret = os.getenv('client_secret')
        self.client_id = os.getenv('client_id')
        self.IMPORT_FOLDER = os.getenv('IMPORT_FOLDER')
        self.cds_files = []

        self.get_access_token()

    def get_access_token(self):
        # Request auth token
        url = self.domain + "oauth/token"
        payload = "client_secret={}&client_id={}&grant_type=client_credentials".format(
            self.client_secret, self.client_id)
        headers = {"content-type": "application/x-www-form-urlencoded"}
        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code != 200:
            print(response.text)
            sys.exit()

        my_array = response.json()
        self.access_token = my_array["access_token"]

    def download_files(self):
        # Access data
        url = self.domain + "bulk-data-download/list/TARIFF-DAILY"
        headers = {
            "User-Agent": "Trade Tariff Backend",
            "Accept": "application/vnd.hmrc.1.0+json",
            "Authorization": "Bearer " + self.access_token
        }
        response = requests.request("GET", url, headers=headers)

        files = response.json()
        for file_entry in files:
            cds_file = CdsFile()
            cds_file.filename = file_entry['filename']
            cds_file.download_url = file_entry['downloadURL']
            self.cds_files.append(cds_file)

        self.cds_files = sorted(self.cds_files, key=lambda x: x.filename, reverse=True)

        for file_entry in self.cds_files:
            resource_path = os.path.join(os.getcwd(), "resources")
            zip_path = os.path.join(resource_path, "zip")
            xml_path = os.path.join(resource_path, "xml")
            filename = file_entry.filename
            download_url = file_entry.download_url
            zip_filename = os.path.join(zip_path, filename)
            
            if os.path.isfile(zip_filename):
                print(f'{filename} already exists, skipping...')
            else:
                print(f'Downloading {filename}...')
                wget.download(download_url, out=zip_path, bar=None)
                zfile = zipfile.ZipFile(zip_filename)
                zfile.extractall(xml_path)
                unzipped_files = zfile.filelist
                if unzipped_files:
                    xml_filename = unzipped_files[0].filename

                    # Copy to the import folder for running the import
                    src = os.path.join(xml_path, xml_filename)
                    dest = os.path.join(self.IMPORT_FOLDER, "CDS")
                    dest = os.path.join(dest, xml_filename)
                    copyfile(src, dest)
                else:
                    print("There was a problem in unzipping that archive.")