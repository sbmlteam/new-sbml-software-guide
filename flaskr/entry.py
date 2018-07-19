from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('entry', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, name, descr, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('entry/index.html', entries=posts)
    
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        descr = request.form['descr']
        error = None
        
        if not name:
            error = 'Please name your post!'
            
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (name, descr, author_id)'
                ' VALUES(?, ?, ?)', 
                (name, descr, g.user['id'])
            )
            db.commit()
            return redirect(url_for('entry.index'))
            
    return render_template('entry/update.html', entry=None, edit=False)

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, name, descr, created, author_id, username'
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
        name = request.form['name']
        descr = request.form['descr']
        error = None
        
        if not name:
            error = 'Please name your post!'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET name = ?, descr = ?'
                ' WHERE id = ?',
                (name, descr, id)
            )
            db.commit()
            return redirect(url_for('entry.index'))
    
    return render_template('entry/update.html', entry=post, edit=True)
    
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('entry.index'))
