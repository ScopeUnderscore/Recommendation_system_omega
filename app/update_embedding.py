import numpy as np
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
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

db = client["social_media_updated"]
posts_collection = db["posts"]
users_collection = db["users"]

# Load Sentence Transformer model
sentence_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)  # Replace with your preferred model


# PCA-based dimensionality reduction function
# def reduce_embedding(embedding, target_dim=3):
#     pca = PCA(n_components=target_dim)
#     reduced_embedding = pca.fit_transform(embedding.reshape(1, -1))
#     return reduced_embedding.flatten()
def reduce_embedding(embedding, target_dim=3):
    """
    Reduces the dimensionality of an embedding using PCA.

    Args:
        embedding (np.ndarray): The embedding to reduce.
        target_dim (int): The target dimensionality.

    Returns:
        np.ndarray: The reduced embedding.
    """
    if embedding.ndim == 1:
        embedding = embedding.reshape(1, -1)  # Ensure 2D input for PCA

    # Check if PCA is possible
    if embedding.shape[0] < target_dim:
        logging.warning(
            f"PCA target_dim={target_dim} is larger than n_samples={embedding.shape[0]}. Skipping PCA."
        )
        return embedding.flatten()[:target_dim]  # Truncate if necessary

    pca = PCA(n_components=target_dim)
    reduced_embedding = pca.fit_transform(embedding)
    return reduced_embedding.flatten()


# Function to calculate embedding from caption and tags
def calculate_embedding(caption, tags=None):
    if tags:
        combined_text = f"{caption} {' '.join(tags)}"
    else:
        combined_text = caption

    logging.info(f"Calculating embedding for text: {combined_text[:30]}...")
    embedding = sentence_model.encode(combined_text, convert_to_numpy=True)
    return embedding


# Function to calculate user embedding
def calculate_user_embedding(user_id):
    user = users_collection.find_one({"_id": user_id})

    if user:
        # Fetch user's posts and bio/interests
        user_posts = posts_collection.find({"user_id": user_id})
        user_texts = [post["caption"] for post in user_posts]

        # Include user bio and interests in embedding
        user_details = f"{user.get('bio', '')} {' '.join(user.get('interests', []) if user.get('interests') else [])}"
        combined_user_text = " ".join(user_texts) + " " + user_details

        logging.info(f"Calculating embedding for user ID {user_id}...")
        embedding = sentence_model.encode(combined_user_text, convert_to_numpy=True)

        # Reduce embedding dimensionality
        reduced_embedding = reduce_embedding(embedding, target_dim=3)
        return reduced_embedding
    else:
        logging.warning(f"User with ID {user_id} not found.")
        return None


# Function to update user embedding in the database
def update_user_embedding(user_id):
    user_embedding = calculate_user_embedding(user_id)

    if user_embedding is not None:
        users_collection.update_one(
            {"_id": user_id}, {"$set": {"user_embedding": user_embedding.tolist()}}
        )
        logging.info(f"Updated user embedding for user {user_id}.")
    else:
        logging.warning(f"User embedding for user {user_id} could not be calculated.")


# Function to calculate engagement score based on likes, views, and comments
def calculate_engagement(likes, views, comments):
    likes_count = len(likes)
    views_count = len(views)
    comments_count = len(comments)

    # Simple engagement score: adjust as needed based on your criteria
    engagement_score = (
        (likes_count * 0.4) + (views_count * 0.4) + (comments_count * 0.2)
    )
    return engagement_score


# Function to update post embeddings and engagement scores
def update_post(post_id):
    post = posts_collection.find_one({"_id": post_id})

    if post:
        logging.info(f"Updating post with ID {post_id}. Caption: {post['caption']}")

        # Calculate embedding
        embedding = calculate_embedding(
            post["caption"],
            post.get("tags", None),
        )

        # Reduce embedding dimensionality
        reduced_embedding = reduce_embedding(embedding, target_dim=3)

        # Update the database with reduced embedding
        posts_collection.update_one(
            {"_id": post_id}, {"$set": {"embedding": reduced_embedding.tolist()}}
        )
        logging.info(f"Updated reduced embedding for post {post_id}.")

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


# Main function to update all data
def update_all_data():
    # Update all posts
    posts = posts_collection.find()
    for post in posts:
        update_post(post["_id"])

    # Update all users
    users = users_collection.find()
    for user in users:
        update_user_embedding(user["_id"])


if __name__ == "__main__":
    update_all_data()
