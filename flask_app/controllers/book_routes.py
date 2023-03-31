from flask_app import app
from flask_app.models import author, book
from flask import request, render_template, redirect

@app.route('/add/book')
def add_book():
    show_books = book.Books.get_all_books()
    return render_template('books.html', all_books = show_books)

@app.route('/save/book', methods=['POST'])
def create_book():
    data = {
        'title':request.form['title'],
        'num_of_pages':request.form['num_of_pages']
    }
    book_id = book.Books.save_book(data)
    return redirect('/add/book')

@app.route('/show/book/<int:id>')
def show_book(id):
    data={'id':id}
    return render_template('view_book.html', favorited=book.Books.authors_favorites_books(data), unfavorited=author.Authors.author_without_favorites(data), one_book= book.Books.get_one_book(data))

@app.route('/add/author/fave', methods=['POST'])
def add_fave_to_author():
    data={
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    author.Authors.add_favorite(data)
    return redirect(f"/show/book/{request.form['book_id']}")
