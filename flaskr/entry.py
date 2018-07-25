from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from entrydata import *

bp = Blueprint('entry', __name__)

@bp.route('/')
def index():
	db = get_db()
	posts = db.execute(
		'SELECT *'
		' FROM post p JOIN user u ON p.author_id = u.id'
		' ORDER BY created DESC'
	).fetchall()
	return render_template('entry/index.html', entries=posts)
	
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
	entry=None
	if request.method == 'POST':
		entry = Entry(request.form, g)
		error = entry.get_error()
		
		if error is not None:
			flash(error)
		else:
			entry.insert(get_db())
			return redirect(url_for('entry.index'))
	
	# we set select _contact and _dependency to their defaults

	return render_template('entry/update.html', select_contact=1,
			select_dependency=0, entry=entry, edit=False)

def get_post(id, check_author=True):
	post = get_db().execute(
		'SELECT *'
		' FROM post p JOIN user u ON p.author_id = u.id'
		' WHERE p.id = ?',
		(id,)
	).fetchone()
	
	if post is None:
		abort(404, "Entry id {0} doesn't exist.".format(id))
		
	if check_author and post['author_id'] != g.user['id']:
		abort(403)
	
	return post
	
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
	post = get_post(id)
	
	if request.method == 'POST':
		entry = Entry(request.form, g)
		error = entry.get_error()
		
		if error is not None:
			flash(error)
		else:
			entry.update(get_db(), id)
			return redirect(url_for('entry.index'))

	select_contact = post['contact_me']
	select_dependency = 0 if post['dependency'] == "No" else (1 if not post['dependency_other'] else 2)
	
	return render_template('entry/update.html', select_contact=select_contact, 
			select_dependency=select_dependency, entry=post, edit=True)
	
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
	get_post(id) # make sure the post exists
	db = get_db()
	db.execute('DELETE FROM post WHERE id = ?', (id,))
	db.commit()
	return redirect(url_for('entry.index'))
