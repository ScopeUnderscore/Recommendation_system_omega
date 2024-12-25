from flask import Flask, jsonify, request
from app.models import fetch_all_posts
from app.recommend import recommend_posts

app = Flask(__name__)


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        # Validate input
        data = request.json
        print(f"request data:{data}")
        if not data or "embedding" not in data:
            return jsonify({"error": "Missing 'embedding' in request body"}), 400

        target_embedding = data["embedding"]
        print(f"target_embedding:{target_embedding}")

        # Fetch posts and calculate recommendations
        all_posts = fetch_all_posts()
        recommendations = recommend_posts(target_embedding, all_posts)
        print(f"recommendations:{recommendations}")

        # Format and return the response
        # return jsonify(
        #     [{"postId": rec[0]["_id"], "similarity": rec[1]} for rec in recommendations]
        response = [
            {"postId": rec["_id"], "similarity": rec["engagementScore"]}
            for rec in recommendations
        ]
        print(f"Formatted response: {response}")  # Debugging line
        return jsonify(response)

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
