from flask_app import app
from flask_app.models import author, book
from flask import request, render_template, redirect

@app.route('/')
def index():
    return redirect('/authors')

@app.route('/authors')
def author_page():
    show_authors = author.Authors.get_all_authors()
    return render_template('authors.html', authors = show_authors)

@app.route('/add/author', methods=['POST'])
def create_author():
    data = {
        "name": request.form['name']
    }
    author_id = author.Authors.save_author(data)
    return redirect('/authors')

@app.route('/show/author/<int:id>')
def show_author(id):
    author_dict={
        'id':id
    }
    return render_template('view_author.html', author_faves = author.Authors.author_with_favorites(author_dict), unfave_books= book.Books.unfavorited_books(author_dict), one_author= author.Authors.one_author(author_dict))

@app.route('/add/book/fave', methods=['POST'])
def add_fave():
    fave_data={
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    book.Books.add_favorite_book(fave_data)
    return redirect(f"/show/author/{request.form['author_id']}")