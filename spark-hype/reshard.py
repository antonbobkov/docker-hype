import random
import argparse

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--num_shards", default=2)
args = parser.parse_args()

from pyspark import SparkConf
from pyspark import SparkContext

conf = SparkConf()
conf.setMaster('yarn-client')
conf.setAppName('spark-yarn')
conf.set('spark.ui.proxyBase', '')

# sc = SparkContext(conf=conf)
sc = SparkContext("local", "pi")

text_file = sc.textFile(args.input) \
            .repartition(int(args.num_shards)) \
            .saveAsTextFile(args.input + "_resharded")            
