from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def overview():
    return render_template("overview.html")

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  
            db.session.add(new_note) 
            db.session.commit()
            flash('Note added!', category='success')

    notes = Note.query.all()
    return render_template("home.html", notes=notes)  

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
