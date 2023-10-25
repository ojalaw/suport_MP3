from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Post, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/football', methods=['GET', 'POST'])
@login_required
def football():
    if request.method == 'POST':
        post_data = request.form.get('post')
        new_post = Post(data=post_data, user_id=current_user.id, sport='football')
        db.session.add(new_post)
        db.session.commit()
        flash('Post added to Football!', category='success')
    posts = Post.query.filter_by(sport='football').all()
    return render_template("football.html", posts=posts)

@views.route('/formula1', methods=['GET', 'POST'])
@login_required
def formula1():
    if request.method == 'POST':
        post_data = request.form.get('post')
        new_post = Post(data=post_data, user_id=current_user.id, sport='formula1')
        db.session.add(new_post)
        db.session.commit()
        flash('Post added to Formula1!', category='success')
    posts = Post.query.filter_by(sport='formula1').all()
    return render_template("formula1.html", posts=posts)

@views.route('/rugby', methods=['GET', 'POST'])
@login_required
def rugby():
    if request.method == 'POST':
        post_data = request.form.get('post')
        new_post = Post(data=post_data, user_id=current_user.id, sport='rugby')
        db.session.add(new_post)
        db.session.commit()
        flash('Post added to Rugby!', category='success')
    posts = Post.query.filter_by(sport='rugby').all()
    return render_template("rugby.html", posts=posts)

@views.route('/')
def overview():
    return render_template("overview.html")

@views.route('/delete-post', methods=['POST'])
@login_required
def delete_post():  
    post = json.loads(request.data)
    postId = post['postId']
    post = Post.query.get(postId)
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()

    return jsonify({})

@views.route('/edit-post', methods=['POST'])
@login_required
def edit_post():
    data = json.loads(request.data)
    postId = data['postId']
    newText = data['text']
    post = Post.query.get(postId)
    if post and post.user_id == current_user.id:
        post.data = newText
        db.session.commit()
        return jsonify({"message": "Post updated successfully!"})
    else:
        return jsonify({"error": "Post not found or unauthorized!"}), 400
