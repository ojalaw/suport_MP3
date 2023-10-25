from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Review, User
from . import db
import json
from flask import send_from_directory
from . import app

views = Blueprint('views', __name__)

app.register_blueprint(views)

@views.route('/football', methods=['GET', 'POST'])
@login_required
def football():
    if request.method == 'POST':
        review_data = request.form.get('review')
        new_review = Review(data=review_data, user_id=current_user.id, sport='football')
        db.session.add(new_review)
        db.session.commit()
        flash('Review added to Football!', category='success')
    reviews = Review.query.filter_by(sport='football').all()
    return render_template("football.html", reviews=reviews)

@views.route('/formula1', methods=['GET', 'POST'])
@login_required
def formula1():
    if request.method == 'POST':
        review_data = request.form.get('review')
        new_review = Review(data=review_data, user_id=current_user.id, sport='formula1')
        db.session.add(new_review)
        db.session.commit()
        flash('Review added to Formula1!', category='success')
    reviews = Review.query.filter_by(sport='formula1').all()
    return render_template("formula1.html", reviews=reviews)

@views.route('/rugby', methods=['GET', 'POST'])
@login_required
def rugby():
    if request.method == 'POST':
        review_data = request.form.get('review')
        new_review = Review(data=review_data, user_id=current_user.id, sport='rugby')
        db.session.add(new_review)
        db.session.commit()
        flash('Review added to Rugby!', category='success')
    reviews = Review.query.filter_by(sport='rugby').all()
    return render_template("rugby.html", reviews=reviews)

@views.route('/')
def overview():
    return render_template("overview.html")

@views.route('/delete-review', methods=['POST'])
@login_required
def delete_review():  
    review = json.loads(request.data)
    reviewId = review['reviewId']
    review = Review.query.get(reviewId)
    if review:
        if review.user_id == current_user.id:
            db.session.delete(review)
            db.session.commit()

    return jsonify({})

@views.route('/edit-review', methods=['POST'])
@login_required
def edit_review():
    data = json.loads(request.data)
    reviewId = data['reviewId']
    newText = data['text']
    review = Review.query.get(reviewId)
    if review and review.user_id == current_user.id:
        review.data = newText
        db.session.commit()
        return jsonify({"message": "Review updated successfully!"})
    else:
        return jsonify({"error": "Review not found or unauthorized!"}), 400
    
@views.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
