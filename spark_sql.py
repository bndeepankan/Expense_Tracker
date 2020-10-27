from pyspark.sql import SparkSession
from db import mongoURI
import json

class sqlOperation():

    def __init__(self):
        self.obj = mongoURI()
        self.input_uri = self.obj.expense_uri
        self.output_uri = self.obj.expense_uri
        self.spark = SparkSession\
            .builder\
            .appName("SQL Operation")\
            .config("spark.mongodb.input.uri", self.input_uri)\
            .config("spark.mongodb.output.uri", self.output_uri)\
            .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:2.4.2")\
            .getOrCreate()

    def searchQuery(self, query, _id):
        """
        query: str query in the form of SQL
        """

        df = self.spark.read.format('com.mongodb.spark.sql.DefaultSource').load()
        df.createOrReplaceTempView("df")
        user_data = self.spark.sql("select * from df where user_id = %s" % _id)
        user_data.createOrReplaceTempView("tmp")
        result = self.spark.sql(query)
        result = result.toJSON().collect()
        output = []
        for val in result:
            output.append(json.loads(val))

        return output 
