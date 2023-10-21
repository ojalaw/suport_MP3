from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/football', methods=['GET', 'POST'])
@login_required
def football():
    if request.method == 'POST':
        note_data = request.form.get('note')
        new_note = Note(data=note_data, user_id=current_user.id, sport='football')
        db.session.add(new_note)
        db.session.commit()
        flash('Note added to Football!', category='success')
    notes = Note.query.filter_by(sport='football').all()
    return render_template("football.html", notes=notes)

@views.route('/formula1', methods=['GET', 'POST'])
@login_required
def formula1():
    if request.method == 'POST':
        note_data = request.form.get('note')
        new_note = Note(data=note_data, user_id=current_user.id, sport='formula1')
        db.session.add(new_note)
        db.session.commit()
        flash('Note added to Formula1!', category='success')
    notes = Note.query.filter_by(sport='formula1').all()
    return render_template("formula1.html", notes=notes)

@views.route('/rugby', methods=['GET', 'POST'])
@login_required
def rugby():
    if request.method == 'POST':
        note_data = request.form.get('note')
        new_note = Note(data=note_data, user_id=current_user.id, sport='rugby')
        db.session.add(new_note)
        db.session.commit()
        flash('Note added to Rugby!', category='success')
    notes = Note.query.filter_by(sport='rugby').all()
    return render_template("rugby.html", notes=notes)

@views.route('/')
def overview():
    return render_template("overview.html")

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():  
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/edit-note', methods=['POST'])
@login_required
def edit_note():
    data = json.loads(request.data)
    noteId = data['noteId']
    newText = data['text']
    note = Note.query.get(noteId)
    if note and note.user_id == current_user.id:
        note.data = newText
        db.session.commit()
        return jsonify({"message": "Note updated successfully!"})
    else:
        return jsonify({"error": "Note not found or unauthorized!"}), 400
