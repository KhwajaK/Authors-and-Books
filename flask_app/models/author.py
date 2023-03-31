from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import book

class Authors:
    db="books_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []
        self.favorite_books=[]


    @classmethod
    def get_all_authors(cls):
        query= """ SELECT * FROM authors; """
        results = connectToMySQL(cls.db).query_db(query)
        authors = []
        for x in results:
            authors.append(cls(x))
        return authors
    
    @classmethod
    def save_author(cls, data):
        query= """ INSERT INTO authors (name) VALUES (%(name)s) ;"""
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def one_author(cls, data):
        query= """ SELECT * FROM authors WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def add_favorite(cls, data):
        query=""" INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"""
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def author_with_favorites(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        author = cls(results[0])
        for row in results:
            if row['books.id'] == None:
                break
            data = {
                "id": row['books.id'],
                "title": row['title'],
                "num_of_pages": row['num_of_pages'],
                "created_at": row['books.created_at'],
                "updated_at": row['books.updated_at']
            }
            author.favorite_books.append(book.Books(data))
        return author

    @classmethod
    def author_without_favorites(cls, data):
        query = """SELECT * FROM authors WHERE authors.id NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s);"""
        unfave_list= []
        results = connectToMySQL(cls.db).query_db(query,data)
        for x in results:
            unfave_list.append(cls(x))
        print(unfave_list, "here is your list")
        return unfave_list