import random

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--parallel_samples", default=100)
parser.add_argument("--num_tasks", default=4)
args = parser.parse_args()

print "args.parallel_samples ", args.parallel_samples
print "args.num_tasks ", args.num_tasks

# NUM_SAMPLES = 1000000
# NUM_SAMPLES = 100

from pyspark import SparkConf
from pyspark import SparkContext

conf = SparkConf()
conf.setMaster('yarn-client')
conf.setAppName('spark-yarn')
conf.set('spark.ui.proxyBase', '')
# conf.set('spark.ui.proxyBase', '/proxy/4040')

# sc = SparkContext(conf=conf)
sc = SparkContext("local", "pi")


def inside():
    x, y = random.random(), random.random()
    if x*x + y*y < 1:
        return 1.0
    else:
        return 0.0

def inside_loop(itr):
    if itr % 1000 == 0:
        print itr
    arr = [inside() for i in range(100000)]
    return sum(arr) / len(arr)

print "hi"
print inside_loop(1)

count = sc.parallelize(xrange(args.parallel_samples), args.num_tasks).map(inside_loop).sum()
print "Pi is roughly %0.15f" % (4.0 * count / args.parallel_samples)
