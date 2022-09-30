import os
from classes.downloader import Downloader
from classes.parser import Parser

# Download files
d = Downloader()
d.download_files()

# Parse the files
p = Parser()
p.parse_files()

# Go to the dest folder
foldername = p.xlsx_path

print("Finding requested folder / files ...")
os.system('open "%s"' % p.xlsx_path)
