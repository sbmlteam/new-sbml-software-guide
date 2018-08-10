from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from entrydata import *
from search import *

import json

bp = Blueprint('entry', __name__)

def get_search(request):
	try:
		return Search(request.args['search'])
	except:
		return Search("-")
	# return Search(request.args['search'])

@bp.route('/')
def index():
	db = get_db()
	search=get_search(request)

	# we make a list of select commands and then union them
	base_cmd = (
		"SELECT p.rowid, *" +
		" FROM post p JOIN user u ON p.author_id = u.id"
		)
	cmd_list = []
	cmd_list.append(base_cmd)

	# dependency term
	if search.no_dependency:
		cmd_list.append(base_cmd + " WHERE dependency = \"\"")
	elif search.dependency:
		cmd_list.append(base_cmd + " WHERE p.dependency MATCH '" + " OR ".join(search.dependency_list) + " OR \"None\"'")

	# keyword term
	if len(search.keywords[0]) > 0:
		cmd_list.append(base_cmd + " WHERE post MATCH '" +" AND ".join(search.keywords) + "'")

	# os term
	if len(search.os_list[0]) > 0:
		os_list = search.os_list
		# matches the appropriate os list
		cmd_list.append(base_cmd + " WHERE os MATCH '" + " ".join(os_list) + "'")

	# fees term (NOT a keywords search; DOESN'T use fts4 searching)
	if (search.academic):
		cmd_list.append(base_cmd + " WHERE fee_academic = 0")
	if (search.nonprofit):
		cmd_list.append(base_cmd + " WHERE fee_nonprofit = 0")
	if (search.govt):
		cmd_list.append(base_cmd + " WHERE fee_govt = 0")
	if (search.commercial):
		cmd_list.append(base_cmd + " WHERE fee_commercial = 0")

	# joins all the search terms and sorts them
	if len(cmd_list) > 0:
		cmd = " INTERSECT ".join(cmd_list) 
	else:
		cmd = base_cmd
	
	cmd += " ORDER BY created DESC"

	print (cmd)
	
	posts = db.execute(cmd).fetchall()
	return render_template('entry/index.html', entries=posts, search=search)
	
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
			return redirect(url_for('entry.index', search=get_search(request)))
	
	# we set select _contact and _dependency to their defaults

	return render_template('entry/update.html', select_contact=1,
			select_dependency=0, entry=entry, os_list=[], edit=False, search=get_search(request))

def get_post(id, check_author=True):
	post = get_db().execute(
		'SELECT p.rowid,*'
		' FROM post p JOIN user u ON p.author_id = u.id'
		' WHERE p.rowid = ?',
		(id,)
	).fetchone()
	
	if post is None:
		abort(404, "Entry id {0} doesn't exist.".format(id))
		
	if (check_author and 
			post['author_id'] != g.user['id'] and
			g.user['admin'] != 1):
		abort(403)
	
	return post

@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
	entry = get_post(id, False)

	os_list=json.loads(entry['os'])
	if "Other" in os_list: os_list.remove("Other")

	return render_template('entry/view.html', os_list=os_list, entry=entry, search=get_search(request))
	
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
			entry.update(get_db(), id, g)
			return redirect(url_for('entry.index', search=get_search(request)))

	select_contact = post['contact_me']
	select_dependency = 0 if post['dependency'] == "None" else (1 if not post['dependency_other'] else 2)
	
	return render_template('entry/update.html', select_contact=select_contact, 
			select_dependency=select_dependency, os_list=json.loads(post['os']), 
			entry=post, edit=True, search=get_search(request))
	
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
	get_post(id) # make sure the post exists
	db = get_db()
	db.execute('DELETE FROM post WHERE rowid = ?', (id,))
	db.commit()
	return redirect(url_for('entry.index', search=get_search(request)))

@bp.route('/search', methods=('GET', 'POST'))
def search():
	search = get_search(request)
	if request.method == 'POST':
		if not search:
			search = Search("-")
		search.set(request.form)
		return redirect(url_for('entry.index', search=search))
	
	print ("search function", ", ".join(search['dependency_list']))
	return render_template('entry/search.html', search=search)

@bp.route('/search_clear', methods=('GET', ))
def search_clear():
	search = Search("-")
	return redirect(url_for('entry.index', search=search))
