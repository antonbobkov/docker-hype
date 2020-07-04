import random
import argparse

from pyspark import SparkConf
from pyspark import SparkContext

conf = SparkConf()
conf.setMaster('yarn-client')
conf.setAppName('spark-yarn')
conf.set('spark.ui.proxyBase', '')

# sc = SparkContext(conf=conf)
sc = SparkContext("local", "pi")

text_file = sc.textFile("/home/anton/spark-stuff/word_count_in.txt")
counts = text_file.flatMap(lambda line: line.split(" ")) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)
counts = counts.repartition(10)
counts.saveAsTextFile("/home/anton/spark-stuff/word_count_out.txt")
