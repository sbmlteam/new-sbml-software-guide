class Search:

	# assigns relevant variables using an inputted dictionary
	def setup(self, temp_vars):
		self.keywords = temp_vars.get("keywords", "").split(", ")

		self.os_other = int(temp_vars.get("os_other", 0))
		self.os_list = temp_vars.get("os_list", "").split(", ")
		print ("init", self.os_list)

		self.academic = int(temp_vars.get("academic", 0))
		self.nonprofit = int(temp_vars.get("nonprofit", 0))
		self.govt = int(temp_vars.get("govt", 0))
		self.commercial = int(temp_vars.get("commercial", 0))

		self.dependency = int(temp_vars.get("dependency", 0))
		self.no_dependency = int(temp_vars.get("no_dependency", 0))
		self.dependency_list = temp_vars.get("dependency_list", "").split(", ")
		print (self.dependency_list)
		print (", ".join(self.dependency_list))

	# works off a URL string to create a search object
	def __init__(self, input_str):
		no_tuples = input_str.split(";")
		tuples = [s.split("-") for s in no_tuples]
		temp_vars = dict(tuples)
		self.setup(temp_vars)

	def __getitem__(self, arg):
		return getattr(self, arg)

	# sets its values based on those of a request.form
	# works off of a submitted form to modify an extant search
	def set(self, form):
		self.keywords = form['keywords'].split(", ")

		# fetch operating systems
		self.os_list = form.getlist('os')
		print (self.os_list)
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
			self.no_dependency = 1
			self.dependency = 0
		elif form['dependency'] == 'Yes':
			self.dependency = 1
			self.no_dependency = 0
			self.dependency_list = form['dependency_list'].split(", ")
		else:
			self.dependency = 0
			self.no_dependency = 0

		print (self.__str__())
	
	# converts the object to a URL-safe string
	def __str__(self):
		url = [str(attr) + "-" + (
					", ".join(self[str(attr)]) 
					if (type(self[str(attr)]) == type([])) 
					# if (attr == 'dependency_list')
					else str(self[str(attr)]))
				for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
		return ";".join(url)

	# returns a pretty version of the object for display
	def pretty_str(self):
		display_str = "\t"
		s = "\n\t" # stands for separator; inserted between items
		if self.keywords: display_str += "Keywords: " + ", ".join(self.keywords) + s
		if self.academic: display_str += "Free for academic use" + s
		if self.nonprofit: display_str += "Free for nonprofit use" + s
		if self.govt: display_str += "Free for government use" + s
		if self.commercial: display_str += "Free for commercial use" + s
		if self.dependency_list and self.dependency: display_str += "Acceptable dependencies: " + ", ".join(self.dependency_list) + s
		elif self.no_dependency: display_str += "No dependencies" + s
		else: display_str += "Any dependencies" + s
		
		if self.os_list: 
			os_list_list = self.os_list
			# remove 'Other' from the end of the list if it's there
			if self.os_other:
				del os_list_list[len(os_list_list)-1]

			display_str += "Required OS support: " + ", ".join(os_list_list) + s

		# remove the separator from the last item
		return display_str[0:len(display_str)-len(s)]

	# returns a real list from its string representation
	def get_list(self, string):
		# going from ['foo', 'bar'] to a real list:
		# remove outer [], split by commas then remove '' from each item
		return [item[1:len(item)-1] for item in string[1:len(string)-1].split(", ")]
