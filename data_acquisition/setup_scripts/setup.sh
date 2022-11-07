#!/bin/bash


. ./configuration.sh


# Notify that the script must be run with sudo 
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

#check if the configuration is already updated

if [[ -f "../status/configured.tmp" ]]
then
    echo "System already configured."
    exit 0
fi
echo "Start system configuration"



####
#
#   GENERATE CONFIG FILE FOR DATA COLLECTION
#
####

cat > configuration/configuration.ini <<EOF
[data_acquisition]
measurement_delta=${MEASUREMENT_DELTA}
sensor_lines=${SENSOR_LINES}
iaq_bucket=${INFLUX_IAQ_BUCKET}


[tags]
sensor_id=${SENSOR_ID}
building=${BUILDING}


[local_db]
local_db_host=${LOCAL_DB_HOST}
local_db_database=${LOCAL_DB_DATABASE}
local_db_username=${LOCAL_DB_USERNAME}
local_db_password=${LOCAL_DB_PASS}


[influx2]
url=${INFLUX_URL}
org=${INFLUX_ORG}
token=${INFLUX_TOKEN}
timeout=${INFLUX_TIMEOUT}
verify_ssl=True
log_bucket=${INFLUX_LOG_BUCKET}
EOF


####
#
#   GENERATE .env FILE FOR LOVAL DB
#
####


cat > configuration/.env <<EOF
MARIADB_ROOT_PASSWORD=${LOCAL_DB_ROOT_PASSWORD}
MARIADB_DATABASE=${LOCAL_DB_DATABASE}
MARIADB_USER=${LOCAL_DB_USERNAME}
MARIADB_PASSWORD=${LOCAL_DB_PASS}
EOF



####
#
#   GENERATE UNIT FILE FOR DATA COLLECTION
#
####


cat > configuration/collect_data.service <<EOF
[Unit]
Description=Collect data from IAQ sensors and send to central DB
Requires=docker.service
PartOf=docker.service
After=network-online.target

[Service]
User=${USER_ON_RASPI}
Restart=always
Group=docker
RestartSec=180
WorkingDirectory=/home/${USER_ON_RASPI}/iaq-arrs/data_acquisition/docker/
# Shutdown container (if running) when unit is started
ExecStartPre=/usr/local/bin/docker-compose -f docker-compose.yml down
# Start container when unit is started
ExecStart=/usr/local/bin/docker-compose -f docker-compose.yml up
# Stop container when unit is stopped
ExecStartPost=/usr/local/bin/docker-compose -f docker-compose.yml down
# Rebuild container when unit is stopped
ExecStop=/usr/local/bin/docker-compose -f docker-compose.yml build

[Install]
WantedBy=multi-user.target
EOF



####
#
#   GENERATE UNIT FILE FOR REVERSE PROXY
#
####

cat > configuration/tunnel_to_ir.service <<EOF
[Unit]
Description=Setup a secure tunnel to IR
After=network-online.target

[Service]
User=${USER_ON_RASPI}
ExecStart=/usr/bin/ssh -NT -o StrictHostKeyChecking=no -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -R ${SERVER_PORT}:localhost:${RASPI_PORT} -p ${IR_SSH_PORT} ${SENSOR_USER}@${IR_SERVER}

# Restart every >2 seconds to avoid StartLimitInterval failure
RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target
EOF



####
#
#   GENERATE CONFIGURATION FOR TELEGRAF AGENT
#
####


cat > configuration/telegraf.conf <<EOF
# Configuration for telegraf agent
[agent]
  ## Default data collection interval for all inputs
  interval = "10s"
  ## Rounds collection interval to 'interval'
  ## ie, if interval="10s" then always collect on :00, :10, :20, etc.
  round_interval = true

  ## Telegraf will send metrics to outputs in batches of at most
  ## metric_batch_size metrics.
  ## This controls the size of writes that Telegraf sends to output plugins.
  metric_batch_size = 1000

  ## Maximum number of unwritten metrics per output.  Increasing this value
  ## allows for longer periods of output downtime without dropping metrics at the
  ## cost of higher maximum memory usage.
  metric_buffer_limit = 10000

  ## Collection jitter is used to jitter the collection by a random amount.
  ## Each plugin will sleep for a random time within jitter before collecting.
  ## This can be used to avoid many plugins querying things like sysfs at the
  ## same time, which can have a measurable effect on the system.
  collection_jitter = "0s"

  ## Default flushing interval for all outputs. Maximum flush_interval will be
  ## flush_interval + flush_jitter
  flush_interval = "10s"
  ## Jitter the flush interval by a random amount. This is primarily to avoid
  ## large write spikes for users running a large number of telegraf instances.
  ## ie, a jitter of 5s and interval 10s means flushes will happen every 10-15s
  flush_jitter = "0s"

  ## By default or when set to "0s", precision will be set to the same
  ## timestamp order as the collection interval, with the maximum being 1s.
  ##   ie, when interval = "10s", precision will be "1s"
  ##       when interval = "250ms", precision will be "1ms"
  ## Precision will NOT be used for service inputs. It is up to each individual
  ## service input to set the timestamp at the appropriate precision.
  ## Valid time units are "ns", "us" (or "µs"), "ms", "s".
  precision = ""

  ## Log at debug level.
  # debug = false
  ## Log only error level messages.
  # quiet = false

  ## Log target controls the destination for logs and can be one of "file",
  ## "stderr" or, on Windows, "eventlog".  When set to "file", the output file
  ## is determined by the "logfile" setting.
  # logtarget = "file"

  ## Name of the file to be logged to when using the "file" logtarget.  If set to
  ## the empty string then logs are written to stderr.
  # logfile = ""

  ## The logfile will be rotated after the time interval specified.  When set
  ## to 0 no time based rotation is performed.  Logs are rotated only when
  ## written to, if there is no log activity rotation may be delayed.
  # logfile_rotation_interval = "0d"

  ## The logfile will be rotated when it becomes larger than the specified
  ## size.  When set to 0 no size based rotation is performed.
  # logfile_rotation_max_size = "0MB"

  ## Maximum number of rotated archives to keep, any older logs are deleted.
  ## If set to -1, no archives are removed.
  # logfile_rotation_max_archives = 5

  ## Pick a timezone to use when logging or type 'local' for local time.
  ## Example: America/Chicago
  # log_with_timezone = ""

  ## Override default hostname, if empty use os.Hostname()
  hostname = "${SENSOR_HOSTNAME}"
  ## If set to true, do no set the "host" tag in the telegraf agent.
  omit_hostname = false
