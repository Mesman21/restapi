from repository.book_repository import BookRepository

class BookService:
    @staticmethod
    async def get_books(status, author, sort_by):
        query = {}
        if status:
            query['status'] = status
        if author:
            query['author'] = author
        return await BookRepository.get_all(query, sort_by)

    @staticmethod
    async def get_book(book_id):
        return await BookRepository.get_by_id(book_id)

    @staticmethod
    async def create_book(book_data):
        return await BookRepository.create(book_data)

    @staticmethod
    async def delete_book(book_id):
        await BookRepository.delete(book_id)