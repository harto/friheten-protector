import boto
from os import path

def upload_file(local_path):
    conn = boto.connect_s3()
    bucket = conn.get_bucket('sauron-uploads')
    key = bucket.new_key(path.basename(local_path))
    with open(local_path) as f:
        key.set_contents_from_file(f)
    print "uploaded %s" % key
