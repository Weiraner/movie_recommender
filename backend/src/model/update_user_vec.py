import numpy as np

def update_user_vector(item_factors, ratings, reg=0.1):
    V = np.vstack(item_factors)
    R = np.array(ratings)
    A = V.T @ V + reg * np.eye(V.shape[1])
    b = V.T @ R
    return np.linalg.solve(A, b)

def recommend(user_vector, item_vectors, top_k=10):
    scores = {item_id: np.dot(user_vector, vec) for item_id, vec in item_vectors.items()}
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

