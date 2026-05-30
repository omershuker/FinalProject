from flask import Flask, render_template
import os, requests

app = Flask(__name__)

BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL", "http://book-service:5001")
REVIEW_SERVICE_URL = os.getenv("REVIEW_SERVICE_URL", "http://review-service:5002")

@app.route('/')
def index():
    books = []
    try:
        books = requests.get(f"{BOOK_SERVICE_URL}/books", timeout=2).json()
        for b in books:
            b['reviews'] = requests.get(f"{REVIEW_SERVICE_URL}/reviews?book_id={b['id']}", timeout=2).json()
    except Exception as e:
        books = [{"id": 0, "title": f"Connection Error: {str(e)}", "author": "None", "reviews": []}]
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)