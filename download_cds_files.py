import sys
from classes.downloader import Downloader
from classes.parser import Parser
import classes.globals as g

if len(sys.argv) > 1:
    arg = sys.argv[1]
    if "d" in arg:
        d = Downloader()
        d.download_files()

    if "p" in arg:
        p = Parser()
        p.parse_files()
