from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment
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
        flash('Post added!', category='success')
        return redirect(url_for('views.football'))
    
    posts = Post.query.filter_by(sport='football').all()
    
    for post in posts:
        post.comments = Comment.query.filter_by(post_id=post.id).all()
    
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
        return redirect(url_for('views.formula1'))
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
        return redirect(url_for('views.rugby'))
    posts = Post.query.filter_by(sport='rugby').all()
    return render_template("rugby.html", posts=posts)

@views.route('/')
def overview():
    return render_template("overview.html")

@views.route('/delete-post', methods=['POST'])
@login_required
def delete_post():
    post_data = json.loads(request.data)
    postId = post_data['postId']
    
    post = Post.query.get(postId)
    
    if post and post.user_id == current_user.id:
        Comment.query.filter_by(post_id=postId).delete()
        
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

@views.route('/add-comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if request.method == 'POST':
        content = request.form.get('content')
        user_id = current_user.id

        if content:
            comment = Comment(content=content, user_id=user_id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()

            flash('Comment added successfully', 'success')
        else:
            flash('Comment content cannot be empty', 'error')

    return redirect(url_for('views.football'))

@views.route('/delete-comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.user_id != current_user.id:
        flash('You do not have permission to delete this comment.', category='error')
        return jsonify({"success": False, "message": "Permission denied."}), 403
    
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted!', category='success')
    
    return jsonify({"success": True, "message": "Comment deleted successfully."})






