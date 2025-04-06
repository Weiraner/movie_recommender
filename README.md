# Movie Recommender
This is a movie recommender with both frontend and backend. It's mainly based on ALS in SparkMlib
To achieve realtime recommendation, it only updates user_vec when user create new rating. Then it will update whole user/movie vector at certain time

# To Begin with
```shell
# frontend
cd frontend
npm install
npm run dev

# backend
# a virtual environment is recommended
# python 3.10.6 is used to develop this project
python3 backend/data/init_db.py
python3 backend/model/train_als.py
python3 backend/main.py
```