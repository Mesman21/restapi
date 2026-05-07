from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from api.endpoints import BookList, BookItem

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

api.add_resource(BookList, '/books')
api.add_resource(BookItem, '/books/<book_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)