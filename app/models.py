from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["social_media_updated"]
posts = db["posts"]


def fetch_all_posts():
    return list(posts.find())
