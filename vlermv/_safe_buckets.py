from time import sleep
import threading, queue

from boto import connect_s3
from boto.exception import S3CreateError

def create_buckets(create_bucket, get_all_buckets, log, state):
    while True:
        bucketname = log.get()
        try:
            state[bucketname] = create_bucket(bucketname)
        except S3CreateError as e:
            code, message, xml = e.args
            wrong_region = b'Your previous request to create the named bucket succeeded and you already own it.'
            if code == 409 and message == 'Conflict' and wrong_region in xml:
                state[bucketname] = next(b for b in get_all_buckets() if b.name == bucketname)
            else:
                raise

class SafeBuckets:
    '''
    Thread-safely create a bucket.
    '''
    def __init__(self, create_bucket = connect_s3().create_bucket,
                 get_all_buckets = connect_s3().get_all_buckets):
        self.log = queue.Queue()
        self.state = {}
        creator = threading.Thread(target = create_buckets,
           args = (create_bucket, get_all_buckets, self.log, self.state), daemon = True)
        creator.start()

    def __getitem__(self, k):
        self.log.put(k)
        while k not in self.state:
            sleep(0)
        return self.state[k]
