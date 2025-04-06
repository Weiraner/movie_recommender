from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
import json
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.update_user_vec import update_user_vector, recommend

# from model.update_user_vector import update_user_vector, recommend

router = APIRouter()

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建数据库文件的绝对路径
data_dir = os.path.abspath(os.path.join(current_dir, '..', 'data'))
db_path = os.path.join(data_dir, 'recommend.db')

def get_conn():
    return sqlite3.connect(db_path)

class RatingRequest(BaseModel):
    user_id: int

@router.post("/recommend")
def get_recommendations(req: RatingRequest):
    conn = get_conn()
    cur = conn.cursor()

    # Load all item vectors and single user vector for recommendation
    cur.execute("SELECT movie_id, vector FROM item_vectors")
    all_item_vecs = {movie_id: np.array(json.loads(vec)) for movie_id, vec in cur.fetchall()}
    
    # Get user vector
    cur.execute("SELECT vector FROM user_vectors WHERE user_id = ?", (req.user_id,))
    row = cur.fetchone()
    
    if row is None:
        # 如果用户向量不存在，返回一个错误
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="User vector not found. Please rate some movies first."
        )
    
    user_vec = np.array(json.loads(row[0]))

    # Recommend
    # recommendations = recommend(user_vec, all_item_vecs)
    scores = {item_id: np.dot(user_vec, vec) for item_id, vec in all_item_vecs.items()}
    top_movie_ids = [i for i,_ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]]
    
    # get detailed movie info
    placeholders = ','.join(['?' for _ in top_movie_ids])
    cur.execute(f"""
        SELECT id, title, date, genres, rating 
        FROM movies 
        WHERE id IN ({placeholders})
    """, top_movie_ids)
    
    movies = cur.fetchall()
    recommendations = [
        {
            "id": movie[0],
            "title": movie[1],
            "date": movie[2],
            "genres": movie[3],
            "rating": movie[4]
        }
        for movie in movies
    ]
    
    conn.close()
    return {
        "top_k": recommendations
    }