from repository.book_repository import BookRepository
from schemas.book import BookSchema

book_schema = BookSchema()

class BookService:
    @staticmethod
    def get_books(status, author, sort_by):
        query = {}
        if status:
            query['status'] = status
        if author:
            query['author'] = author
        return BookRepository.get_all(query, sort_by)

    @staticmethod
    def get_book(book_id):
        return BookRepository.get_by_id(book_id)

    @staticmethod
    def create_book(data):
        errors = book_schema.validate(data)
        if errors:
            return None, errors
        return BookRepository.create(data), None

    @staticmethod
    def delete_book(book_id):
        BookRepository.delete(book_id)