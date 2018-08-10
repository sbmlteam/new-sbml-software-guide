from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import guide
from guide.db import get_db
from guide.entry import get_search

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/', methods=('GET', 'POST'))
def profile():
	db = get_db()
	entries = db.execute(
		'SELECT p.rowid, name' 
		' FROM post p JOIN user u ON p.author_id = u.id'
		' ORDER BY created DESC'
	).fetchall()
	return render_template('profile/index.html', email=g.user['username'], entries=entries, search=get_search(request))

@bp.route('/settings', methods=('GET', 'POST'))
def settings():
	return render_template('profile/settings.html', search=get_search(request))
