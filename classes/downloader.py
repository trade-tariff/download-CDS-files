import requests
import ssl
import sys
import os
from dotenv import load_dotenv
import zipfile
from shutil import copyfile
from classes.cds_file import CdsFile
import urllib.request

load_dotenv(".env")


class Downloader(object):
    def __init__(self):
        # Get credentials
        self.domain = os.getenv("GOVUK_API_DOMAIN", "")
        self.client_id = os.getenv("CLIENT_ID", "")
        self.client_secret = os.getenv("CLIENT_SECRET", "")
        self.import_folder = os.getenv("IMPORT_FOLDER", "")
        self._copy_to_import_folder = int(os.getenv("COPY_TO_IMPORT_FOLDER", "0"))
        self.cds_files = []

        self.get_access_token()
        self.create_ssl_unverified_context()

    def create_ssl_unverified_context(self):
        ssl._create_default_https_context = ssl._create_unverified_context

    def get_access_token(self):
        url = self.domain + "oauth/token"
        print(f"Fetching access token from: {url}")

        payload = "client_secret={}&client_id={}&grant_type=client_credentials".format(
            self.client_secret, self.client_id
        )
        headers = {"content-type": "application/x-www-form-urlencoded"}

        response = requests.request("POST", url, data=payload, headers=headers)
        if response.status_code != 200:
            print("Failed to retrieve an an access token")
            print(response.text)
            sys.exit(1)

        my_array = response.json()
        self.access_token = my_array["access_token"]

    def download_files(self):
        # Access data
        url = self.domain + "bulk-data-download/list/TARIFF-DAILY"
        headers = {
            "User-Agent": "Trade Tariff Backend",
            "Accept": "application/vnd.hmrc.1.0+json",
            "Authorization": "Bearer " + self.access_token,
        }
        response = requests.request("GET", url, headers=headers)

        files = response.json()
        for file_entry in files:
            cds_file = CdsFile()
            cds_file.filename = file_entry["filename"]
            cds_file.download_url = file_entry["downloadURL"]
            self.cds_files.append(cds_file)

        self.cds_files = sorted(self.cds_files, key=lambda x: x.filename, reverse=True)

        resource_path = os.path.join(os.getcwd(), "resources")
        zip_path = os.path.join(resource_path, "zip")
        xml_path = os.path.join(resource_path, "xml")

        self.make_folder(resource_path)
        self.make_folder(zip_path)
        self.make_folder(xml_path)

        # Download the data files
        for file_entry in self.cds_files:
            filename = file_entry.filename
            if "gzip" in filename:
                download_url = file_entry.download_url
                zip_filename = os.path.join(zip_path, filename)

                if os.path.isfile(zip_filename):
                    print(f"{filename} already exists, skipping...")
                else:
                    print(f"Downloading {filename}...")
                    try:
                        urllib.request.urlretrieve(download_url, zip_filename)
                        zfile = zipfile.ZipFile(zip_filename)
                        zfile.extractall(xml_path)
                        unzipped_files = zfile.filelist

                        if unzipped_files:
                            xml_filename = unzipped_files[0].filename

                            if self._copy_to_import_folder == 1:
                                # Copy to the import folder for running the import
                                src = os.path.join(xml_path, xml_filename)
                                dest = os.path.join(self.import_folder, "CDS")
                                dest = os.path.join(dest, xml_filename)
                                copyfile(src, dest)
                        else:
                            print("There was a problem in unzipping that archive.")
                    except Exception:
                        print(
                            "Failed attempt to download file from",
                            download_url,
                            file_entry.filename,
                        )

    def make_folder(self, folder_name):
        try:
            os.mkdir(folder_name)
        except Exception:
            pass

    def download_files_monthly(self):
        # Access data
        url = self.domain + "bulk-data-download/list/TARIFF-MONTHLY"
        headers = {
            "User-Agent": "Trade Tariff Backend",
            "Accept": "application/vnd.hmrc.1.0+json",
            "Authorization": "Bearer " + self.access_token,
        }
        response = requests.request("GET", url, headers=headers)

        files = response.json()
        for file_entry in files:
            cds_file = CdsFile()
            cds_file.filename = file_entry["filename"]
            cds_file.download_url = file_entry["downloadURL"]
            self.cds_files.append(cds_file)
            print(file_entry["filename"])

        self.cds_files = sorted(self.cds_files, key=lambda x: x.filename, reverse=True)

        for file_entry in self.cds_files:
            resource_path = os.path.join(os.getcwd(), "resources")
            zip_path = os.path.join(resource_path, "zip")
            xml_path = os.path.join(resource_path, "xml_monthly")
            filename = file_entry.filename
            if "gzip" in filename:
                download_url = file_entry.download_url
                zip_filename = os.path.join(zip_path, filename)

                if os.path.isfile(zip_filename):
                    print(f"{filename} already exists, skipping...")
                else:
                    print(f"Downloading {filename}...")
                    try:
                        urllib.request.urlretrieve(download_url, zip_filename)
                        zfile = zipfile.ZipFile(zip_filename)
                        zfile.extractall(xml_path)
                        unzipped_files = zfile.filelist
                        if unzipped_files:
                            xml_filename = unzipped_files[0].filename

                            # Copy to the import folder for running the import
                            src = os.path.join(xml_path, xml_filename)
                            dest = os.path.join(self.import_folder, "CDS")
                            dest = os.path.join(dest, xml_filename)
                            copyfile(src, dest)
                        else:
                            print("There was a problem in unzipping that archive.")
                    except Exception:
                        print(
                            "Failed attempt to download file from",
                            download_url,
                            file_entry.filename,
                        )

    def download_files_annual(self):
        # Access data
        url = self.domain + "bulk-data-download/list/TARIFF-ANNUAL"
        headers = {
            "User-Agent": "Trade Tariff Backend",
            "Accept": "application/vnd.hmrc.1.0+json",
            "Authorization": "Bearer " + self.access_token,
        }
        response = requests.request("GET", url, headers=headers)

        files = response.json()
        for file_entry in files:
            cds_file = CdsFile()
            cds_file.filename = file_entry["filename"]
            cds_file.download_url = file_entry["downloadURL"]
            self.cds_files.append(cds_file)
            print(file_entry["filename"])

        self.cds_files = sorted(self.cds_files, key=lambda x: x.filename, reverse=True)

        for file_entry in self.cds_files:
            resource_path = os.path.join(os.getcwd(), "resources")
            zip_path = os.path.join(resource_path, "zip")
            xml_path = os.path.join(resource_path, "xml_annual")
            filename = file_entry.filename
            if "gzip" in filename:
                download_url = file_entry.download_url
                zip_filename = os.path.join(zip_path, filename)

                if os.path.isfile(zip_filename):
                    print(f"{filename} already exists, skipping...")
                else:
                    print(f"Downloading {filename}...")
                    try:
                        urllib.request.urlretrieve(download_url, zip_filename)
                        zfile = zipfile.ZipFile(zip_filename)
                        zfile.extractall(xml_path)
                        unzipped_files = zfile.filelist
                        if unzipped_files:
                            xml_filename = unzipped_files[0].filename

                            # Copy to the import folder for running the import
                            src = os.path.join(xml_path, xml_filename)
                            dest = os.path.join(self.import_folder, "CDS")
                            dest = os.path.join(dest, xml_filename)
                            copyfile(src, dest)
                        else:
                            print("There was a problem in unzipping that archive.")
                    except Exception:
                        print(
                            "Failed attempt to download file from",
                            download_url,
                            file_entry.filename,
                        )
