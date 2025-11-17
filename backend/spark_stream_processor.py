import os
os.environ["HADOOP_HOME"] = "C:\\hadoop"
os.environ["PATH"] += os.pathsep + "C:\\hadoop\\bin"

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, count
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

# Step 1: Create a Spark Session
spark = SparkSession.builder \
    .appName("QuizEvaluationStreamProcessor") \
    .master("local[*]") \
    .config("spark.streaming.stopGracefullyOnShutdown", "true") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

# Step 2: Define the schema for Kafka messages
schema = StructType([
    StructField("student_id", StringType()),
    StructField("quiz_id", StringType()),
    StructField("score", IntegerType()),
    StructField("total", IntegerType()),
    StructField("accuracy", FloatType())
])

# Step 3: Read stream from Kafka topic
quiz_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "quiz_evaluations") \
    .option("startingOffsets", "latest") \
    .load()

# Step 4: Parse the Kafka message value (JSON)
quiz_data = quiz_df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), schema).alias("data")).select("data.*")

# Step 5: Compute live metrics
aggregated = quiz_data.groupBy("student_id").agg(
    count("quiz_id").alias("quizzes_taken"),
    avg("accuracy").alias("avg_accuracy"),
    avg("score").alias("avg_score")
)

# Step 6: Output results to console in real-time
query = aggregated.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
