from pyspark.sql.types import *
from pyspark.sql import *

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input")
args = parser.parse_args()

spark = SparkSession.builder \
                    .master("local") \
                    .getOrCreate()

sc = spark.sparkContext

rows = sc.textFile(args.input) \
        .map(lambda p: Row(data=p))
df = spark.createDataFrame(rows) \
          .sort("data") \
          .rdd \
          .map(lambda p: p.data) \
          .saveAsTextFile(args.input + "_sorted")

