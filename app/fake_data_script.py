from pymongo import MongoClient
from faker import Faker
import random
import os
from datetime import datetime
import ollama  # LLaMA integration

# Initialize Faker instance
fake = Faker()

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["social_media"]
posts_collection = db["posts"]

# # Create a directory for storing generated images (even though we won't use it now)
# output_dir = "public/storage/images"
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)


# Function to generate realistic captions using LLaMA
def generate_realistic_caption():
    # Use LLaMA model for realistic captions
    response = ollama.chat(
        model="llama2",
        messages=[
            {
                "role": "user",
                "content": "Write a creative, engaging, and contextually appropriate caption with in 20 words",
            }
        ],
    )
    if response and response.message and response.message.content:
        captionz = response.message.content.strip()
        # print(response.message.content.strip())
        # Check and remove the unwanted prefix
        prefix = "here is a possible caption for an Instagram post in under 15 words:"
        if captionz.startswith(prefix):
            captionz = captionz[len(prefix) :].strip()
        else:
            # print("Unexpected response format:", response)
            captionz = response.message.content.strip()  # Fallback in case of errors

        return captionz  # Extract and return the caption
    else:
        print("Unexpected response format:", response)
        return "Default caption"  # Provide a fallback caption in case of errors


# Function to generate realistic tags that are more realistic
# def generate_realistic_tags():
#     # You can use common social media hashtags or generate some meaningful words
#     common_hashtags = [
#         "#love",
#         "#life",
#         "#instagood",
#         "#fun",
#         "#photography",
#         "#happy",
#         "#fashion",
#     ]
#     return random.sample(
#         common_hashtags, random.randint(1, 5)
#     )  # Randomly select 1 to 5 tags
def generate_realistic_tags(caption):
    """
    Generates hashtags dynamically using LLaMA2 based on the provided caption.

    Args:
        caption (str): The caption for which to generate relevant hashtags.

    Returns:
        list: A list of generated hashtags.
    """
    try:
        # Generate hashtags using LLaMA2
        response = ollama.chat(
            model="llama2",
            messages=[
                {
                    "role": "user",
                    "content": f'Generate a list of relevant hashtags for the following caption: "{caption}"',
                }
            ],
        )

        # Extract the hashtags from the response
        if response and response.message and response.message.content:
            # Split hashtags into a list, assuming they are comma-separated or newline-separated
            hashtags = response.message.content.strip().split()
            # Keep only valid hashtags that start with '#'
            hashtags = [tag for tag in hashtags if tag.startswith("#")]
        else:
            print("Unexpected response format:", response)
            hashtags = ["#default"]  # Fallback in case of errors

    except Exception as e:
        print(f"Error generating hashtags: {e}")
        hashtags = ["#default"]  # Fallback in case of exceptions

    return random.sample(hashtags, min(len(hashtags), random.randint(1, 5)))


# Function to generate realistic comments using LLaMA
def generate_realistic_comments():
    num_comments = random.randint(1, 5)  # Number of comments to generate
    comments = []

    for _ in range(num_comments):
        # Generate a comment using LLaMA
        response = ollama.chat(
            model="llama2",
            messages=[
                {
                    "role": "user",
                    "content": "Generate a realistic social media comment under 15 words.",
                }
            ],
        )

        # Extract the comment from the response
        if response and response.message and response.message.content:
            comment_text = response.message.content.strip()  # Extract the comment text

            # Check and remove the unwanted prefix
            prefix = "Sure, here's a realistic social media comment:"
            if comment_text.startswith(prefix):
                comment_text = comment_text[len(prefix) :].strip()
        else:
            # print("Unexpected response format:", response)
            comment_text = "Default comment"  # Fallback in case of errors

        # Construct the comment structure
        comment = {"userId": f"user{random.randint(1, 1000)}", "text": comment_text}
        comments.append(comment)

    return comments


# Function to generate a dummy post with realistic data
def generate_dummy_post(post_id):
    # Generate random post details
    user_id = f"user{random.randint(1, 1000)}"

    # Generate a valid filename with a random image extension (we won't create actual images)
    file_extension = random.choice(["jpg", "png", "gif"])
    filename = f"image_{post_id}_{random.randint(1, 1000)}.{file_extension}"

    # Generate more realistic caption, tags, and comments using LLaMA
    caption = generate_realistic_caption()
    upload_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    likes = [f"user{random.randint(1, 1000)}" for _ in range(random.randint(1, 10))]
    comments = generate_realistic_comments()
    post_saved = [f"user{random.randint(1, 1000)}" for _ in range(random.randint(1, 5))]
    views = [f"user{random.randint(1, 1000)}" for _ in range(random.randint(1, 10))]
    tags = generate_realistic_tags(caption)

    # Return the post data (no image will be generated)
    return {
        "_id": f"post_{post_id:03d}",
        "userId": user_id,
        "filename": filename,
        "caption": caption,
        "uploadDate": upload_date,
        "likes": likes,
        "comments": comments,
        "postSaved": post_saved,
        "views": views,
        "tags": tags,
        "image": "hui.jpg",  # Path to the image (just filename)
    }


# Insert 10 dummy posts into MongoDB
for i in range(1, 11):
    post = generate_dummy_post(i)
    # Insert the post document into the MongoDB collection
    posts_collection.insert_one(post)
    print(f"Inserted post {post['_id']} with image filename {post['image']}")
