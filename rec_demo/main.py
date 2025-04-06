from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

# Spark initialization
spark = SparkSession.builder \
    .appName("MovieLensALS") \
    .master("local[*]") \
    .getOrCreate()

# read rating data
data = spark.read.csv("../ml-100k/u.data", sep="\t", inferSchema=True)
data = data.withColumnRenamed("_c0", "userId") \
           .withColumnRenamed("_c1", "movieId") \
           .withColumnRenamed("_c2", "rating") \
           .withColumnRenamed("_c3", "timestamp")

# divide AB test set
(train, test) = data.randomSplit([0.8, 0.2], seed=42)

# Build ALS model
als = ALS(
    maxIter=10,
    regParam=0.1,
    userCol="userId",
    itemCol="movieId",
    ratingCol="rating",
    coldStartStrategy="drop"
)
model = als.fit(train)

# train ALS model
pred = model.transform(test)
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
rmse = evaluator.evaluate(pred)
print(f"RMSE: {rmse:.4f}")
print(model)

# recommend to user
from recommend import show_user_recommendations
show_user_recommendations(spark, model)

spark.stop()
