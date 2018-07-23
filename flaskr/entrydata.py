class Entry:

	def __init__(self, form, g):
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
		elif contact == 'Other':
			self.contact = form['contact_other_txt']

		# fetch dependency
		self.dependency = form['dependency']
		if self.dependency == 'Yes':
			self.dependency = form['dependency_yes_txt']
		elif self.dependency == 'Other':
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
