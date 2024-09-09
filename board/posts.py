from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app
from bson.objectid import ObjectId
from board.database import get_db
from datetime import datetime
from datetime import datetime, timezone


bp = Blueprint('posts', __name__)

@bp.route("/create", methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        author = request.form['author'] or 'Anonymous'
        message = request.form['message']

        if bool(message.strip()):   # Check for non empty strings
            db = get_db()
            posts_collection = db['posts']
            post={
                'author': author,
                'message': message,
                'created': datetime.now(timezone.utc)
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
    replies_collection = db['replies']
    pipeline = [
        {
            '$lookup': {
                'from': 'replies',
                'localField': '_id',
                'foreignField': 'post_id',  # Assuming replies have a field 'post_id' referring to the post
                'as': 'replies'
            }
        },
        {
            '$addFields': {
                'replyCount': { '$size': '$replies' }
            }
        },
        {
            '$sort': { 'created': -1 }  # Sort by creation date
        }
    ]
    posts = list(posts_collection.aggregate(pipeline))
    return render_template('posts/posts.html', posts=posts)

@bp.route("/posts/<post_id>/add_reply", methods=('GET', 'POST'))
def reply(post_id):
    if request.method == 'POST':
        author = request.form['author'] or 'Anonymous'
        message = request.form['message']

        if bool(message.strip()):   # Check for non empty strings
            db = get_db()
            replies_collection = db['replies']
            post={
                'post_id': ObjectId(post_id),
                'author': author,
                'message': message,
                'created': datetime.now(timezone.utc)
            }
            replies_collection.insert_one(post)
            current_app.logger.debug(f'New post by {author}')
            flash(f'Thank you for your reply, {author}!', category='success')
            return redirect(url_for('posts.replies', post_id=post_id))
        else: 
            flash('You need to post a message!', category='error')
    return render_template('replies/create.html')

@bp.route("/posts/<post_id>/replies",)
def replies(post_id):
    db = get_db()
    replies_collection = db['replies']
    posts_collection = db['posts']
    post = posts_collection.find_one({"_id": ObjectId(post_id)})
    replies = replies_collection.find()     # -1 is descending order
    return render_template('replies/replies.html', replies=replies, post=post)