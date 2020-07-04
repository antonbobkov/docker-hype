import random
import string
import argparse

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--size_mb", default=.001)
parser.add_argument("--num_shards", default=10)
parser.add_argument("--output")
args = parser.parse_args()

NUM_LINES = int(float(args.size_mb) * 1000000 / 20)

print "args.size_mb ", args.size_mb
print "NUM_LINES ", NUM_LINES
print "args.num_shards ", int(args.num_shards)
print "args.output ", args.output


from pyspark import SparkConf
from pyspark import SparkContext

conf = SparkConf()
conf.setMaster('yarn-client')
conf.setAppName('spark-yarn')
conf.set('spark.ui.proxyBase', '')

sc = SparkContext(conf=conf)
# sc = SparkContext("local", "pi")

def generate(itr):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(19))

print generate(1)

count = sc.parallelize(xrange(NUM_LINES), int(args.num_shards)) \
          .map(generate) \
          .saveAsTextFile(args.output)

# OUTDIR=/user/pi/spark-stuff/generate_out_test; spark-submit generate_yarn.py --output="$OUTDIR"
# OUTDIR=/user/pi/spark-stuff/generate_out_1MB_100_shards; spark-submit generate_yarn.py --output="$OUTDIR" --size_mb=1 --num_shards=100
# OUTDIR=/user/pi/spark-stuff/generate_out_1GB_1000_shards; spark-submit generate_yarn.py --output="$OUTDIR" --size_mb=1000 --num_shards=1000
