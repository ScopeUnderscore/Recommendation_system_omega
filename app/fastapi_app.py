from fastapi import FastAPI
from app.models import fetch_all_posts
from app.recommend import recommend_posts

app = FastAPI()


@app.post("/recommend")
async def recommend(embedding: list):
    all_posts = fetch_all_posts()
    recommendations = recommend_posts(embedding, all_posts)
    return [{"postId": rec[0]["_id"], "similarity": rec[1]} for rec in recommendations]
