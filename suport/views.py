from flask import (Blueprint, render_template, request, flash,
                   jsonify, redirect, url_for)
from flask_login import login_required, current_user
from .models import Post, User, Comment
from . import db
from sqlalchemy import desc
import json

views = Blueprint('views', __name__)


@views.route('/football-post', methods=['GET', 'POST'])
@login_required
def football():
    if request.method == 'POST':
        post_data = request.form.get('post')

        if len(post_data) < 10:
            flash('Post must be at least 10 characters long.',
                  category='error')
        elif len(post_data) > 1000:
            flash('Post must be no more than 1000 characters long.',
                  category='error')
        else:
            new_post = Post(data=post_data, user_id=current_user.id,
                            sport='football')
            db.session.add(new_post)
            db.session.commit()
            flash('Post added!', category='success')
            return redirect(url_for('views.football'))

    posts = Post.query.filter_by(sport='football')\
        .order_by(desc(Post.date)).all()

    for post in posts:
        post.comments = Comment.query.filter_by(post_id=post.id).all()

    return render_template("football.html", posts=posts)


@views.route('/formula1-post', methods=['GET', 'POST'])
@login_required
def formula1():
    if request.method == 'POST':
        post_data = request.form.get('post')

        if len(post_data) < 10:
            flash('Post must be at least 10 characters long.',
                  category='error')
        elif len(post_data) > 1000:
            flash('Post must be no more than 1000 characters long.',
                  category='error')
        else:
            new_post = Post(data=post_data, user_id=current_user.id,
                            sport='formula1')
            db.session.add(new_post)
            db.session.commit()
            flash('Post added to Formula 1!', category='success')
            return redirect(url_for('views.formula1'))

    posts = Post.query.filter_by(sport='formula1')\
        .order_by(desc(Post.date)).all()

    for post in posts:
        post.comments = Comment.query.filter_by(post_id=post.id).all()

    return render_template("formula1.html", posts=posts)


@views.route('/rugby-post', methods=['GET', 'POST'])
@login_required
def rugby():
    if request.method == 'POST':
        post_data = request.form.get('post')

        if len(post_data) < 10:
            flash('Post must be at least 10 characters long.',
                  category='error')
        elif len(post_data) > 1000:
            flash('Post must be no more than 1000 characters long.',
                  category='error')
        else:
            new_post = Post(data=post_data, user_id=current_user.id,
                            sport='rugby')
            db.session.add(new_post)
            db.session.commit()
            flash('Post added to Rugby!', category='success')
            return redirect(url_for('views.rugby'))

    posts = Post.query.filter_by(sport='rugby').order_by(desc(Post.date)).all()

    for post in posts:
        post.comments = Comment.query.filter_by(post_id=post.id).all()

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

        flash("Post deleted successfully!", 'success')
    else:
        flash("Post not found or unauthorized!", 'error')

    return jsonify({"redirect": url_for('views.football')})


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
        flash("Post updated successfully!", 'success')
        return jsonify({
            'status': 'success',
            'message': 'Post updated successfully!'
        })
    else:
        flash("Post not found or unauthorized!", 'error')
        return jsonify({
            'status': 'error',
            'message': 'Post not found or unauthorized!'
        })


@views.route('/add-comment/<string:sport>/<int:post_id>', methods=['POST'])
@login_required
def add_comment(sport, post_id):
    if request.method == 'POST':
        content = request.form.get('content')
        user_id = current_user.id

        if not content:
            flash('Comment content cannot be empty', 'error')
        elif len(content) > 1000:
            flash('Comment must be no more than 1000 characters long.',
                  'error')
        else:
            comment = Comment(content=content, user_id=user_id,
                              post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash('Comment added successfully', 'success')

    return redirect(request.referrer)


@views.route('/delete-comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != current_user.id:
        flash("Permission denied.", 'error')
        return jsonify({"redirect": request.referrer})

    db.session.delete(comment)
    db.session.commit()

    flash("Comment deleted successfully.", 'success')

    return jsonify({"redirect": request.referrer})


@views.route('/profile', methods=['GET', 'POST', '<int:user_id>'])
@login_required
def profile(user_id=None):
    if user_id is None:
        user = current_user
    else:
        user = User.query.get(user_id)

    posts = Post.query.filter_by(user_id=user.id).all()
    comments = Comment.query.filter_by(user_id=user.id).all()

    if request.method == 'POST':
        favourite_sport = request.form.get('favourite_sport')
        favourite_team = request.form.get('favourite_team')

        user.favourite_sport = favourite_sport
        user.favourite_team = favourite_team
        db.session.commit()

    return render_template("profile.html", user=user, posts=posts,
                           comments=comments)


@views.route('/all-users')
@login_required
def all_users():
    users = User.query.all()
    return render_template('all-users.html', users=users)


@views.route('/edit_bio', methods=['POST'])
@login_required
def edit_bio():
    user = current_user
    new_bio = request.form.get('bio')

    if len(new_bio) > 500:
        flash("Bio must be 500 characters or less.", 'error')
    elif new_bio != user.bio:
        user.bio = new_bio
        db.session.commit()
        flash("Bio updated successfully!", 'success')

    return redirect(url_for('views.profile', user_id=user.id))


@views.route('/edit_favourite_sport', methods=['POST'])
@login_required
def edit_favourite_sport():
    user = current_user
    new_sport = request.form.get('favourite_sport')

    if len(new_sport) == 0:
        flash("Favorite sport cannot be blank.", 'error')
        return redirect(url_for('views.profile', user_id=user.id))

    if len(new_sport) > 25:
        flash("Favorite sport must be 25 characters or less.", 'error')
    elif new_sport != user.favourite_sport:
        user.favourite_sport = new_sport
        db.session.commit()
        flash("Favorite sport updated successfully!", 'success')

    return redirect(url_for('views.profile', user_id=user.id))


@views.route('/edit_favourite_team', methods=['POST'])
@login_required
def edit_favourite_team():
    user = current_user
    new_team = request.form.get('favourite_team')

    if len(new_team) == 0:
        flash("Favorite team cannot be blank.", 'error')
        return redirect(url_for('views.profile', user_id=user.id))

    if len(new_team) > 25:
        flash("Favorite team must be 25 characters or less.", 'error')
    elif new_team != user.favourite_team:
        user.favourite_team = new_team
        db.session.commit()
        flash("Favorite team updated successfully!", 'success')

    return redirect(url_for('views.profile', user_id=user.id))
