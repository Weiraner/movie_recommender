from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.rate import router as rate_router
from fastapi.middleware.cors import CORSMiddleware
from api.recommend import router as recommend_router

app = FastAPI()

# 包含rate和recommend的路由
app.include_router(rate_router)
app.include_router(recommend_router)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 也可以写 ["*"] 方便开发调试
    allow_credentials=True,
    allow_methods=["*"],  # 确保包括 "POST"
    allow_headers=["*"],  # 允许 Content-Type 等请求头
)

# 注册你的推荐路由
app.include_router(recommend_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)