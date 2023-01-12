

class QueueItem:

    description = None

    message = None

    measurements = []

    def __init__(self, description, value):
        if description == "sensor_reading":
            self.description = description
            self.measurements = value
        else:
            self.description = description
            self.message = value
        pass
