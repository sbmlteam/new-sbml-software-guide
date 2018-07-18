# Taken from http://flask.pocoo.org/docs/1.0/tutorial/factory/

import os
import sys
from argparse import ArgumentParser

from flask import Flask

def create_app(test_config=None, init=False, python_called=False):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
        
    if python_called:
        import db
        import auth
        import entry
        import profile
    else:
        from . import db
        from . import auth
        from . import entry
        from . import profile
    
    db.init_app(app)

    if init:
        with app.app_context():
            db.init_db()

    app.register_blueprint(auth.bp)
    app.register_blueprint(entry.bp)
    app.register_blueprint(profile.bp)
    app.add_url_rule('/', endpoint='index')
        
    return app

if __name__ == "__main__":
    python_called = True

    parser = ArgumentParser(description = "SBML software guide web interface")
    parser.add_argument("-i", "--init",
            help="Re-initializes the database, clearing the existing one", action="store_true")
    args = parser.parse_args()

    app = create_app(init=args.init, python_called=python_called)
    app.run(threaded = True)
