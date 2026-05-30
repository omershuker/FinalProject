from flask import Flask, jsonify

app = Flask(__name__)

books = [
    {"id": 1, "title": "The Phoenix Project", "author": "Gene Kim"},
    {"id": 2, "title": "The DevOps Handbook", "author": "Gene Kim, Jez Humble"}
]

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    return jsonify(book) if book else (jsonify({"error": "Not found"}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)