import os
import classes.globals as g
from classes.parser import Parser

p = Parser()
foldername = p.xml_path

# systems = {
#     'nt': os.startfile,
#     'posix': lambda foldername: os.system('xdg-open "%s"' % foldername)
#     'os2': lambda foldername: os.system('open "%s"' % foldername)
#      }

# systems.get(os.name, os.startfile)(foldername)
print("Finding requested folder / files ...")
os.system('open "%s"' % foldername)
