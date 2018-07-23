DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS recovery;

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE post (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	author_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

	-- Inputted by user --
	name TEXT NOT NULL,
	contact TEXT NOT NULL,
	version TEXT NOT NULL,
	website TEXT NOT NULL,
	descr TEXT NOT NULL,
	tags TEXT NOT NULL,

	src TEXT NOT NULL,
	dependency NUMERIC NOT NULL,
	sbml_lvl TEXT NOT NULL,
	sbml_pkg TEXT NOT NULL,
	uses TEXT NOT NULL,
	lib TEXT NOT NULL,

	-- os checklist
	os_win INTEGER NOT NULL, -- integer = boolean
	os_mac INTEGER NOT NULL,
	os_linux INTEGER NOT NULL,
	os_web INTEGER NOT NULL,
	os_ios INTEGER NOT NULL,
	os_android INTEGER NOT NULL,
	os_na INTEGER NOT NULL,
	os_other TEXT NOT NULL,
	
	-- fee checklist
	fee_academic INTEGER NOT NULL,
	fee_nonprofit INTEGER NOT NULL,
	fee_govt INTEGER NOT NULL,
	fee_commercial INTEGER NOT NULL,

	-- optional parameters
	contact TEXT,
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
