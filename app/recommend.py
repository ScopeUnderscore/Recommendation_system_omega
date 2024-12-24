# import numpy as np


# def recommend_posts(target_embedding, all_posts, top_n=5):
#     recommendations = []
#     for post in all_posts:
#         # Cosine similarity
#         similarity = np.dot(target_embedding, post["embedding"]) / (
#             np.linalg.norm(target_embedding) * np.linalg.norm(post["embedding"])
#         )
#         recommendations.append((post, similarity))

#     # Sort by similarity
#     recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
#     return recommendations[:top_n]


###############################################################
from sentence_transformers import SentenceTransformer
import numpy as np
from pymongo import MongoClient


def recommend_posts(target_embedding, all_posts, top_n=5):
    recommendations = []
    for post in all_posts:
        # Cosine similarity
        similarity = np.dot(target_embedding, post["embedding"]) / (
            np.linalg.norm(target_embedding) * np.linalg.norm(post["embedding"])
        )
        recommendations.append((post, similarity))

    # Sort by similarity
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
    return recommendations[:top_n]


if __name__ == "__main__":
    # Initialize the embedding model (ensure it's the same model used for the posts)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Example text to generate target embedding
    target_text = " pizza "
    target_embedding = model.encode(
        target_text
    ).tolist()  # This will have 384 dimensions

    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["social_media"]
    posts_collection = db["posts"]

    # Fetch posts from the database
    all_posts = list(
        posts_collection.find({}, {"_id": 1, "embedding": 1, "caption": 1})
    )

    # Ensure embeddings are lists (if stored as arrays in the database)
    for post in all_posts:
        post["embedding"] = list(post["embedding"])

    # Get top recommendations
    recommendations = recommend_posts(target_embedding, all_posts, top_n=3)

    # Print recommendations
    print("Top Recommendations:")
    for post, similarity in recommendations:
        print(
            f"Post ID: {post['_id']}, Caption: {post['caption']}, Similarity: {similarity:.4f}"
        )
