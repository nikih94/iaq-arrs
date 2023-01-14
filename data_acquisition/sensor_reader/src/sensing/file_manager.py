import json
import datetime
import subprocess
import time
from json import JSONEncoder
import os


#json and files in python
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/

"""
Converts datetime to iso format

https://pynative.com/python-serialize-datetime-into-json/
"""

# subclass JSONEncoder


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


"""
Resize file to x lines using unix split

tail -n 30 raw_log.json > tmp && cat tmp > raw_log.json && rm tmp

"""


def truncate_file(name, lines):
    command = "tail -n "+str(lines)+" "+str(name) + \
        " > log/tmp_log && cat log/tmp_log > " + \
        str(name) + " && rm log/tmp_log"
    proc = subprocess.Popen(command, shell=True)
    proc.wait()
    directory = os.getcwd()
    # print(directory)
