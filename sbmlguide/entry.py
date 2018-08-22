from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import sbmlguide
from sbmlguide.auth import *
from sbmlguide.db import *
from sbmlguide.entrydata import *
from sbmlguide.search import *

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

	posts = db.execute(search.search_str()).fetchall()

	total = db.execute('SELECT COUNT(*) FROM post').fetchone()[0]

	return render_template('entry/index.html',
			entries=posts, search=search, current=len(posts), total=total)

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
	lib_list = json.loads(entry['lib'])
	uses_list = json.loads(entry['uses'])
	lvl_list = json.loads(entry['sbml_lvl'])
	pkg_list = json.loads(entry['sbml_pkg'])

	return render_template('entry/view.html', 
			os_list=os_list, lib_list=lib_list, uses_list=uses_list,
			lvl_list=lvl_list, pkg_list=pkg_list,
			entry=entry, search=get_search(request))
	
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
	
	os_list = json.loads(post['os'])
	lib_list = json.loads(post['lib'])
	uses_list = json.loads(post['uses'])
	lvl_list = json.loads(post['sbml_lvl'])
	pkg_list = json.loads(post['sbml_pkg'])

	return render_template('entry/update.html',
			select_contact=select_contact, select_dependency=select_dependency,
			os_list=os_list, lib_list=lib_list, uses_list=uses_list,
			lvl_list=lvl_list, pkg_list=pkg_list,
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
