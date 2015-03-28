BEGIN TRANSACTION;
DROP TABLE IF EXISTS login_data;
DROP TABLE IF EXISTS users_data;
DROP TABLE IF EXISTS bikes_data;
DROP TABLE IF EXISTS app_data;
DROP TABLE IF EXISTS code_data;
DROP TABLE IF EXISTS access_data;
DROP TRIGGER IF EXISTS code_data_cleaner_update;
DROP TRIGGER IF EXISTS code_data_cleaner_insert;
CREATE TABLE login_data (login TEXT UNIQUE, password TEXT);
INSERT INTO "login_data" VALUES('lobzik','123123');
INSERT INTO "login_data" VALUES('spark','123123');
INSERT INTO "login_data" VALUES('spectre','123123');
INSERT INTO "login_data" VALUES('lalala','123123');
INSERT INTO "login_data" VALUES('kosyura','123123');
CREATE TABLE users_data (id INTEGER PRIMARY KEY, login TEXT UNIQUE, firstname TEXT, secondname TEXT, age INTEGER, city TEXT, email TEXT, like_bikes TEXT, my_bikes TEXT);
INSERT INTO "users_data" VALUES(1,'lobzik','Egor','Aslapov',21,'Moscow','egor.aslapov@mail.ru','3','3');
INSERT INTO "users_data" VALUES(2,'spark','Aydar','Nazmutdinov',21,'Moscow','darikspark@mail.ru','3','3');
INSERT INTO "users_data" VALUES(3,'spectre','Slava','Belous',20,'Moscow','v.belous@yandex.ru','2,4','2');
INSERT INTO "users_data" VALUES(4,'lalala','Lala','Lalalka',28,'Samara','lalala@gmail.com','1,3','3');
INSERT INTO "users_data" VALUES(5,'kosyura','Olya','Kosyura',22,'Moscow','kosyura@mail.ru','4,5','4');
CREATE TABLE bikes_data (id INTEGER PRIMARY KEY, firm TEXT, model TEXT, color TEXT, cost REAL, description TEXT);
INSERT INTO "bikes_data" VALUES(1,'Yamaha','YZF-R1M','Black',840290.0,'Engine type: 998cc, liquid-cooled inline 4 cylinder DOHC 16 valves; Transmission: 6-speed w/multi-plate slipper clutch');
INSERT INTO "bikes_data" VALUES(2,'Yamaha','YZ250F','Blue',430490.0,'Engine type: 249cc liquid-cooled DOHC 4-stroke; 4 titanium valves; Transmission: Constant-mesh 5-speed; multiplate wet clutch');
INSERT INTO "bikes_data" VALUES(3,'Yamaha','XT250','Black',200990.0,'Engine type: 249cc air-cooled, SOHC 4-stroke single; Transmission: 5-speed; multiple-disc wet clutch');
INSERT INTO "bikes_data" VALUES(4,'Kawasaki','Ninja H2R','Black',700490.0,'Engine type: Liquid-cooled, 4-stroke in-line four; Transmission: 6-speed, return, dog-ring');
INSERT INTO "bikes_data" VALUES(5,'Kawasaki','Z1000 ABS','Black',600190.0,'Engine type: Four-stroke, liquid-cooled, DOHC, Four valves per cylinder, inline-four; Transmission: Six-speed');
INSERT INTO "bikes_data" VALUES(6,'Honda','CB1100','Gray',300490.0,'Engine type: 1140cc air- and oil-cooled inline four-cylinder; Transmission: Six-speed');
CREATE TABLE app_data (client_id TEXT PRIMARY KEY, client_secret TEXT, login TEXT);
INSERT INTO "app_data" VALUES ('13321','123123123','lobzik');
CREATE TABLE code_data (login TEXT, client_id TEXT, code TEXT, expiration_time INTEGER, redirect_uri TEXT, PRIMARY KEY(login, client_id));
CREATE TABLE access_data (client_id TEXT, access_token TEXT UNIQUE, refresh_token TEXT UNIQUE, expiration_time INTEGER);
CREATE TRIGGER code_data_cleaner_update UPDATE ON code_data
BEGIN
	DELETE FROM code_data WHERE strftime('%s', 'now') >= expiration_time;
END;
CREATE TRIGGER code_data_cleaner_insert INSERT ON code_data
BEGIN
	DELETE FROM code_data WHERE strftime('%s', 'now') >= expiration_time;
END;
COMMIT;
