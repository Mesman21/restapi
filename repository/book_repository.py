from bson import ObjectId
from database import books_collection

class BookRepository:
    @staticmethod
    def get_all(query, sort_by=None):
        cursor = books_collection.find(query)
        if sort_by in ['title', 'year']:
            cursor = cursor.sort(sort_by, 1)
        books = []
        for book in cursor:
            book['_id'] = str(book['_id'])
            books.append(book)
        return books

    @staticmethod
    def get_by_id(book_id):
        book = books_collection.find_one({"_id": ObjectId(book_id)})
        if book:
            book['_id'] = str(book['_id'])
        return book

    @staticmethod
    def create(data):
        result = books_collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return data

    @staticmethod
    def delete(book_id):
        books_collection.delete_one({"_id": ObjectId(book_id)})