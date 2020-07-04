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

# sc = SparkContext(conf=conf)
sc = SparkContext("local", "pi")

has_seed = False

def reset_seed():
    global has_seed
    print "Resetting seed"
    random.seed()
    has_seed = True

def generate(itr):
    global has_seed
    if has_seed == False:
        reset_seed()
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(19))

print "generating", generate(1)
print "generating", generate(2)

has_seed = False
count = sc.parallelize(xrange(NUM_LINES), int(args.num_shards)) \
          .map(generate) \
          .saveAsTextFile(args.output)

# OUTDIR=/home/anton/spark-stuff/generate_out_test; rm -r $OUTDIR; spark-submit generate.py --output="$OUTDIR"
# OUTDIR=/home/anton/spark-stuff/generate_out_1MB_100_shards; rm -r $OUTDIR; spark-submit generate.py --output="$OUTDIR" --size_mb=1 --num_shards=100
# OUTDIR=/home/anton/spark-stuff/generate_out_1GB_1000_shards; rm -r $OUTDIR; spark-submit generate.py --output="$OUTDIR" --size_mb=1000 --num_shards=1000
