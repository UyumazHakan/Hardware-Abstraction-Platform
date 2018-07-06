#!/usr/bin/python3
import sys
from tinydb import TinyDB, Query

args = sys.argv
db = TinyDB(args[1])
