import sys
from classes.parser import Parser
import classes.globals as g


p = Parser()
p.parse_files()
p.parse_quota_balances()
