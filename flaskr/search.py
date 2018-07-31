class Search:

	def __init__(self):
		self.setup({})

	def setup(self, temp_vars):
		self.keywords = temp_vars.get("keywords", "")

		self.os_other = int(temp_vars.get("os_other", 0))
		self.os_list = list(temp_vars.get("os_list", []))

		self.academic = int(temp_vars.get("academic", 0))
		self.nonprofit = int(temp_vars.get("nonprofit", 0))
		self.govt = int(temp_vars.get("govt", 0))
		self.commercial = int(temp_vars.get("commercial", 0))

		self.dependency = int(temp_vars.get("dependency", 0))
		self.dependency_list = list(temp_vars.get("dependency_list", ""))

	def __init__(self, input_str):
		no_tuples = input_str.split(" ")
		tuples = [s.split("-") for s in no_tuples]
		temp_vars = dict(tuples)
		self.setup(temp_vars)

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

		print (self.__str__())
	
	def __str__(self):
		return " ".join(
				[str(attr) + "-" + str(self[str(attr)])
				for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
				)
