#download the base image
FROM python:3.8-alpine3.15


# install avahi
# Avahi is for DNS-SD broadcasting on the local network; DBUS is how Avahi communicates with clients
RUN apk add make gcc libc-dev g++ linux-headers dbus avahi avahi-dev avahi-compat-libdns_sd avahi-tools

#RUN dbus-daemon --system && avahi-daemon --no-chroot --daemonize

# install netperf
ENV NETPERF_VERSION=2.7.0


# Install dependencies for netperf compile
RUN apk add --update --no-cache g++ make curl

# Download and install NetPerf
RUN curl -LO https://github.com/HewlettPackard/netperf/archive/netperf-${NETPERF_VERSION}.tar.gz \
    && tar -xzf netperf-${NETPERF_VERSION}.tar.gz \
    && mv netperf-netperf-${NETPERF_VERSION}/ netperf-${NETPERF_VERSION}
RUN cd netperf-${NETPERF_VERSION} && CFLAGS="-fcommon" ./configure --build=aarch64-unknown-linux-gnu \
    && make && make install

# install influxdb
RUN pip3 install 'influxdb-client[ciso]' && pip3 install pyrsistent && pip install rx 



#CMD ["/bin/sh"]

ENTRYPOINT ["sh","/arrs_or/latency_monitor/docker/entrypoint.sh"]

#CMD ["python3","-uc","/arrs_or/latency_monitor/hello.py"]