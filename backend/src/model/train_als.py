from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
import json
import sqlite3
import os
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建数据库文件的绝对路径
data_dir = os.path.abspath(os.path.join(current_dir, '..', 'data'))
db_path = os.path.join(data_dir, 'recommend.db')

# 创建SparkSession
spark = SparkSession.builder.appName("ALS_Training").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")  # 只显示错误信息

# 从SQLite读取数据
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT user_id, movie_id, rating FROM ratings")
ratings_data = cursor.fetchall()
conn.close()

# 定义schema
schema = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("movie_id", IntegerType(), True),
    StructField("rating", FloatType(), True)
])

# 创建DataFrame
ratings = spark.createDataFrame(ratings_data, schema)

# 训练ALS模型
als = ALS(userCol="user_id", itemCol="movie_id", ratingCol="rating", coldStartStrategy="drop")
model = als.fit(ratings)

# 获取物品向量和用户向量
item_factors = model.itemFactors.collect()
user_factors = model.userFactors.collect()

# 保存向量到SQLite
conn = sqlite3.connect(db_path)
c = conn.cursor()

# 确保表存在
c.execute("""
    CREATE TABLE IF NOT EXISTS item_vectors (
        movie_id INTEGER PRIMARY KEY,
        vector TEXT
    )
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS user_vectors (
        user_id INTEGER PRIMARY KEY,
        vector TEXT
    )
""")

# 保存物品向量
for row in item_factors:
    vec = json.dumps(row["features"])
    c.execute("REPLACE INTO item_vectors (movie_id, vector) VALUES (?, ?)", (row["id"], vec))

# 保存用户向量
for row in user_factors:
    vec = json.dumps(row["features"])
    c.execute("REPLACE INTO user_vectors (user_id, vector) VALUES (?, ?)", (row["id"], vec))

conn.commit()
conn.close()

spark.stop()
