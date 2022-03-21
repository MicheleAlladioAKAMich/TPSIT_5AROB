import flask
from flask import jsonify


app = flask.Flask(__name__)
app.config["DEBUG"] = True

books = [{'id':0, 'title':'Il nome della rosa', 'author':'Umberto Eco', 'year_published':1980},
        {'id':1, 'title':'Libro 2', 'author':'Umberto Eco', 'year_published':1965},
        {'id':2, 'title':'Libro 3', 'author':'Michele Alladio', 'year_published':1289}]

@app.route('/', methods=['GET'])
def home():
    return "<h1>Biblioteca online</h1><p>Prototipo di web API.</p>"

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

app.run(debug=True)