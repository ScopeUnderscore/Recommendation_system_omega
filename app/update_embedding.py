import numpy as np
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
try:
    # Check the connection status
    client.admin.command("ping")
    print("MongoDB connection successful!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

db = client["social_media"]
posts_collection = db["posts"]

# Initialize the Sentence-Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Function to calculate embedding from caption and tags
def calculate_embedding(caption, tags=None):
    # Combine caption and tags into a single string
    if tags:
        combined_text = f"{caption} {' '.join(tags)}"
    else:
        combined_text = caption

    logging.info(f"Calculating embedding for text: {combined_text[:30]}...")
    return model.encode(combined_text).tolist()


# Function to calculate engagement score based on likes, views, and comments
def calculate_engagement(likes, views, comments):
    likes_count = len(likes)
    views_count = len(views)
    comments_count = len(comments)

    # Simple engagement score: adjust as needed based on your criteria
    engagement_score = (
        (likes_count * 0.5) + (views_count * 0.3) + (comments_count * 0.2)
    )
    return engagement_score


# Function to update the embeddings and engagement score in the database
def update_post(post_id):
    post = posts_collection.find_one({"_id": post_id})

    if post:
        # Log the current post for debugging
        logging.info(f"Updating post with ID {post_id}. Caption: {post['caption']}")

        # Update embedding
        embedding = calculate_embedding(
            post["caption"],
            post.get("tags", None),  # Use tags if present
        )
        posts_collection.update_one(
            {"_id": post_id}, {"$set": {"embedding": embedding}}
        )
        logging.info(f"Updated embedding for post {post_id}.")

        # Update engagement score
        engagement_score = calculate_engagement(
            post["likes"], post["views"], post["comments"]
        )
        posts_collection.update_one(
            {"_id": post_id}, {"$set": {"engagementScore": engagement_score}}
        )
        logging.info(f"Updated engagement score for post {post_id}.")
    else:
        logging.warning(f"Post with ID {post_id} not found.")


# Main function to update embeddings and engagement scores for all posts
def update_all_posts():
    posts = posts_collection.find()

    for post in posts:
        update_post(post["_id"])


if __name__ == "__main__":
    update_all_posts()
