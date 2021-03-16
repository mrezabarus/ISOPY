from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/rezademopostgre'
app.debug = True
db = SQLAlchemy(app)
CORS(app, resources={r'/*':{'origins':'*'}})


class books(db.Model):
    __tablename__ = 'books'
    bookTitle = db.Column(db.String(100), primary_key=True)
    bookText = db.Column(db.String(), nullable=False)
    likes = db.Column(db.Integer(), nullable=False, default=0)

    def __init__(self,bookTitle, bookText, likes):
        self.bookTitle = bookTitle
        self.bookText = bookText
        self.likes = likes

@app.route('/test', methods=['GET'])
def test():
    return {
        'test':'Hello World'
    }

@app.route('/books', methods=['GET'])
def gbooks():
    allBooks = books.query.all()
    output = []
    for book in allBooks:
        currBook = {}
        currBook['bookTitle'] = book.bookTitle
        currBook['bookText'] = book.bookText
        currBook['likes'] = book.likes
        output.append(currBook)
    return jsonify(output)

@app.route('/books', methods=['POST'])
def pbooks():
    bookData = request.get_json()
    book = books(bookTitle=bookData['bookTitle'],bookText=bookData['bookText'],likes=bookData['likes'])
    db.session.add(book)
    db.session.commit()
    return jsonify(bookData)