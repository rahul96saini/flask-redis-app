from flask import Flask, request
import redis
import os

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)


@app.route("/")
def home():
    count = redis_client.incr("visitor_count")

    return f"""
    <html>
        <head>
            <title>Flask Redis App</title>
        </head>
        <body>
            <h1>Welcome to My AWS Application!</h1>
            <h2>Visitor Count: {count}</h2>

            <form action="/visitor" method="POST">
                <input type="text" name="name" placeholder="Enter your name" required>
                <button type="submit">Submit</button>
            </form>
        </body>
    </html>
    """


@app.route("/visitor", methods=["POST"])
def visitor():
    name = request.form.get("name")

    redis_client.lpush("recent_visitors", name)
    redis_client.ltrim("recent_visitors", 0, 4)

    return f"""
    <h1>Hello, {name}!</h1>
    <p>Your name has been stored in Redis.</p>
    <a href="/">Go Back</a>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)