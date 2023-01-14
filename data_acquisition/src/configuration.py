import configparser


class Configuration:

    config = None

    # data_aquisition
    measurement_delta = None
    sensor_lines = None
    iaq_bucket = None

    # [tags]
    sensor_id = None
    building = None

    # [local_db]
    local_db_host = None
    local_db_database = None
    local_db_username = None
    local_db_password = None

    # [influx2]
    url = None
    org = None
    token = None
    timeout = None
    verify_ssl = None
    log_bucket = None

    def __init__(self, path):
        self.config = configparser.ConfigParser()
        self.config.read(path)
        self.load_configuration()
        pass

    def load_configuration(self):
        self.measurement_delta = self.config['data_acquisition'].get(
            'measurement_delta')
        self.sensor_lines = self.config['data_acquisition'].get('sensor_lines')
        self.iaq_bucket = self.config['data_acquisition'].get('iaq_bucket')
        self.sensor_id = self.config['tags'].get('sensor_id')
        self.building = self.config['tags'].get('building')
        self.local_db_host = self.config['local_db'].get('local_db_host')
        self.local_db_database = self.config['local_db'].get(
            'local_db_database')
        self.local_db_username = self.config['local_db'].get(
            'local_db_username')
        self.local_db_password = self.config['local_db'].get(
            'local_db_password')
        self.url = self.config['influx2'].get('url')
        self.org = self.config['influx2'].get('org')
        self.token = self.config['influx2'].get('token')
        self.timeout = self.config['influx2'].get('timeout')
        self.verify_ssl = self.config['influx2'].get('verify_ssl')
        self.log_bucket = self.config['influx2'].get('log_bucket')
