from flask import Flask, jsonify, request

app = Flask(__name__)

reviews = [
    {"book_id": 1, "rating": 5, "comment": "Amazing classic!"},
    {"book_id": 2, "rating": 4, "comment": "Very detailed methodologies."}
]

@app.route('/reviews', methods=['GET'])
def get_reviews():
    book_id = request.args.get('book_id', type=int)
    if book_id:
        return jsonify([r for r in reviews if r['book_id'] == book_id])
    return jsonify(reviews)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)