import functools


class QueueItem:

    priority = None

    entry_counter = None

    value = None

    def __init__(self, value, entry_counter):
        self.value = value
        self.entry_counter = entry_counter

    def __lt__(self, other):
        return (self.priority, self.entry_counter) < (other.priority, other.entry_counter)

    def __eq__(self, other):
        return (self.priority, self.entry_counter) == (other.priority, other.entry_counter)


class MainItem(QueueItem):

    def __init__(self, value, entry_counter):
        super().__init__(value, entry_counter)
        self.priority = 1


class CriticalError(QueueItem):

    def __init__(self, value, entry_counter):
        super().__init__(value, entry_counter)
        self.priority = 1


class SensorReadError(QueueItem):

    def __init__(self, value, entry_counter):
        super().__init__(value, entry_counter)
        self.priority = 6


class DataItem(QueueItem):

    def __init__(self, value, entry_counter):
        super().__init__(value, entry_counter)
        self.priority = 3
