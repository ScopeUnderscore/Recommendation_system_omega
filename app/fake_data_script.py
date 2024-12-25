from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime
import ollama  # LLaMA integration

# Initialize Faker instance
fake = Faker()

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["social_media_updated"]
posts_collection = db["posts"]
users_collection = db["users"]


# Function to generate realistic captions using LLaMA
def generate_realistic_caption():
    try:
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
            caption = response.message.content.strip()
            return caption
        else:
            return "Default caption"
    except Exception as e:
        print(f"Error generating caption: {e}")
        return "Default caption"


def generate_realistic_tags(caption):
    try:
        response = ollama.chat(
            model="llama2",
            messages=[
                {
                    "role": "user",
                    "content": f'Generate a list of relevant hashtags for the following caption: "{caption}"',
                }
            ],
        )
        if response and response.message and response.message.content:
            hashtags = response.message.content.strip().split()
            return [tag for tag in hashtags if tag.startswith("#")]
        else:
            return ["#default"]
    except Exception as e:
        print(f"Error generating hashtags: {e}")
        return ["#default"]


def generate_realistic_comments():
    comments = []
    try:
        num_comments = random.randint(1, 5)
        for _ in range(num_comments):
            response = ollama.chat(
                model="llama2",
                messages=[
                    {
                        "role": "user",
                        "content": "Generate a realistic social media comment under 15 words.",
                    }
                ],
            )
            if response and response.message and response.message.content:
                comment = response.message.content.strip()
                comments.append(
                    {"userId": f"user{random.randint(1, 1000)}", "text": comment}
                )
            else:
                comments.append(
                    {
                        "userId": f"user{random.randint(1, 1000)}",
                        "text": "Default comment",
                    }
                )
    except Exception as e:
        print(f"Error generating comments: {e}")
    return comments


# Function to generate dummy users
def generate_dummy_user(user_id):
    preferences = [fake.word() for _ in range(random.randint(1, 3))]
    followers = [f"user{random.randint(1, 1000)}" for _ in range(random.randint(1, 5))]
    followings = [f"user{random.randint(1, 1000)}" for _ in range(random.randint(1, 5))]
    saved_posts = [f"post_{random.randint(1, 50)}" for _ in range(random.randint(1, 5))]
    posts = [f"post_{random.randint(1, 50)}" for _ in range(random.randint(1, 5))]
    location = fake.city()

    return {
        "_id": f"user_{user_id:03d}",
        "name": fake.name(),
        "email": fake.email(),
        "preferences": preferences,
        "followers": followers,
        "followings": followings,
        "likedPosts": saved_posts,
        "savedPosts": saved_posts,
        "posts": posts,
        "location": location,
        "lastActive": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "createdAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


# Function to generate dummy posts
def generate_dummy_post(post_id):
    user_id = f"user_{random.randint(1, 50)}"
    caption = generate_realistic_caption()
    upload_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    likes = [f"user_{random.randint(1, 50)}" for _ in range(random.randint(1, 10))]
    comments = generate_realistic_comments()
    saved_by_users = [
        f"user_{random.randint(1, 50)}" for _ in range(random.randint(1, 5))
    ]
    tags = generate_realistic_tags(caption)

    return {
        "_id": f"post_{post_id:03d}",
        "userId": user_id,
        "filename": f"image_{post_id}.jpg",
        "caption": caption,
        "uploadDate": upload_date,
        "likes": likes,
        "comments": comments,
        "postSaved": saved_by_users,
        "tags": tags,
        "views": [
            f"user_{random.randint(1, 50)}" for _ in range(random.randint(1, 10))
        ],
    }


# Insert dummy users and posts into MongoDB
num_users = 50
num_posts = 100

# Insert users
for i in range(1, num_users + 1):
    user = generate_dummy_user(i)
    users_collection.insert_one(user)
    print(f"Inserted user {user['_id']}")

# Insert posts
for i in range(1, num_posts + 1):
    post = generate_dummy_post(i)
    posts_collection.insert_one(post)
    print(f"Inserted post {post['_id']}")
