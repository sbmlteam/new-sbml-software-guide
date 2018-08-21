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

	uses TEXT NOT NULL,
	uses_other TEXT NOT NULL,

	sbml_pkg TEXT NOT NULL,

	sbml_lvl TEXT NOT NULL,

	lib TEXT NOT NULL,
	lib_other TEXT NOT NULL,

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
