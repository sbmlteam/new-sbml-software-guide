import os
import sys
from argparse import ArgumentParser
from flask import Flask
from werkzeug.security import generate_password_hash

# Allow "guide" to be imported.
try:
    thisdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(thisdir, '..'))
except:
    sys.path.append('..')

import guide
from guide import auth
from guide import db
from guide import entry
from guide import profile


def create_app(test_config=None, init=False, python_called=False):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'guide.sqlite'),
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

	db.init_app(app)

	if init:
		with app.app_context():
			db.init_db()
			db_instance = db.get_db()
			db_instance.execute(
				'INSERT INTO user (username, password, admin) VALUES (?, ?, ?)',
				("admin@sbml.com", generate_password_hash("admin"), 1)
			)
			db_instance.commit()


	app.register_blueprint(auth.bp)
	app.register_blueprint(entry.bp)
	app.register_blueprint(profile.bp)
	app.add_url_rule('/', endpoint='index')
		
	return app

def main():
	python_called = True

	parser = ArgumentParser(description = "SBML software guide web interface")
	parser.add_argument("-i", "--init",
			help="Re-initializes the database, clearing the existing one", action="store_true")
	args = parser.parse_args()

	app = create_app(init=args.init, python_called=python_called)
	app.run(threaded = True)


if __name__ == "__main__":
	main()
