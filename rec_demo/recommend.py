from pyspark.sql.functions import explode
from utils import load_movie_titles

def show_user_recommendations(spark, model, top_n=5):
    print("\n推荐示例：")
    recs = model.recommendForAllUsers(top_n)
    movie_titles = load_movie_titles("../ml-100k/u.item")

    # 展平推荐结果并展示电影名
    recs = recs.selectExpr("userId", "explode(recommendations) as rec") \
               .selectExpr("userId", "rec.movieId as movieId", "rec.rating as score")

    recs = recs.toPandas()
    for uid in recs['userId'].unique()[:3]:  # 只展示前3个用户
        print(f"\n用户 {uid} 推荐电影：")
        user_recs = recs[recs['userId'] == uid].sort_values(by="score", ascending=False)
        for _, row in user_recs.iterrows():
            movie_name = movie_titles.get(row['movieId'], "未知")
            print(f"  - {movie_name} (Score: {row['score']:.2f})")
