DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS recovery;

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	admin INTEGER
);

CREATE VIRTUAL TABLE post USING fts4 (
	-- id INTEGER PRIMARY KEY AUTOINCREMENT,
	author_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

	-- Inputted by user --
	name TEXT NOT NULL,
	contact TEXT NOT NULL,
	contact_me INTEGER, -- INTEGER = bool
	version TEXT NOT NULL,
	site TEXT NOT NULL,
	descr TEXT NOT NULL,
	tags TEXT NOT NULL,

	src TEXT NOT NULL,
	src_other_txt TEXT NOT NULL,
	dependency TEXT NOT NULL,
	dependency_other INTEGER,

	lvl_1_1_i INTEGER,
	lvl_1_2_i INTEGER,
	lvl_2_1_i INTEGER,
	lvl_2_2_i INTEGER,
	lvl_2_3_i INTEGER,
	lvl_2_4_i INTEGER,
	lvl_2_5_i INTEGER,
	lvl_3_1_i INTEGER,
	lvl_3_2_i INTEGER,

	lvl_1_1_e INTEGER,
	lvl_1_2_e INTEGER,
	lvl_2_1_e INTEGER,
	lvl_2_2_e INTEGER,
	lvl_2_3_e INTEGER,
	lvl_2_4_e INTEGER,
	lvl_2_5_e INTEGER,
	lvl_3_1_e INTEGER,
	lvl_3_2_e INTEGER,

	pkg_array_r INTEGER,
	pkg_distr_r INTEGER,
	pkg_flux_r INTEGER,
	pkg_groups_r INTEGER,
	pkg_heir_r INTEGER,
	pkg_layout_r INTEGER,
	pkg_multi_r INTEGER,
	pkg_quali_r INTEGER,
	pkg_render_r INTEGER,
	pkg_spacial_r INTEGER,

	pkg_array_w INTEGER,
	pkg_distr_w INTEGER,
	pkg_flux_w INTEGER,
	pkg_groups_w INTEGER,
	pkg_heir_w INTEGER,
	pkg_layout_w INTEGER,
	pkg_multi_w INTEGER,
	pkg_quali_w INTEGER,
	pkg_render_w INTEGER,
	pkg_spacial_w INTEGER,

	pkg_array_f INTEGER,
	pkg_distr_f INTEGER,
	pkg_flux_f INTEGER,
	pkg_groups_f INTEGER,
	pkg_heir_f INTEGER,
	pkg_layout_f INTEGER,
	pkg_multi_f INTEGER,
	pkg_quali_f INTEGER,
	pkg_render_f INTEGER,
	pkg_spacial_f INTEGER,

	uses_model INTEGER,
	uses_numsim INTEGER,
	uses_analysis INTEGER,
	uses_visual INTEGER,
	uses_integrate INTEGER,
	uses_manage INTEGER,
	uses_convert INTEGER,
	uses_prog INTEGER,
	uses_net INTEGER,
	uses_other INTEGER,
	uses_other_txt TEXT NOT NULL,

	lib_sbml INTEGER,
	lib_jsbml INTEGER,
	lib_custom INTEGER,
	lib_idk INTEGER,
	lib_other INTEGER,
	lib_other_txt TEXT NOT NULL,

	-- os list
	os TEXT NOT NULL,
	os_other INTEGER,

	-- fee checklist
	fee_academic INTEGER NOT NULL,
	fee_nonprofit INTEGER NOT NULL,
	fee_govt INTEGER NOT NULL,
	fee_commercial INTEGER NOT NULL,

	-- optional parameters
	contact_info TEXT,
	doi TEXT,
	citation TEXT,
	api TEXT,
	extra TEXT,

	FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE recovery (
	email TEXT UNIQUE NOT NULL,
	code TEXT NOT NULL
);