[[outputs.influxdb_v2]]
  ## The URLs of the InfluxDB cluster nodes.
  ##
  ## Multiple URLs can be specified for a single cluster, only ONE of the
  ## urls will be written to each interval.
  ##   ex: urls = ["https://us-west-2-1.aws.cloud2.influxdata.com"]
  urls = ["${INFLUX_URL}"]

  ## Token for authentication.
  token = "$TELEGRAF_TOKEN_PLACEHOLDER"

  ## Organization is the name of the organization you wish to write to; must exist.
  organization = "${INFLUX_ORG}"

  ## Destination bucket to write into.
  bucket = "${TELEGRAF_BUCKET}"

  ## The value of this tag will be used to determine the bucket.  If this
  ## tag is not set the 'bucket' option is used as the default.
  # bucket_tag = ""

  ## If true, the bucket tag will not be added to the metric.
  # exclude_bucket_tag = false

  ## Timeout for HTTP messages.
  # timeout = "5s"

  ## Additional HTTP headers
  # http_headers = {"X-Special-Header" = "Special-Value"}

  ## HTTP Proxy override, if unset values the standard proxy environment
  ## variables are consulted to determine which proxy, if any, should be used.
  # http_proxy = "http://corporate.proxy:3128"

  ## HTTP User-Agent
  # user_agent = "telegraf"

  ## Content-Encoding for write request body, can be set to "gzip" to
  ## compress body or "identity" to apply no encoding.
  # content_encoding = "gzip"

  ## Enable or disable uint support for writing uints influxdb 2.0.
  # influx_uint_support = false

  ## Optional TLS Config for use on HTTP connections.
  # tls_ca = "/etc/telegraf/ca.pem"
  # tls_cert = "/etc/telegraf/cert.pem"
  # tls_key = "/etc/telegraf/key.pem"
  ## Use TLS but skip chain & host verification
  insecure_skip_verify = false
[[inputs.cpu]]
  ## Whether to report per-cpu stats or not
  percpu = true
  ## Whether to report total system cpu stats or not
  totalcpu = true
  ## If true, collect raw CPU time metrics
  collect_cpu_time = false
  ## If true, compute and report the sum of all non-idle CPU states
  report_active = false
[[inputs.disk]]
  ## By default stats will be gathered for all mount points.
  ## Set mount_points will restrict the stats to only the specified mount points.
  # mount_points = ["/"]
  ## Ignore mount points by filesystem type.
  ignore_fs = ["tmpfs", "devtmpfs", "devfs", "iso9660", "overlay", "aufs", "squashfs"]
[[inputs.diskio]]
  ## By default, telegraf will gather stats for all devices including
  ## disk partitions.
  ## Setting devices will restrict the stats to the specified devices.
  # devices = ["sda", "sdb", "vd*"]
  ## Uncomment the following line if you need disk serial numbers.
  # skip_serial_number = false
  #
  ## On systems which support it, device metadata can be added in the form of
  ## tags.
  ## Currently only Linux is supported via udev properties. You can view
  ## available properties for a device by running:
  ## 'udevadm info -q property -n /dev/sda'
  ## Note: Most, but not all, udev properties can be accessed this way. Properties
  ## that are currently inaccessible include DEVTYPE, DEVNAME, and DEVPATH.
  # device_tags = ["ID_FS_TYPE", "ID_FS_USAGE"]
  #
  ## Using the same metadata source as device_tags, you can also customize the
  ## name of the device via templates.
  ## The 'name_templates' parameter is a list of templates to try and apply to
  ## the device. The template may contain variables in the form of '$PROPERTY' or
  ## '${PROPERTY}'. The first template which does not contain any variables not
  ## present for the device is used as the device name tag.
  ## The typical use case is for LVM volumes, to get the VG/LV name instead of
  ## the near-meaningless DM-0 name.
  # name_templates = ["$ID_FS_LABEL","$DM_VG_NAME/$DM_LV_NAME"]
[[inputs.mem]]
  # no configuration
[[inputs.net]]
  ## By default, telegraf gathers stats from any up interface (excluding loopback)
  ## Setting interfaces will tell it to gather these explicit interfaces,
  ## regardless of status.
  ##
  # interfaces = ["eth0"]
  ##
  ## On linux systems telegraf also collects protocol stats.
  ## Setting ignore_protocol_stats to true will skip reporting of protocol metrics.
  ##
  # ignore_protocol_stats = false
  ##
[[inputs.processes]]
  # no configuration
[[inputs.swap]]
  # no configuration
[[inputs.system]]
  ## Uncomment to remove deprecated metrics.
  # fielddrop = ["uptime_format"]
EOF



echo "End iaq data collection setup ended"
