from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType, StringType, StructType, TimestampType
import psycopg2

dbOptions = {"host": "postgres", 'port': 5432, "user": "Postgres", "password": "postgres"}
dbSchema = 'popular'
windowDuration = '5 minutes'
slidingDuration = '1 minute'

# Example Part 1
# Create a spark session
spark = SparkSession.builder \
    .appName("Structured Streaming").getOrCreate()

# Set log level
spark.sparkContext.setLogLevel('WARN')

# Example Part 2
# Read messages from Kafka
kafkaMessages = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers",
            "my-cluster-kafka-bootstrap:9092") \
    .option("subscribe", "tracking-data") \
    .option("startingOffsets", "earliest") \
    .load()

# Define schema of tracking data
trackingMessageSchema = StructType() \
    .add("mission", StringType()) \
    .add("timestamp", IntegerType())

# Example Part 3
# Convert value: binary -> JSON -> fields + parsed timestamp
trackingMessages = kafkaMessages.select(
    # Extract 'value' from Kafka message (i.e., the tracking data)
    from_json(
        column("value").cast("string"),
        trackingMessageSchema
    ).alias("json")
).select(
    # Convert Unix timestamp to TimestampType
    from_unixtime(column('json.timestamp'))
    .cast(TimestampType())
    .alias("parsed_timestamp"),

    # Select all JSON fields
    column("json.*")
) \
    .withColumnRenamed('json.mission', 'mission') \
    .withWatermark("parsed_timestamp", windowDuration)

# Example Part 4
# Compute most popular slides
popular = trackingMessages.groupBy(
    window(
        column("parsed_timestamp"),
        windowDuration,
        slidingDuration
    ),
    column("mission")
).count().withColumnRenamed('count', 'views')

# Example Part 5
# Start running the query; print running counts to the console
consoleDump = popular \
    .writeStream \
    .trigger(processingTime=slidingDuration) \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Example Part 6


def saveToDatabase(batchDataframe, batchId):
    # Define function to save a dataframe to mysql
    def save_to_db(iterator):
        # Connect to database and use schema 
        con = psycopg2.connect("host=postgres port=5432 dbname=kranichairline_db user=postgres password=postgres")
        cur = con.cursor()
        cur.execute("UPDATE flights SET price= price + (price * 10 / 100) ")
        cur.execute("select * from flights")
        data = cur.fetchall()
        cur.close()      
    # Perform batch UPSERTS per data partition
    batchDataframe.foreachPartition(save_to_db)

# Example Part 7


dbInsertStream = popular.writeStream \
    .trigger(processingTime=slidingDuration) \
    .outputMode("update") \
    .foreachBatch(saveToDatabase) \
    .start()

# Wait for termination
spark.streams.awaitAnyTermination()
