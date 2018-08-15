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
		if "Other" in self.os:
			self.os_other = 1
			self.os.insert(0, form['os_other_txt'])
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
		self.src_other_txt = form['src_other_txt'] if self.src == "3" else ""

		# sbml level
		sbml_lvl = form.getlist('sbml_lvl')

		self.lvl_1_1_i = "lvl_1_1_i" in sbml_lvl
		self.lvl_1_2_i = "lvl_1_2_i" in sbml_lvl
		self.lvl_2_1_i = "lvl_2_1_i" in sbml_lvl
		self.lvl_2_2_i = "lvl_2_2_i" in sbml_lvl
		self.lvl_2_3_i = "lvl_2_3_i" in sbml_lvl
		self.lvl_2_4_i = "lvl_2_4_i" in sbml_lvl
		self.lvl_2_5_i = "lvl_2_5_i" in sbml_lvl
		self.lvl_3_1_i = "lvl_3_1_i" in sbml_lvl
		self.lvl_3_2_i = "lvl_3_2_i" in sbml_lvl

		self.lvl_1_1_e = "lvl_1_1_e" in sbml_lvl
		self.lvl_1_2_e = "lvl_1_2_e" in sbml_lvl
		self.lvl_2_1_e = "lvl_2_1_e" in sbml_lvl
		self.lvl_2_2_e = "lvl_2_2_e" in sbml_lvl
		self.lvl_2_3_e = "lvl_2_3_e" in sbml_lvl
		self.lvl_2_4_e = "lvl_2_4_e" in sbml_lvl
		self.lvl_2_5_e = "lvl_2_5_e" in sbml_lvl
		self.lvl_3_1_e = "lvl_3_1_e" in sbml_lvl
		self.lvl_3_2_e = "lvl_3_2_e" in sbml_lvl

		# level 3 package checks
		sbml_pkg = form.getlist("sbml_pkg")

		self.pkg_array_r =		"pkg_array_r"	in sbml_pkg
		self.pkg_distr_r =		"pkg_distr_r"	in sbml_pkg
		self.pkg_flux_r =		"pkg_flux_r"	in sbml_pkg
		self.pkg_groups_r =		"pkg_groups_r"	in sbml_pkg
		self.pkg_heir_r =		"pkg_heir_r"	in sbml_pkg
		self.pkg_layout_r =		"pkg_layout_r"	in sbml_pkg
		self.pkg_multi_r =		"pkg_multi_r"	in sbml_pkg
		self.pkg_quali_r =		"pkg_quali_r"	in sbml_pkg
		self.pkg_render_r =		"pkg_render_r"	in sbml_pkg
		self.pkg_spacial_r =	"pkg_spacial_r"	in sbml_pkg

		self.pkg_array_w =		"pkg_array_w"	in sbml_pkg
		self.pkg_distr_w =		"pkg_distr_w"	in sbml_pkg
		self.pkg_flux_w =		"pkg_flux_w"	in sbml_pkg
		self.pkg_groups_w =		"pkg_groups_w"	in sbml_pkg
		self.pkg_heir_w =		"pkg_heir_w"	in sbml_pkg
		self.pkg_layout_w =		"pkg_layout_w"	in sbml_pkg
		self.pkg_multi_w =		"pkg_multi_w"	in sbml_pkg
		self.pkg_quali_w =		"pkg_quali_w"	in sbml_pkg
		self.pkg_render_w =		"pkg_render_w"	in sbml_pkg
		self.pkg_spacial_w =	"pkg_spacial_w"	in sbml_pkg

		self.pkg_array_f =		"pkg_array_f"	in sbml_pkg
		self.pkg_distr_f =		"pkg_distr_f"	in sbml_pkg
		self.pkg_flux_f =		"pkg_flux_f"	in sbml_pkg
		self.pkg_groups_f =		"pkg_groups_f"	in sbml_pkg
		self.pkg_heir_f =		"pkg_heir_f"	in sbml_pkg
		self.pkg_layout_f =		"pkg_layout_f"	in sbml_pkg
		self.pkg_multi_f =		"pkg_multi_f"	in sbml_pkg
		self.pkg_quali_f =		"pkg_quali_f"	in sbml_pkg
		self.pkg_render_f =		"pkg_render_f"	in sbml_pkg
		self.pkg_spacial_f =	"pkg_spacial_f"	in sbml_pkg

		uses = form.getlist("uses")

		self.uses_model		= "uses_model"		in uses
		self.uses_numsim	= "uses_numsim"		in uses
		self.uses_analysis	= "uses_analysis"	in uses
		self.uses_visual	= "uses_visual"		in uses
		self.uses_integrate	= "uses_integrate"	in uses
		self.uses_manage	= "uses_manage"		in uses
		self.uses_convert	= "uses_convert"	in uses
		self.uses_prog		= "uses_prog"		in uses
		self.uses_net		= "uses_net"		in uses
		self.uses_other		= "uses_other"		in uses

		self.uses_other_txt = form["uses_other_txt"] if self.uses_other else ""

		lib = form.getlist("lib")
		self.lib_sbml	= "lib_sbml"	in lib
		self.lib_jsbml	= "lib_jsbml"	in lib
		self.lib_custom	= "lib_custom"	in lib
		self.lib_idk	= "lib_idk"		in lib
		self.lib_other	= "lib_other"	in lib

		self.lib_other_txt = form["lib_other_txt"] if self.lib_other else ""

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
