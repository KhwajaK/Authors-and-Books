from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Books:
    db="books_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_favorites = []

    @classmethod
    def get_all_books(cls):
        query = '''SELECT * FROM books;'''
        all_books = []
        results = connectToMySQL(cls.db).query_db(query)
        for row in results:
            all_books.append(cls(row))
        return all_books
    
    @classmethod
    def get_one_book(cls, data):
        query = """ SELECT * FROM books WHERE id = %(id)s;"""
        one_book = connectToMySQL(cls.db).query_db(query,data)
        print("is this the book you're looking for??", one_book)
        return cls(one_book[0])
    
    @classmethod
    def save_book(cls, data):
        query = """ INSERT INTO books (title, num_of_pages) VALUE (%(title)s, %(num_of_pages)s);
        """
        saved_book = connectToMySQL(cls.db).query_db(query,data)
        print(saved_book)
        return saved_book

    
    @classmethod
    def authors_favorites_books(cls, data):
        query = """ SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        book = cls(results[0])
        for info in results:
            if info['authors.id'] == None:
                break
            data={
                'id': info['authors.id'],
                'name': info['name'], 
                "created_at": info['authors.created_at'],
                "updated_at": info['authors.updated_at']}
            book.authors_favorites.append(author.Authors(data))
        return book


    @classmethod
    def unfavorited_books(cls, data):
        query = """ SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s);
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        books = []
        for info in results:
            books.append(cls(info))
        print(books)
        return books
    
    
    @classmethod
    def add_favorite_book(cls, data):
        query=""" INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"""
        return connectToMySQL(cls.db).query_db(query,data)
