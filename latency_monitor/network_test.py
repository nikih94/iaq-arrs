from pprint import pprint
import time
import json
import subprocess
import os


class NetworkTest:
    devices = []
    server = ()

    """
    The watchdog timer to kill latency tests that take to-much time
    """

    TIMEOUT = 10

    """
    THE LOGGER logas events on file, stdout and central influxdb
    """
    logger = None

    def __init__(self, server_ip, timeout):
        self.server = (server_ip, 'no-mac', 'ir-server')
        self.TIMEOUT = timeout
        pass

    """
    Measure latency in microseconds using netperf
    """

    def measure_latency(self):
        self.devices.append(self.server)
        result = []
        for dev in self.devices:
            try:
                proc = subprocess.Popen(
                    ['netperf -H '+dev[0]+'  -l -10000 -TCP_RR  -b 1 -v 2 -- -O mean_latency'], stdout=subprocess.PIPE, shell=True)
                outs, errs = proc.communicate(timeout=self.TIMEOUT)
                lines = outs.splitlines()
                latency = lines[6].rstrip().decode('utf-8')
                print('Device: ', dev[0], ' latency in usec: ', latency)
                result.append([dev[1], dev[2], latency])
            except subprocess.TimeoutExpired as t:
                self.logger.error("Timeout error when measuring latency to device mac:" + str(
                    dev[1]) + " hostname:" + str(dev[2]) + " watchdog: " + str(self.TIMEOUT))
        return result

    """
    Load list of addresses to ping from the bonjour protocol
    """

    def load_devices(self):
        self.devices = []
        try:
            proc = subprocess.Popen(
                ['avahi-browse -a -r -t -l -p  2> /dev/null | grep "^=;wl.[^;]*;IPv4;network-latency" '], stdout=subprocess.PIPE, shell=True)
            outs, errs = proc.communicate(timeout=self.TIMEOUT)
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
            self.logger.error(
                "Timeout error when reading avahi device list, watchdog: " + str(self.TIMEOUT))


if __name__ == "__main__":
    print('Started')
    NT = NetworkTest('iaq.innorenew.eu', 10)
    NT.load_devices()
    NT.measure_latency()
