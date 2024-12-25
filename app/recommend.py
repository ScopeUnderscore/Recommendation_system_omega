import numpy as np


def recommend_posts(user_embedding, all_posts, top_n=5):
    """
    Recommends posts to the user based on their embedding.

    Args:
        user_embedding (list): The user's embedding vector.
        all_posts (list): A list of posts, where each post is a dictionary containing its embedding.
        top_n (int): The number of top posts to recommend.

    Returns:
        list: A list of the top N recommended posts for the user.
    """
    recommendations = []

    # Calculate cosine similarity between user's embedding and each post's embedding
    for post in all_posts:
        # Cosine similarity formula
        similarity = np.dot(user_embedding, post["embedding"]) / (
            np.linalg.norm(user_embedding) * np.linalg.norm(post["embedding"])
        )
        recommendations.append((post, similarity))

    # Sort the recommendations by similarity score in descending order
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)

    # Return top N recommended posts
    return [post for post, _ in recommendations[:top_n]]


# # Example usage
# if __name__ == "__main__":
#     # Example user embedding (could be fetched from the database for the logged-in user)
#     user_embedding = [0.67, 0.23, 0.56]  # Example values

#     # Example posts with their embeddings
#     all_posts = [
#         {
#             "_id": "post_001",
#             "embedding": [0.15, 0.22, 0.55],
#             "caption": "A beautiful sunset!",
#         },
#         {
#             "_id": "post_002",
#             "embedding": [0.11, 0.24, 0.60],
#             "caption": "Hiking in the mountains.",
#         },
#         {
#             "_id": "post_003",
#             "embedding": [0.10, 0.20, 0.50],
#             "caption": "Beach day vibes.",
#         },
#         {
#             "_id": "post_004",
#             "embedding": [0.14, 0.23, 0.54],
#             "caption": "Exploring the city.",
#         },
#         {
#             "_id": "post_005",
#             "embedding": [0.12, 0.22, 0.55],
#             "caption": "Camping under the stars.",
#         },
#     ]

#     # Recommend top 3 posts for the user
#     recommended_posts = recommend_posts(user_embedding, all_posts, top_n=3)

#     # Print the recommended posts
#     print("Recommended Posts:")
#     for post in recommended_posts:
#         print(f"Post ID: {post['_id']}, Caption: {post['caption']}")


#######################################################################################################################################################
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
# from sentence_transformers import SentenceTransformer
# import numpy as np
# from pymongo import MongoClient


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


# if __name__ == "__main__":
#     # Initialize the embedding model (ensure it's the same model used for the posts)
#     model = SentenceTransformer("all-MiniLM-L6-v2")

#     # Example text to generate target embedding
#     target_text = " sunset"
#     target_embedding = model.encode(
#         target_text
#     ).tolist()  # This will have 384 dimensions

#     # Connect to MongoDB
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client["social_media"]
#     posts_collection = db["posts"]

#     # Fetch posts from the database
#     all_posts = list(
#         posts_collection.find({}, {"_id": 1, "embedding": 1, "caption": 1})
#     )

#     # Ensure embeddings are lists (if stored as arrays in the database)
#     for post in all_posts:
#         post["embedding"] = list(post["embedding"])

#     # Get top recommendations
#     recommendations = recommend_posts(target_embedding, all_posts, top_n=3)

#     # Print recommendations
#     print("Top Recommendations:")
#     for post, similarity in recommendations:
#         print(
#             f"Post ID: {post['_id']}, Caption: {post['caption']}, Similarity: {similarity:.4f}"
#         )
