'''
Date: 2021-10-30 20:04:14
LastEditors: GC
LastEditTime: 2021-11-02 15:34:18
FilePath: \Flask-Project\website\views.py
'''
from flask import Blueprint, render_template, request, jsonify
from flask.helpers import flash
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# Create a bluprint for our flask application
views = Blueprint("views", __name__)


@views.route("/", methods=["POST", "GET"])
# To make sure we can not go to the home page unless you log in
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is too short.", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Notes added.", category="success")

    return render_template("home.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
