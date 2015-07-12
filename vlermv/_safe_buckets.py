from time import sleep
import threading, queue

from boto import connect_s3

def create_buckets(create_bucket, log, state):
    while True:
        bucketname = log.get()
        state[bucketname] = create_bucket(bucketname)

class SafeBuckets:
    '''
    Thread-safely create a bucket.
    '''
    def __init__(self, create_bucket = connect_s3().create_bucket):
        self.log = queue.Queue()
        self.state = {}
        creator = threading.Thread(target = create_buckets,
           args = (create_bucket, self.log, self.state), daemon = True)
        creator.start()

    def __getitem__(self, k):
        self.log.put(k)
        while k not in self.state:
            sleep(0)
