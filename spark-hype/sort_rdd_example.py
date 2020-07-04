# import pyspark class Row from module sql
from pyspark.sql.types import *
from pyspark.sql import *

spark = SparkSession.builder \
                    .master("local") \
                    .getOrCreate()


sc = spark.sparkContext

lines = sc.textFile("people.txt")

parts = lines.map(lambda l: l.split(","))
people = parts.map(lambda p: Row(name=p[0],age=int(p[1])))
peopledf = spark.createDataFrame(people)
people = parts.map(lambda p: Row(name=p[0], age=int(p[1].strip())))
schemaString = "name age"
fields = [StructField(field_name, StringType(), True) for
field_name in schemaString.split()]
schema = StructType(fields)
spark.createDataFrame(people, schema).sort("age").show()
