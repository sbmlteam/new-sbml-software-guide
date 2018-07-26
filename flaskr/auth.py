import functools
import string
import random

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		password2 = request.form['password2']
		db = get_db()
		error = None
		
		if db.execute(
			'SELECT id FROM user WHERE username = ?', (username,)
		).fetchone() is not None:
			error = 'User {} is already registered.'.format(username)
		elif not username:
			error = 'Email is required.'
		elif "@" not in username:
			error = 'Please enter a valid email.'
		elif not password:
			error = 'Password is required.'
		elif password != password2:
			error = 'The passwords are not the same.'
			
		if error is None:
			db.execute(
				'INSERT INTO user (username, password, admin) VALUES (?, ?, ?)',
				(username, generate_password_hash(password), 0)
			)
			db.commit()
			return redirect(url_for('auth.login'))
			
		flash(error)
		
	return render_template('auth/register.html')
	
@bp.route('/recover', methods=('GET', 'POST'))
def recover():
	if request.method == 'POST':
		username = request.form['username']
		db = get_db()
		error = None
		
		if db.execute(
			'SELECT id FROM user WHERE username = ?', (username,)
		).fetchone() is None:
			error = 'No user associated with {}.'.format(username)
		
		if error is None:
			code = generate_code()
			db.execute('DELETE FROM recovery WHERE email = ?', (username, ))
			db.execute('INSERT INTO recovery (email, code) VALUES(?, ?)', (username, generate_password_hash(code)))
			print (code)

			# TODO: Send email

			db.commit()
			return redirect(url_for('auth.recover_sent', email=username))
			
		flash(error)
		
	return render_template('auth/recover.html')

@bp.route('/recover/sent', methods=('GET', 'POST'))
def recover_sent():
	email = request.args['email']
	if request.method == 'POST':
		code = request.form['code']
		passworda = request.form['passworda']
		passwordb = request.form['passwordb']
		db = get_db()
		error = None

		correct_code = db.execute(
				'SELECT code FROM recovery WHERE email = ?', (email,)
				).fetchone()['code']
		if not check_password_hash(correct_code, code):
			error = 'Incorrect code.'
		elif passworda is not passwordb:
			error = 'The passwords must match.'

		if error is not None:
			flash(error)
		else:
			db.execute('UPDATE user SET password = ? WHERE username = ?', (generate_password_hash(passworda), email))
			db.commit()
			return redirect(url_for('auth.login'))
	return render_template('auth/recover_sent.html', email=email)
	
@bp.route('/recover/success', methods=('GET', 'POST'))
def success():
	# sent email
	pass
		
@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		user = db.execute(
			'SELECT * FROM user WHERE username = ?', (username,)
		).fetchone()
		
		if user is None:
			error = 'Incorrect username.'
		elif not check_password_hash(user['password'], password):
			error = 'Incorrect password.'
		
		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('index'))
			
		flash(error)
		
	return render_template('auth/login.html')
	
@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')
	
	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id = ?', (user_id,)
		).fetchone()
		
@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

@bp.route('/delete', methods=('GET', 'POST'))
def delete():
	user_id = session.get('user_id')
	db = get_db()
	db.execute('DELETE FROM post WHERE author_id = ?', (user_id,))
	db.execute('DELETE FROM user WHERE id = ?', (user_id,))
	db.commit()
	return redirect(url_for('entry.index'))

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))
			
		return view(**kwargs)
	
	return wrapped_view

def generate_code(size=8, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
