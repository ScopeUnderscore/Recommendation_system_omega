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
db = client["social_media"]  # Use your database name
posts_collection = db["posts"]  # Use your collection name

# Create a directory for storing generated images (even though we won't use it now)
output_dir = "public/storage/images"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# Function to generate realistic captions using LLaMA
def generate_realistic_caption():
    # Use LLaMA model for realistic captions
    response = ollama.chat(
        model="llama2",
        messages=[
            {
                "role": "user",
                "content": "Generate captions usually seen in social media apps.",
            }
        ],
    )
    if response and response.message and response.message.content:
        print(response.message.content.strip())
        return response.message.content.strip()  # Extract and return the caption
    else:
        print("Unexpected response format:", response)
        return "Default caption"  # Provide a fallback caption in case of errors


# Function to generate realistic tags that are more realistic
def generate_realistic_tags():
    # You can use common social media hashtags or generate some meaningful words
    common_hashtags = [
        "#love",
        "#life",
        "#instagood",
        "#fun",
        "#photography",
        "#happy",
        "#fashion",
    ]
    return random.sample(
        common_hashtags, random.randint(1, 5)
    )  # Randomly select 1 to 5 tags


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
                    "content": "Generate a realistic social media comment.",
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
            print("Unexpected response format:", response)
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
    tags = generate_realistic_tags()

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
        "image": os.path.join(
            output_dir, filename
        ),  # Path to the image (just filename)
    }


# Insert 10 dummy posts into MongoDB
for i in range(1, 11):
    post = generate_dummy_post(i)
    # Insert the post document into the MongoDB collection
    posts_collection.insert_one(post)
    print(f"Inserted post {post['_id']} with image filename {post['image']}")
