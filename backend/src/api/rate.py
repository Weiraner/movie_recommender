from fastapi import APIRouter, Response, status
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
    movie_id: int
    rating: float

@router.post("/rate")
def rate_movie(req: RatingRequest):
    conn = get_conn()
    cur = conn.cursor()

    # Save new rating
    cur.execute("INSERT INTO ratings (user_id, movie_id, rating) VALUES (?, ?, ?)",
                (req.user_id, req.movie_id, req.rating))
    conn.commit()

    # Get user ratings
    cur.execute("SELECT movie_id, rating FROM ratings WHERE user_id = ?", (req.user_id,))
    user_ratings = cur.fetchall()

    # Load item vectors
    cur.execute("SELECT movie_id, vector FROM item_vectors WHERE movie_id IN (%s)" % 
                ",".join(["?"]*len(user_ratings)), [r[0] for r in user_ratings])
    item_vecs_raw = cur.fetchall()
    item_vecs = [np.array(json.loads(v)) for (_, v) in item_vecs_raw]
    ratings = [r[1] for r in user_ratings]

    # Update user vector
    user_vec = update_user_vector(item_vecs, ratings)
    cur.execute("REPLACE INTO user_vectors (user_id, vector) VALUES (?, ?)",
                (req.user_id, json.dumps(user_vec.tolist())))
    conn.commit()

    conn.close()
    return Response(status_code=status.HTTP_204_NO_CONTENT)