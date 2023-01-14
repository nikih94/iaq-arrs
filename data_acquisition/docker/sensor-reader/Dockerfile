#download the base image
FROM python:3.8-alpine3.15

# LABEL about the custom image
LABEL maintainer="niki.hrovatin@famnit.upr.si"
LABEL version="1.0.0"
LABEL description="Custom Docker image for DAQ-monitoring"

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

RUN apk add --no-cache git 

RUN set -ex && \
    apk add --no-cache gcc musl-dev

RUN pip3 install minimalmodbus && pip3 install mysql-connector-python==8.0.29 && pip3 install 'influxdb-client[ciso]' && pip3 install pyrsistent && pip install retry2

#RUN git clone https://gitlab.com/nikih94/arrs_or

#RUN cd arrs_or &&\
#    git pull 

#set entrypoint, not python but shell
CMD ["/bin/sh"]