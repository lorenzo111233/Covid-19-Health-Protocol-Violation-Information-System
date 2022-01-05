DROP TABLE IF EXISTS violations;

CREATE TABLE violations(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	violation TEXT NOT NULL,
	name TEXT NULL
	
);

DROP TABLE IF EXISTS stat;

CREATE TABLE stat(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	status TEXT NULL,
	penalty TEXT NOT NULL
	
);

DROP TABLE IF EXISTS user;

CREATE TABLE user(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	password TEXT NOT NULL,
	position TEXT NOT NULL,
	mail TEXT NOT NULL,
	barangay TEXT NOT NULL,
	hashCode TEXT NULL
	
);

CREATE TABLE barangays(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	barangay TEXT NOT NULL,
	name TEXT NOT NULL
	
);


DROP TABLE IF EXISTS violators;

CREATE TABLE violators(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	last_name TEXT NOT NULL,
	first_name TEXT NOT NULL,
	middle_name TEXT NOT NULL,
	house_number TEXT NOT NULL,
	street TEXT NOT NULL,
	barangay TEXT NOT NULL,
	contact int NOT NULL,
	violation TEXT NOT NULL,
	penalty TEXT NOT NULL,
	total_penalty INTEGER NOT NULL,
	date datetime DEFAULT(datetime('now')) ,
	status TEXT NOT NULL
		
);

DROP TABLE IF EXISTS pay;

CREATE TABLE pay(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	last_name TEXT NOT NULL,
	first_name TEXT NOT NULL,
	middle_name TEXT NOT NULL,
	house_number TEXT NOT NULL,
	street TEXT NOT NULL,
	barangay TEXT NOT NULL,
	contact int NOT NULL,
	violation TEXT NOT NULL,
	penalty TEXT NOT NULL,
	total_penalty INTEGER NOT NULL,
	date DATE DEFAULT(date('now')),
	status TEXT NOT NULL
		
);

DROP TABLE IF EXISTS logs;

CREATE TABLE logs(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	action TEXT NOT NULL,
	address TEXT NOT NULL,
	date TIMESTAMP DATE DEFAULT(datetime('now','localtime'))

);

DROP TABLE IF EXISTS municipal_logs;

CREATE TABLE municipal_logs(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	action TEXT NOT NULL,
	address TEXT NOT NULL,
	date TIMESTAMP DATE DEFAULT(datetime('now','localtime'))

);


DROP TABLE IF EXISTS archive;

CREATE TABLE archive(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	last_name TEXT NOT NULL,
	first_name TEXT NOT NULL,
	middle_name TEXT NOT NULL,
	house_number TEXT NOT NULL,
	street TEXT NOT NULL,
	barangay TEXT NOT NULL,
	contact int NOT NULL,
	violation TEXT NOT NULL,
	penalty TEXT NOT NULL,
	total_penalty INTEGER NOT NULL,
	date TEXT NOT NULL,
	status TEXT NOT NULL	

);

DROP TABLE IF EXISTS image;

CREATE TABLE image(
	pid INTEGER PRIMARY KEY AUTOINCREMENT,
	ima TEXT,
	name TEXT DEFAULT NULL
);

DROP TABLE IF EXISTS hi;

CREATE TABLE hi(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	password TEXT DEFAULT NULL
);

