from async_timeout import timeout
import netperf_wrapper
from pprint import pprint
import time
import json
import subprocess
import psutil
import os


class NetworkTest:
    devices = []
    server = ()

    def __init__(self, server_ip):
        self.server = (server_ip, 'no-mac', 'ir-server')
        pass

    """
    Measure latency in microseconds using netperf
    """

    def measure_latency_to(self):
        self.devices.append(self.server)
        pprint(self.devices)
        for dev in self.devices:
            try:
                proc = subprocess.Popen(
                    ['netperf  -H '+dev[0]+'  -l 3 -TCP_RR  -b 1 -v 2 -- -O mean_latency'], stdout=subprocess.PIPE, shell=True)
                outs, errs = proc.communicate(timeout=10)
                lines = outs.splitlines()
                if len(lines) == 7:
                    latency = lines[6].rstrip().decode('utf-8')
                    print('Device: ', dev[0], ' latency in usec: ', latency)
            except subprocess.TimeoutExpired as t:
                print('Timed out')

    """
    Load list of addresses to ping from the bonjour protocol
    """

    def load_devices(self):
        try:
            proc = subprocess.Popen(
                ['avahi-browse -a -r -t -l -p  2> /dev/null | grep "^=;wl.[^;]*;IPv4;network-latency" '], stdout=subprocess.PIPE, shell=True)
            outs, errs = proc.communicate(timeout=10)
            lines = outs.splitlines()
            for line in lines:
                line = line.rstrip().decode('utf-8')
                ip = line.split(";")[7]
                mac = line.split(";")[9].strip('\"')
                name = line.split(";")[6]
                if name[len(name)-6:len(name)] == ".local":
                    name = name[0:len(name)-6]
                self.devices.append((ip, mac, name))
        except subprocess.TimeoutExpired as t:
            print('Timed out')


if __name__ == "__main__":
    print('Started')
    NT = NetworkTest('88.200.63.216')
    NT.load_devices()
    NT.measure_latency_to()
