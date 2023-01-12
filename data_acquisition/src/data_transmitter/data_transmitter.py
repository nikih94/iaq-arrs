from threading import Thread
from pqueue import Queue
from time import sleep
from random import randint


class DataTransmitter(Thread):

    q = None

    def __init__(self, q):
        super(DataTransmitter, self).__init__()
        self.q = q
        print("started consumer****************", flush=True)
        pass

    def run(self):
        while True:
            sleep(5000)
            try:
                while self.q.qsize() > 1:
                    value = self.q.get()
                    self.q.task_done()
                print("consumer: ", value, flush=True)
            except EOFError as err:
                print(err)
