CREATE TABLE processed(
	pk integer auto increment primary key,
	serverid integer not null,
	filename blob not null,
	datetime string not null);

CREATE TABLE results(
	pk integer auto increment primary key,
	serverid integer not null,
	category string not null,
	catNumber integer not null,
	datetime string not null,
	value int not null);

