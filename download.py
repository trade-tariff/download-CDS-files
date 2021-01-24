import sys
from classes.downloader import Downloader
from classes.parser import Parser
import classes.globals as g


d = Downloader()
d.download_files()
