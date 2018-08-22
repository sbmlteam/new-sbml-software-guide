import json
import time
from datetime import datetime

class Entry:

	def __init__(self, form, g):
		self.error = None

		self.created = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')

		self.author_id = g.user['id']
		# fetch basic forms
		self.name = form['name']
		self.descr = form['descr']
		self.version = form['version']
		self.site = form['site']
		self.tags = form['tags']

		# fetch contact
		self.contact = form['contact']
		if self.contact == 'Use my username':
			self.contact = g.user['username']
			self.contact_me = 1
		elif self.contact == 'Other':
			self.contact = form['contact_other_txt']
			self.contact_me = 0

		# fetch dependency
		try: 
			self.dependency = form['dependency']
			self.dependency_other = 0
			if self.dependency == 'Yes':
				# self.depenency_other = 0
				self.dependency = form['dependency_yes_txt']
			elif self.dependency == 'Other':
				self.dependency_other = 1
				self.dependency = form['dependency_other_txt']
		except: self.error = 'Please select the dependencies your software has!'

		# fetch operating systems
		self.os = form.getlist('os')
		if "Other" in self.os and form['os_other_txt']:
			self.os_other = 1
			self.os.insert(0, form['os_other_txt'])
			self.os.remove("Other")
		else:
			self.os_other = 0
		# we use json.dumps because self.os is a list but we need a string
		self.os = json.dumps(self.os)

		# fee marking
		self.fee_academic = self.get_fee('fee_academic', form)
		self.fee_nonprofit = self.get_fee('fee_nonprofit', form)
		self.fee_govt = self.get_fee('fee_govt', form)
		self.fee_commercial = self.get_fee('fee_commercial', form)

		# open source checks
		self.src = form['src']
		if self.src == "Other":
			self.src_other = 1
			self.src = form['src_other_txt']
		else:
			self.src_other = 0

		# sbml level
		self.sbml_lvl = json.dumps(form.getlist('sbml_lvl'))

		# level 3 package checks
		self.sbml_pkg = json.dumps(form.getlist("sbml_pkg"))

		self.uses = form.getlist("uses")
		if "Other" in self.uses and form['uses_other_txt']:
			self.uses.remove("Other")
			self.uses.insert(0, form['uses_other_txt'])
			self.uses_other = 1
		else:
			self.uses_other = 0
		self.uses = json.dumps(self.uses)

		self.lib = form.getlist("lib")
		if "Other" in self.lib and form['lib_other_txt']:
			self.lib.remove("Other")
			self.lib.insert(0, form['lib_other_txt'])
			self.lib_other = 1
		else:
			self.lib_other = 0
		self.lib = json.dumps(self.lib)

		self.contact_info = form['contact_info']
		self.doi = form['doi']
		self.citation = form['citation']
		self.api = form['api']
		self.extra = form['extra']

	def __getitem__(self, arg):
		return getattr(self, arg)

	# returns 0 if there's no fee; else 1
	def get_fee(self, name, form):
		try: return 0 if form[name] == 'Free' else 1
		except: return -1

	# returns any applicable errors
	def get_error(self):
		error = None
		if self.error:
			error = self.error
		elif not self.name:
			error = 'Please name your entry!'
		elif not self.version:
			error = 'Please enter a version!'
		elif not self.descr:
			error = 'Please provide a description of your software!'
		elif len(self.descr) > 1024:
			error = 'Please provide a shorter description of your software!'
		elif not self.tags:
			error = 'Please enter some key phrases to describe your software!'
		elif len(self.tags.splitlines()) < 3:
			error = 'Please enter more phrases to describe your software!'
		elif self.os == json.dumps([]):
			error = 'Please select the operating systems your software supports!'
		elif not self.dependency:
			error = 'Please select the dependencies your software has!'
		elif (self.fee_academic == -1 or self.fee_nonprofit == -1 or
			self.fee_govt == -1 or self.fee_commercial == -1):
			error = 'Please finish your fees section!'
		elif self.sbml_lvl == json.dumps([]):
			error = 'Please select the SBML levels your software supports!'
		elif not self.src:
			error = 'Please provide information about your source code!'
		elif self.lib == json.dumps([]):
			error = 'Please select the SBML library your software uses!'
		elif self.uses == json.dumps([]):
			error = 'Please provide more details about your software\'s facilities!'
		
		return error

	# inserts this entry into the database
	def insert(self, db):
		# gets a list of every property this entry has
		prop_name = [str(attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not attr == "error"]
		prop_val = [self[attr] for attr in prop_name]

		# inserts those properties and their respective values into the database
		cmd = ("INSERT INTO post (" + ", ".join(prop_name) + ")" + 
				" VALUES (" + ", ".join(len(prop_val)*('?',)) + ")")

		print(cmd)

		db.execute(cmd, tuple(prop_val))
		db.commit()

	# updates this entry in the database
	def update(self, db, id, g):
		# we need to check if it's an admin editing, since
		# their username shouldn't overwrite the original one
		if g.user['admin'] == 1 and self.contact_me:
			contact = db.execute(
				'SELECT contact FROM post WHERE id = ?',
				(id, )
			).fetchone()['contact']
		else:
			contact = self.contact

		prop_name = [str(attr) for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__") and not attr == "error"]
		prop_val = [self[attr] for attr in prop_name]
		prop_val.append(id)

		cmd = ("UPDATE post SET " + ", ".join([name + " = ?" for name in prop_name]) +
				"WHERE rowid = ?")

		db.execute(cmd, tuple(prop_val))
		db.commit()
