class Search:

	def __init__(self):
		self.os_other = 0
		self.os_list = []

		self.academic = 0
		self.nonprofit = 0
		self.govt = 0
		self.commercial = 0

		self.dependency = 0
		self.dependency_list = []

	def __getitem__(self, arg):
		return getattr(self, arg)
