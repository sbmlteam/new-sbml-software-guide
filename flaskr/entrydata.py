class Entry:

	def __init__(self, form, g):
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
		self.dependency = form['dependency']
		self.dependency_other = 0
		if self.dependency == 'Yes':
			# self.depenency_other = 0
			self.dependency = form['dependency_yes_txt']
		elif self.dependency == 'Other':
			self.dependency_other = 1
			self.dependency = form['dependency_other_txt']

		# fetch operating systems
		self.os = form.getlist('os')
		if self.os == 'Other':
			self.os.append(form['os_other_txt'])

		# fee marking
		self.fee_academic = self.get_fee('fee_academic', form)
		self.fee_nonprofit = self.get_fee('fee_nonprofit', form)
		self.fee_govt = self.get_fee('fee_govt', form)
		self.fee_commercial = self.get_fee('fee_commercial', form)

	def __getitem__(self, arg):
		return getattr(self, arg)

	# returns 0 if there's no fee; else 1
	def get_fee(self, name, form):
		return 0 if form[name] == 'Free' else 1

	# returns any applicable errors
	def get_error(self):
		error = None
		if not self.name:
			error = 'Please name your entry!'
		
		return error

	# inserts this entry into the database
	def insert(self, db):
		db.execute(
			'INSERT INTO post'
			' (author_id, name, contact, contact_me, version, site, descr, tags,'
			' dependency, dependency_other, fee_academic, fee_nonprofit, fee_govt, fee_commercial)'
			' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
			(self.author_id, self.name, self.contact, self.contact_me, self.version, self.site, 
			self.descr, self.tags, self.dependency, self.dependency_other,
			self.fee_academic, self.fee_nonprofit, self.fee_govt, self.fee_commercial)
		)
		db.commit()

	# updates this entry in the database
	def update(self, db, id):
		db.execute(
			'UPDATE post SET'
			' name = ?, contact = ?, contact_me = ?, version = ?, site = ?, descr = ?, tags = ?,'
			' dependency = ?, dependency_other = ?, fee_academic = ?, fee_nonprofit = ?,'
			' fee_govt = ?, fee_commercial = ?'
			' WHERE id = ?',
			(self.name, self.contact, self.contact_me, self.version, self.site, self.descr, self.tags,
			self.dependency, self.dependency_other, self.fee_academic, self.fee_nonprofit,
			self.fee_govt, self.fee_commercial, id)
		)
		db.commit()
