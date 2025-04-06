@app.post("/rate")
def rate_movie(user_id: int, movie_id: int, rating: float):
    # 1. 写入评分记录（MySQL / Parquet / Kafka / CSV）
    append_rating(user_id, movie_id, rating)

    # 2. 从 Redis 取出 item vectors
    rated_items, item_vectors = get_item_vectors([movie_id])

    # 3. 用 ridge regression 更新 user_vector
    u_i = update_user_vector(item_vectors, [rating])

    # 4. 存入 Redis
    redis.set(f"user:{user_id}", json.dumps(u_i.tolist()))

    # 5. 实时推荐：与所有 item 向量做 dot product
    scores = recommend(u_i, all_item_vectors)

    return top_k(scores)
