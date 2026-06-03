from flask import request
from flask_restful import Resource
from flasgger import swag_from
from services.book_service import BookService

get_books_spec = {
    "tags": ["Books"],
    "parameters": [
        {
            "name": "status", 
            "in": "query", 
            "type": "string",
            "enum": ["наявні в бібліотеці", "видані комусь"],
            "description": "Фільтр за статусом"
        },
        {
            "name": "author", 
            "in": "query", 
            "type": "string",
            "description": "Фільтр за автором"
        },
        {
            "name": "sort_by", 
            "in": "query", 
            "type": "string",
            "enum": ["title", "year"],
            "description": "Поле для сортування"
        }
    ],
    "responses": {
        "200": {"description": "List of books"}
    }
}

post_book_spec = {
    "tags": ["Books"],
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "example": "Кобзар"},
                    "author": {"type": "string", "example": "Тарас Шевченко"},
                    "description": {"type": "string", "example": "Збірка поетичних творів"},
                    "status": {
                        "type": "string",
                        "enum": ["наявні в бібліотеці", "видані комусь"],
                        "example": "наявні в бібліотеці"
                    },
                    "year": {"type": "integer", "example": 1840}
                }
            }
        }
    ],
    "responses": {
        "201": {"description": "Book created"},
        "400": {"description": "Validation error"}
    }
}

get_book_spec = {
    "tags": ["Books"],
    "parameters": [
        {"name": "book_id", "in": "path", "type": "string", "required": True}
    ],
    "responses": {
        "200": {"description": "Book data"},
        "404": {"description": "Book not found"}
    }
}

delete_book_spec = {
    "tags": ["Books"],
    "parameters": [
        {"name": "book_id", "in": "path", "type": "string", "required": True}
    ],
    "responses": {
        "204": {"description": "Book deleted"}
    }
}

class BookList(Resource):
    @swag_from(get_books_spec)
    def get(self):
        status = request.args.get('status')
        author = request.args.get('author')
        sort_by = request.args.get('sort_by')
        
        books = BookService.get_books(status, author, sort_by)
        return books, 200

    @swag_from(post_book_spec)
    def post(self):
        data = request.get_json()
        book, errors = BookService.create_book(data)
        if errors:
            return {"errors": errors}, 400
        return book, 201

class BookItem(Resource):
    @swag_from(get_book_spec)
    def get(self, book_id):
        book = BookService.get_book(book_id)
        if not book:
            return {"message": "Not found"}, 404
        return book, 200

    @swag_from(delete_book_spec)
    def delete(self, book_id):
        BookService.delete_book(book_id)
        return '', 204