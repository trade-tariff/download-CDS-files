import os
from classes.downloader import Downloader
from classes.parser import Parser
import classes.globals as g

# Download files
d = Downloader()
d.download_files()

# Parse the files
p = Parser()
p.parse_files()
p.parse_quota_balances()

# Go to the dest folder
foldername = p.xlsx_path

print("Finding requested folder / files ...")
os.system('open "%s"' % p.xlsx_path)
