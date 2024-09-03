from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app
from bson.objectid import ObjectId
from board.database import get_db
from datetime import datetime

bp = Blueprint('posts', __name__)

@bp.route("/create", methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        author = request.form['author'] or 'Anonymous'
        message = request.form['message']

        if message: 
            db = get_db()
            posts_collection = db['posts']
            post={
                'author': author,
                'message': message,
                'created': datetime.now()
            }
            posts_collection.insert_one(post)
            current_app.logger.debug(f'New post by {author}')
            flash(f'Thank you for posting, {author}!', category='success')
            return redirect(url_for('posts.posts'))
        else: 
            flash('You need to post a message!', category='error')
    return render_template('posts/create.html')

@bp.route('/posts')
def posts():
    db = get_db()
    posts_collection = db['posts']
    posts = posts_collection.find().sort('created', -1)     # -1 is descending order
    return render_template('posts/posts.html', posts=posts)