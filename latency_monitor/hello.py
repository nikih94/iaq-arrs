#!/usr/bin/env python
import logging
import sched
import time
import struct
import influx_client
import configparser
import log_errors
import re
import uuid
import network_test


if __name__ == "__main__":
    print("Main started")
