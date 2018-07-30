class Search:

	def __init__(self):
		self.keywords = ""

		self.os_other = 0
		self.os_list = []

		self.academic = 0
		self.nonprofit = 0
		self.govt = 0
		self.commercial = 0

		self.dependency = 0
		self.dependency_list = ""

	def __getitem__(self, arg):
		return getattr(self, arg)

	# sets its values based on those of a request.form
	def set(self, form):
		self.keywords = form['keywords']

		# fetch operating systems
		self.os_list = form.getlist('os')
		if "Other" in self.os_list:
			self.os_other = 1
			self.os_list.insert(0, form['os_other_txt'])
		else:
			self.os_other = 0

		# get fees
		fees = form.getlist('fee')
		self.academic = 1 if "Academic" in fees else 0
		self.nonprofit = 1 if "Non-Profit" in fees else 0
		self.govt = 1 if "Government" in fees else 0
		self.commercial = 1 if "Commercial" in fees else 0

		# get dependencies
		if form['dependency'] == 'None':
			self.dependency = 0
		else:
			self.dependency = 1
			self.dependency_list = form['dependency_list']
