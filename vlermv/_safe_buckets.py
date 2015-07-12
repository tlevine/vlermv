from time import sleep
import threading, queue

from boto import connect_s3

def create_buckets(log, state):
    while True:
        bucketname = log.get()
        state[bucketname] = connect_s3().create_bucket(bucketname)

class SafeBuckets:
    '''
    Thread-safely create a bucket.
    '''
    def __init__(self):
        self.log = queue.Queue()
        self.state = {}
        creator = threading.Thread(target = create_buckets,
                                   args = (self.log,), daemon = True)

    def __getitem__(self, k):
        self.log.put(k)
        while k not in self.state:
            sleep(0)
