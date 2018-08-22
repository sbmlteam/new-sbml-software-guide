class Search:

	# assigns relevant variables using an inputted dictionary
	def setup(self, temp_vars):
		self.keywords = temp_vars.get("keywords", "").split(", ")

		self.os_other = int(temp_vars.get("os_other", 0))
		self.os_list = temp_vars.get("os_list", "").split(", ")
		print ("init", self.os_list)

		self.lvl = temp_vars.get("lvl", "").split(", ")

		self.pkg = temp_vars.get("pkg", "").split(", ")
		# if future support is okay for the package, then any value
		# (read, write, or future support planned) is okay in the search
		# so we just chop off the future support planned line
		self.pkg = [(pkg[0:len(pkg)-len(": Future Support Planned")]
			if "Future Support Planned" in pkg
			else pkg)
			for pkg in self.pkg]

		self.uses_other = int(temp_vars.get("uses_other", 0))
		self.uses = temp_vars.get("uses", "").split(", ")

		self.lib = temp_vars.get("lib", "False") != "False"

		self.academic = int(temp_vars.get("academic", 0))
		self.nonprofit = int(temp_vars.get("nonprofit", 0))
		self.govt = int(temp_vars.get("govt", 0))
		self.commercial = int(temp_vars.get("commercial", 0))

		self.dependency = int(temp_vars.get("dependency", 0))
		self.no_dependency = int(temp_vars.get("no_dependency", 0))
		self.dependency_list = temp_vars.get("dependency_list", "").split(", ")

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
		if "Other" in self.os_list and form['os_other_txt']:
			self.os_other = 1
			self.os_list.insert(0, form['os_other_txt'])
			self.os_list.remove("Other")
		else:
			self.os_other = 0

		self.uses = form.getlist('uses')
		if "Other" in self.uses and form['uses_other_txt']:
			self.uses_other = 1
			self.uses.insert(0, form['uses_other_txt'])
			self.uses.remove("Other")
		else:
			self.uses_other = 0

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

		self.lvl = form.getlist('sbml_lvl')

		self.pkg = form.getlist('sbml_pkg')

		self.lib = str(bool(form.getlist('lib')))

		print (self.__str__())
	
	# converts the object to a URL-safe string
	def __str__(self):
		url = [str(attr) + "-" + (
					", ".join(self[str(attr)]) 
					if (type(self[str(attr)]) == type([])) 
					else str(self[str(attr)]))
				for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
		return ";".join(url)

	# returns a pretty version of the object for display
	def pretty_str(self):
		display_str = "\t"
		s = "\n\t" # stands for separator; inserted between items
		if len(self.keywords[0]) > 0: display_str += "Keywords: " + ", ".join(self.keywords) + s
		if self.academic: display_str += "Free for academic use" + s
		if self.nonprofit: display_str += "Free for nonprofit use" + s
		if self.govt: display_str += "Free for government use" + s
		if self.commercial: display_str += "Free for commercial use" + s
		if self.dependency_list and self.dependency: display_str += "Acceptable dependencies: " + ", ".join(self.dependency_list) + s
		elif self.no_dependency: display_str += "No dependencies" + s
		# else: display_str += "Any dependencies" + s
		
		if len(self.os_list[0]) > 0: 
			display_str += ("Required OS support: " + s + "\t" +
				(s + "\t").join(self.os_list) + s)

		if len(self.lvl[0]) > 0:
			display_str += ("Required SBML support: " + s + "\t" +
				(s + "\t").join(self.lvl) + s)

		if len(self.pkg[0]) > 0:
			display_str += ("Required packages: " + s + "\t" +
				(s + "\t").join(self.pkg) + s)

		if len(self.uses[0]) > 0:
			display_str += ("Required facilities: " + s + "\t" +
				(s + "\t").join(self.uses) + s)

		if self.lib:
			display_str += "Mainstream parser" + s

		# remove the separator from the last item
		display_str = display_str[0:len(display_str)-len(s)]
		return display_str if len(display_str) > 0 else "\tNone"

	# returns a real list from its string representation
	def get_list(self, string):
		# going from ['foo', 'bar'] to a real list:
		# remove outer [], split by commas then remove '' from each item
		return [item[1:len(item)-1] for item in string[1:len(string)-1].split(", ")]

	# returns the SQL command represented by this search
	def search_str(self):
		# we make a list of select commands and then union them
		base_cmd = (
			"SELECT p.rowid, *" +
			" FROM post p JOIN user u ON p.author_id = u.id"
			)
		cmd_list = []
		cmd_list.append(base_cmd)

		# dependency term
		if self.no_dependency:
			cmd_list.append(base_cmd + " WHERE dependency = \"\"")
		elif self.dependency:
			cmd_list.append(base_cmd + " WHERE p.dependency MATCH '" + " OR ".join(self.dependency_list) + " OR \"None\"'")

		# keyword term
		if len(self.keywords[0]) > 0:
			cmd_list.append(base_cmd + " WHERE post MATCH '" +" ".join(self.keywords) + "'")

		# os term
		if len(self.os_list[0]) > 0:
			os_list = self.os_list
			# matches the appropriate os list
			cmd_list.append(base_cmd + " WHERE os MATCH '" + " ".join(os_list) + "'")

		# fees term (NOT a keywords search; DOESN'T use fts4 searching)
		if (self.academic):
			cmd_list.append(base_cmd + " WHERE fee_academic = 0")
		if (self.nonprofit):
			cmd_list.append(base_cmd + " WHERE fee_nonprofit = 0")
		if (self.govt):
			cmd_list.append(base_cmd + " WHERE fee_govt = 0")
		if (self.commercial):
			cmd_list.append(base_cmd + " WHERE fee_commercial = 0")

		# sbml level term
		if len(self.lvl[0]) > 0:
			cmd_list.append(base_cmd + " WHERE sbml_lvl MATCH '\"" + "\" \"".join(self.lvl) + "\"'")

		# sbml lvl3 packages term
		if len(self.pkg[0]) > 0:
			cmd_list.append(base_cmd + " WHERE sbml_pkg MATCH '\"" + "\" \"".join(self.pkg) + "\"'")

		# required uses term
		if len(self.uses[0]) > 0:
			cmd_list.append(base_cmd + " WHERE uses MATCH '\"" + "\" \"".join(self.uses) + "\"'")

		if self.lib:
			cmd_list.append(base_cmd + " WHERE lib MATCH 'JSBML OR libSBML'")

		# joins all the search terms and sorts them
		if len(cmd_list) > 0:
			cmd = " INTERSECT ".join(cmd_list) 
		else:
			cmd = base_cmd
		
		cmd += " ORDER BY created DESC"

		print (cmd)
		return cmd
