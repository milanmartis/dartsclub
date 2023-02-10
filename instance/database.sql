BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER NOT NULL,
	"email"	VARCHAR(150),
	"password"	VARCHAR(150),
	"first_name"	VARCHAR(150),
	"orderz"	INTEGER,
	PRIMARY KEY("id"),
	UNIQUE("email")
);
CREATE TABLE IF NOT EXISTS "season" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(300),
	"season_from"	DATETIME,
	"season_to"	DATETIME,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user_season" (
	"user_id"	INTEGER,
	"season_id"	INTEGER,
	"season_first_date"	DATETIME,
	"orderz"	INTEGER,
	FOREIGN KEY("season_id") REFERENCES "season"("id"),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "note" (
	"id"	INTEGER NOT NULL,
	"data"	VARCHAR(10000),
	"date_time"	DATETIME,
	"user_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "round" (
	"id"	INTEGER NOT NULL,
	"season_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("season_id") REFERENCES "season"("id")
);
CREATE TABLE IF NOT EXISTS "groupz" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(300),
	"shorts"	TEXT,
	"season_id"	INTEGER,
	"round_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("season_id") REFERENCES "season"("id"),
	FOREIGN KEY("round_id") REFERENCES "round"("id")
);
CREATE TABLE IF NOT EXISTS "duel" (
	"id"	INTEGER NOT NULL,
	"notice"	VARCHAR(10000),
	"date_duel"	DATETIME,
	"season_id"	INTEGER,
	"round_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("round_id") REFERENCES "round"("id"),
	FOREIGN KEY("season_id") REFERENCES "season"("id")
);
CREATE TABLE IF NOT EXISTS "user_duel" (
	"user_id"	INTEGER,
	"duel_id"	INTEGER,
	"result"	INTEGER,
	"against"	INTEGER,
	"points"	INTEGER,
	"checked"	INTEGER,
	"notez"	INTEGER,
	"addons"	INTEGER,
	FOREIGN KEY("user_id") REFERENCES "user"("id"),
	FOREIGN KEY("duel_id") REFERENCES "duel"("id")
);
CREATE TABLE IF NOT EXISTS "user_group" (
	"user_id"	INTEGER,
	"groupz_id"	INTEGER,
	"season_id"	INTEGER,
	"round_id"	INTEGER,
	FOREIGN KEY("season_id") REFERENCES "season"("id"),
	FOREIGN KEY("groupz_id") REFERENCES "groupz"("id"),
	FOREIGN KEY("round_id") REFERENCES "round"("id"),
	FOREIGN KEY("user_id") REFERENCES "user"("id")
);
CREATE TABLE IF NOT EXISTS "openhour" (
	"id"	INTEGER NOT NULL,
	"notice"	VARCHAR(500),
	"oh_from"	DATETIME,
	"oh_to"	DATETIME,
	"duel_id"	INTEGER,
	PRIMARY KEY("id"),
	FOREIGN KEY("duel_id") REFERENCES "duel"("id")
);
INSERT INTO "user" VALUES (1,'hery@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','hery',3);
INSERT INTO "user" VALUES (2,'andy@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','andy',1);
INSERT INTO "user" VALUES (3,'imre@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','imre',2);
INSERT INTO "user" VALUES (4,'juso@dartsclub.sk','sha256$Fbeh01RJg948Kphg$4ac10931c021f725856a74c8783e13dcdfef727373f682b4318bd4fd3b9583d1','juso',6);
INSERT INTO "user" VALUES (5,'jardo@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','jardo',11);
INSERT INTO "user" VALUES (6,'matis@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','matis',12);
INSERT INTO "user" VALUES (7,'peto@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','peto',7);
INSERT INTO "user" VALUES (8,'demo@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','demo',4);
INSERT INTO "user" VALUES (9,'h1@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','h1',10);
INSERT INTO "user" VALUES (10,'magnum@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','magnum',21);
INSERT INTO "user" VALUES (11,'foxo@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','foxo',16);
INSERT INTO "user" VALUES (12,'edo@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','edo',13);
INSERT INTO "user" VALUES (13,'h2@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','h2',15);
INSERT INTO "user" VALUES (14,'tomas_v@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','tomáš_v',14);
INSERT INTO "user" VALUES (15,'majo@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','majo',8);
INSERT INTO "user" VALUES (16,'tomas@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','tomáš',14);
INSERT INTO "user" VALUES (17,'pista@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','pišta',22);
INSERT INTO "user" VALUES (18,'samo_n@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','samo_n',9);
INSERT INTO "user" VALUES (19,'marek@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','marek',17);
INSERT INTO "user" VALUES (20,'h3@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','h3',20);
INSERT INTO "user" VALUES (21,'milanmartis@gmail.com','sha256$Abu3aAAp0hYha4fJ$8ea439c4796c6d9b4d02f1c252d4ee3974f6580c7cc03434ec8aa248585535a8','milan',0);
INSERT INTO "user" VALUES (22,'petko@dartsclub.sk','sha256$Abu3aAAp0hYha4fJ$8ea439c4796c6d9b4d02f1c252d4ee3974f6580c7cc03434ec8aa248585535a8','Peter Grič',0);
INSERT INTO "user" VALUES (23,'konik_r@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','Koník R',18);
INSERT INTO "user" VALUES (24,'gric_j@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','Grič J',19);
INSERT INTO "user" VALUES (25,'juhasz_a@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','Juhász A',23);
INSERT INTO "user" VALUES (26,'drahos@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','Drahoš',24);
INSERT INTO "user" VALUES (27,'h4@dartsclub.sk','sha256$bAP8swh72ZFzw2Wo$997746eff2d7c50e774dede206c43848fa8f8e1714227d2969147156d001785d','h4',25);
INSERT INTO "season" VALUES (1,'First Season','2023-01-16 12:27:26','2023-01-16 12:27:26');
INSERT INTO "user_season" VALUES (1,1,'2023-01-16 13:29:42',3);
INSERT INTO "user_season" VALUES (2,1,'2023-01-16 13:29:42',1);
INSERT INTO "user_season" VALUES (3,1,'2023-01-16 13:29:42',2);
INSERT INTO "user_season" VALUES (4,1,'2023-01-16 13:29:42',6);
INSERT INTO "user_season" VALUES (5,1,'2023-01-16 13:29:42',11);
INSERT INTO "user_season" VALUES (6,1,'2023-01-16 13:29:42',12);
INSERT INTO "user_season" VALUES (7,1,'2023-01-16 13:29:42',7);
INSERT INTO "user_season" VALUES (8,1,'2023-01-16 13:29:42',4);
INSERT INTO "user_season" VALUES (9,1,'2023-01-16 13:29:42',10);
INSERT INTO "user_season" VALUES (10,1,'2023-01-16 13:29:42',21);
INSERT INTO "user_season" VALUES (11,1,'2023-01-16 13:29:42',16);
INSERT INTO "user_season" VALUES (12,1,'2023-01-16 13:29:42',13);
INSERT INTO "user_season" VALUES (13,1,'2023-01-16 13:29:42',15);
INSERT INTO "user_season" VALUES (14,1,'2023-01-16 13:29:42',5);
INSERT INTO "user_season" VALUES (15,1,'2023-01-16 13:29:42',8);
INSERT INTO "user_season" VALUES (16,1,'2023-01-16 13:29:42',14);
INSERT INTO "user_season" VALUES (17,1,'2023-01-16 13:29:42',22);
INSERT INTO "user_season" VALUES (18,1,'2023-01-16 13:29:42',9);
INSERT INTO "user_season" VALUES (19,1,'2023-01-16 13:29:42',17);
INSERT INTO "user_season" VALUES (20,1,'2023-01-16 13:29:42',20);
INSERT INTO "user_season" VALUES (23,1,'2023-01-16 13:29:42',18);
INSERT INTO "user_season" VALUES (24,1,'2023-01-16 13:29:42',19);
INSERT INTO "user_season" VALUES (25,1,'2023-01-16 13:29:42',23);
INSERT INTO "user_season" VALUES (26,1,'2023-01-16 13:29:42',24);
INSERT INTO "user_season" VALUES (27,1,'2023-01-16 13:29:42',25);
INSERT INTO "round" VALUES (1,1);
INSERT INTO "round" VALUES (2,1);
INSERT INTO "groupz" VALUES (1,'Group 1','A',1,1);
INSERT INTO "groupz" VALUES (2,'Group 2','B1',1,1);
INSERT INTO "groupz" VALUES (3,'Group 3','B2',1,1);
INSERT INTO "groupz" VALUES (7,'Group 4','C1',1,1);
INSERT INTO "groupz" VALUES (8,'Group 1','A',1,2);
INSERT INTO "groupz" VALUES (9,'Group 2','B1',1,2);
INSERT INTO "groupz" VALUES (10,'Group 3','B2',1,2);
INSERT INTO "groupz" VALUES (11,'Group 4','C1',1,2);
INSERT INTO "groupz" VALUES (12,'Group 5','C2',1,2);
INSERT INTO "duel" VALUES (1,NULL,'2023-01-16 14:30:46.740645',1,1);
INSERT INTO "duel" VALUES (2,NULL,'2023-01-16 14:30:46.772777',1,1);
INSERT INTO "duel" VALUES (3,NULL,'2023-01-16 14:30:46.803357',1,1);
INSERT INTO "duel" VALUES (4,NULL,'2023-01-16 14:30:46.834297',1,1);
INSERT INTO "duel" VALUES (5,NULL,'2023-01-16 14:30:46.863976',1,1);
INSERT INTO "duel" VALUES (6,NULL,'2023-01-16 14:30:46.894540',1,1);
INSERT INTO "duel" VALUES (7,NULL,'2023-01-16 14:30:46.925370',1,1);
INSERT INTO "duel" VALUES (8,NULL,'2023-01-16 14:30:46.955010',1,1);
INSERT INTO "duel" VALUES (9,NULL,'2023-01-16 14:30:46.985339',1,1);
INSERT INTO "duel" VALUES (10,NULL,'2023-01-16 14:30:47.017274',1,1);
INSERT INTO "duel" VALUES (11,NULL,'2023-01-16 14:30:47.065998',1,1);
INSERT INTO "duel" VALUES (12,NULL,'2023-01-16 14:30:47.096026',1,1);
INSERT INTO "duel" VALUES (13,NULL,'2023-01-16 14:30:47.127359',1,1);
INSERT INTO "duel" VALUES (14,NULL,'2023-01-16 14:30:47.159391',1,1);
INSERT INTO "duel" VALUES (15,NULL,'2023-01-16 14:30:47.190563',1,1);
INSERT INTO "duel" VALUES (16,NULL,'2023-01-16 14:30:47.220925',1,1);
INSERT INTO "duel" VALUES (17,NULL,'2023-01-16 14:30:47.253042',1,1);
INSERT INTO "duel" VALUES (18,NULL,'2023-01-16 14:30:47.283771',1,1);
INSERT INTO "duel" VALUES (19,NULL,'2023-01-16 14:30:47.314388',1,1);
INSERT INTO "duel" VALUES (20,NULL,'2023-01-16 14:30:47.346136',1,1);
INSERT INTO "duel" VALUES (21,NULL,'2023-01-16 14:30:47.401137',1,1);
INSERT INTO "duel" VALUES (22,NULL,'2023-01-16 14:30:47.433135',1,1);
INSERT INTO "duel" VALUES (23,NULL,'2023-01-16 14:30:47.464161',1,1);
INSERT INTO "duel" VALUES (24,NULL,'2023-01-16 14:30:47.494132',1,1);
INSERT INTO "duel" VALUES (25,NULL,'2023-01-16 14:30:47.524584',1,1);
INSERT INTO "duel" VALUES (26,NULL,'2023-01-16 14:30:47.555198',1,1);
INSERT INTO "duel" VALUES (27,NULL,'2023-01-16 14:30:47.586699',1,1);
INSERT INTO "duel" VALUES (28,NULL,'2023-01-16 14:30:47.617982',1,1);
INSERT INTO "duel" VALUES (29,NULL,'2023-01-16 14:30:47.653389',1,1);
INSERT INTO "duel" VALUES (30,NULL,'2023-01-16 14:30:47.686392',1,1);
INSERT INTO "duel" VALUES (91,NULL,'2023-01-17 22:40:18.501763',1,1);
INSERT INTO "duel" VALUES (92,NULL,'2023-01-17 22:40:18.532494',1,1);
INSERT INTO "duel" VALUES (93,NULL,'2023-01-17 22:40:18.563069',1,1);
INSERT INTO "duel" VALUES (94,NULL,'2023-01-17 22:40:18.594590',1,1);
INSERT INTO "duel" VALUES (95,NULL,'2023-01-17 22:40:18.625683',1,1);
INSERT INTO "duel" VALUES (96,NULL,'2023-01-17 22:40:18.655877',1,1);
INSERT INTO "duel" VALUES (97,NULL,'2023-01-17 22:40:18.688264',1,1);
INSERT INTO "duel" VALUES (98,NULL,'2023-01-17 22:40:18.719579',1,1);
INSERT INTO "duel" VALUES (99,NULL,'2023-01-17 22:40:18.749740',1,1);
INSERT INTO "duel" VALUES (100,NULL,'2023-01-17 22:40:18.780830',1,1);
INSERT INTO "duel" VALUES (101,NULL,'2023-02-01 10:29:59.136330',1,2);
INSERT INTO "duel" VALUES (102,NULL,'2023-02-01 10:29:59.171016',1,2);
INSERT INTO "duel" VALUES (103,NULL,'2023-02-01 10:29:59.202818',1,2);
INSERT INTO "duel" VALUES (104,NULL,'2023-02-01 10:29:59.234764',1,2);
INSERT INTO "duel" VALUES (105,NULL,'2023-02-01 10:29:59.265650',1,2);
INSERT INTO "duel" VALUES (106,NULL,'2023-02-01 10:29:59.296434',1,2);
INSERT INTO "duel" VALUES (107,NULL,'2023-02-01 10:29:59.327557',1,2);
INSERT INTO "duel" VALUES (108,NULL,'2023-02-01 10:29:59.358995',1,2);
INSERT INTO "duel" VALUES (109,NULL,'2023-02-01 10:29:59.389783',1,2);
INSERT INTO "duel" VALUES (110,NULL,'2023-02-01 10:29:59.421065',1,2);
INSERT INTO "duel" VALUES (111,NULL,'2023-02-01 10:29:59.470132',1,2);
INSERT INTO "duel" VALUES (112,NULL,'2023-02-01 10:29:59.500644',1,2);
INSERT INTO "duel" VALUES (113,NULL,'2023-02-01 10:29:59.531807',1,2);
INSERT INTO "duel" VALUES (114,NULL,'2023-02-01 10:29:59.562362',1,2);
INSERT INTO "duel" VALUES (115,NULL,'2023-02-01 10:29:59.594399',1,2);
INSERT INTO "duel" VALUES (116,NULL,'2023-02-01 10:29:59.625499',1,2);
INSERT INTO "duel" VALUES (117,NULL,'2023-02-01 10:29:59.656345',1,2);
INSERT INTO "duel" VALUES (118,NULL,'2023-02-01 10:29:59.686677',1,2);
INSERT INTO "duel" VALUES (119,NULL,'2023-02-01 10:29:59.717229',1,2);
INSERT INTO "duel" VALUES (120,NULL,'2023-02-01 10:29:59.748000',1,2);
INSERT INTO "duel" VALUES (121,NULL,'2023-02-01 10:29:59.807062',1,2);
INSERT INTO "duel" VALUES (122,NULL,'2023-02-01 10:29:59.836786',1,2);
INSERT INTO "duel" VALUES (123,NULL,'2023-02-01 10:29:59.870242',1,2);
INSERT INTO "duel" VALUES (124,NULL,'2023-02-01 10:29:59.911117',1,2);
INSERT INTO "duel" VALUES (125,NULL,'2023-02-01 10:29:59.941493',1,2);
INSERT INTO "duel" VALUES (126,NULL,'2023-02-01 10:29:59.971422',1,2);
INSERT INTO "duel" VALUES (127,NULL,'2023-02-01 10:30:00.001020',1,2);
INSERT INTO "duel" VALUES (128,NULL,'2023-02-01 10:30:00.032692',1,2);
INSERT INTO "duel" VALUES (129,NULL,'2023-02-01 10:30:00.062737',1,2);
INSERT INTO "duel" VALUES (130,NULL,'2023-02-01 10:30:00.092243',1,2);
INSERT INTO "duel" VALUES (131,NULL,'2023-02-01 10:30:00.154135',1,2);
INSERT INTO "duel" VALUES (132,NULL,'2023-02-01 10:30:00.183736',1,2);
INSERT INTO "duel" VALUES (133,NULL,'2023-02-01 10:30:00.215365',1,2);
INSERT INTO "duel" VALUES (134,NULL,'2023-02-01 10:30:00.245843',1,2);
INSERT INTO "duel" VALUES (135,NULL,'2023-02-01 10:30:00.277616',1,2);
INSERT INTO "duel" VALUES (136,NULL,'2023-02-01 10:30:00.315089',1,2);
INSERT INTO "duel" VALUES (137,NULL,'2023-02-01 10:30:00.350074',1,2);
INSERT INTO "duel" VALUES (138,NULL,'2023-02-01 10:30:00.380672',1,2);
INSERT INTO "duel" VALUES (139,NULL,'2023-02-01 10:30:00.409965',1,2);
INSERT INTO "duel" VALUES (140,NULL,'2023-02-01 10:30:00.441856',1,2);
INSERT INTO "duel" VALUES (141,NULL,'2023-02-01 10:30:00.490177',1,2);
INSERT INTO "duel" VALUES (142,NULL,'2023-02-01 10:30:00.520417',1,2);
INSERT INTO "duel" VALUES (143,NULL,'2023-02-01 10:30:00.549639',1,2);
INSERT INTO "duel" VALUES (144,NULL,'2023-02-01 10:30:00.580775',1,2);
INSERT INTO "duel" VALUES (145,NULL,'2023-02-01 10:30:00.612173',1,2);
INSERT INTO "duel" VALUES (146,NULL,'2023-02-01 10:30:00.641545',1,2);
INSERT INTO "duel" VALUES (147,NULL,'2023-02-01 10:30:00.673688',1,2);
INSERT INTO "duel" VALUES (148,NULL,'2023-02-01 10:30:00.705664',1,2);
INSERT INTO "duel" VALUES (149,NULL,'2023-02-01 10:30:00.736577',1,2);
INSERT INTO "duel" VALUES (150,NULL,'2023-02-01 10:30:00.767839',1,2);
INSERT INTO "user_duel" VALUES (1,1,3,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (2,1,6,3,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (1,2,2,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (3,2,6,2,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (1,3,6,1,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (4,3,1,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (1,4,6,4,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (5,4,4,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (2,5,6,4,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (3,5,4,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (2,6,6,1,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (4,6,1,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (2,7,6,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (5,7,0,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (3,8,6,1,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (4,8,1,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (3,9,6,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (5,9,0,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (4,10,1,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (5,10,6,1,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (6,11,6,3,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (7,11,3,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (6,12,4,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (8,12,6,4,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (6,13,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (9,13,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (6,14,6,1,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (10,14,1,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (7,15,3,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (8,15,6,3,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (7,16,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (9,16,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (7,17,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (10,17,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (8,18,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (9,18,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (8,19,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (10,19,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (9,20,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (10,20,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (11,21,4,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (12,21,6,4,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (11,22,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (13,22,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (11,23,4,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (14,23,6,4,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (11,24,3,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (15,24,6,3,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (12,25,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (13,25,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (12,26,0,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (14,26,6,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (12,27,3,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (15,27,6,3,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (13,28,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (14,28,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (13,29,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (15,29,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (14,30,6,4,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (15,30,4,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (16,91,6,4,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (17,91,4,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (16,92,1,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (18,92,6,1,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (16,93,6,3,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (19,93,3,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (16,94,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (20,94,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (17,95,0,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (18,95,6,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (17,96,6,4,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (19,96,4,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (17,97,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (20,97,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (18,98,6,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (19,98,0,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (18,99,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (20,99,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (19,100,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (20,100,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (14,101,1,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (2,101,6,1,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (14,102,0,0,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (1,102,0,0,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (14,103,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (3,103,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (14,104,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (8,104,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (2,105,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (1,105,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (2,106,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (3,106,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (2,107,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (8,107,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (1,108,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (3,108,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (1,109,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (8,109,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (3,110,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (8,110,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (18,111,1,6,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (4,111,6,1,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (18,112,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (7,112,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (18,113,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (15,113,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (18,114,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (9,114,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (4,115,6,5,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (7,115,5,6,1,'false',NULL,1);
INSERT INTO "user_duel" VALUES (4,116,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (15,116,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (4,117,6,4,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (9,117,4,6,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (7,118,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (15,118,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (7,119,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (9,119,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (15,120,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (9,120,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (12,121,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (16,121,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (12,122,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (5,122,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (12,123,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (13,123,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (12,124,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (6,124,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (16,125,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (5,125,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (16,126,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (13,126,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (16,127,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (6,127,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (5,128,6,5,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (13,128,5,6,1,'true',NULL,1);
INSERT INTO "user_duel" VALUES (5,129,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (6,129,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (13,130,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (6,130,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (20,131,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (11,131,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (20,132,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (23,132,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (20,133,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (19,133,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (20,134,0,4,0,'true',NULL,1);
INSERT INTO "user_duel" VALUES (24,134,4,0,2,'true',NULL,1);
INSERT INTO "user_duel" VALUES (11,135,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (23,135,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (11,136,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (19,136,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (11,137,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (24,137,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (23,138,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (19,138,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (23,139,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (24,139,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (19,140,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (24,140,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (25,141,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (10,141,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (25,142,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (17,142,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (25,143,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (26,143,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (25,144,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (27,144,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (10,145,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (17,145,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (10,146,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (26,146,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (10,147,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (27,147,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (17,148,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (26,148,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (17,149,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (27,149,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (26,150,0,0,0,'false',NULL,1);
INSERT INTO "user_duel" VALUES (27,150,0,0,0,'false',NULL,1);
INSERT INTO "user_group" VALUES (1,1,1,1);
INSERT INTO "user_group" VALUES (2,1,1,1);
INSERT INTO "user_group" VALUES (3,1,1,1);
INSERT INTO "user_group" VALUES (4,1,1,1);
INSERT INTO "user_group" VALUES (5,1,1,1);
INSERT INTO "user_group" VALUES (6,2,1,1);
INSERT INTO "user_group" VALUES (7,2,1,1);
INSERT INTO "user_group" VALUES (8,2,1,1);
INSERT INTO "user_group" VALUES (9,2,1,1);
INSERT INTO "user_group" VALUES (10,2,1,1);
INSERT INTO "user_group" VALUES (11,3,1,1);
INSERT INTO "user_group" VALUES (12,3,1,1);
INSERT INTO "user_group" VALUES (13,3,1,1);
INSERT INTO "user_group" VALUES (14,3,1,1);
INSERT INTO "user_group" VALUES (15,3,1,1);
INSERT INTO "user_group" VALUES (16,7,1,1);
INSERT INTO "user_group" VALUES (17,7,1,1);
INSERT INTO "user_group" VALUES (18,7,1,1);
INSERT INTO "user_group" VALUES (19,7,1,1);
INSERT INTO "user_group" VALUES (20,7,1,1);
INSERT INTO "user_group" VALUES (2,8,1,2);
INSERT INTO "user_group" VALUES (3,8,1,2);
INSERT INTO "user_group" VALUES (1,8,1,2);
INSERT INTO "user_group" VALUES (8,8,1,2);
INSERT INTO "user_group" VALUES (14,8,1,2);
INSERT INTO "user_group" VALUES (4,9,1,2);
INSERT INTO "user_group" VALUES (7,9,1,2);
INSERT INTO "user_group" VALUES (15,9,1,2);
INSERT INTO "user_group" VALUES (18,9,1,2);
INSERT INTO "user_group" VALUES (9,9,1,2);
INSERT INTO "user_group" VALUES (5,10,1,2);
INSERT INTO "user_group" VALUES (6,10,1,2);
INSERT INTO "user_group" VALUES (12,10,1,2);
INSERT INTO "user_group" VALUES (16,10,1,2);
INSERT INTO "user_group" VALUES (13,10,1,2);
INSERT INTO "user_group" VALUES (11,11,1,2);
INSERT INTO "user_group" VALUES (19,11,1,2);
INSERT INTO "user_group" VALUES (23,11,1,2);
INSERT INTO "user_group" VALUES (24,11,1,2);
INSERT INTO "user_group" VALUES (20,11,1,2);
INSERT INTO "user_group" VALUES (10,12,1,2);
INSERT INTO "user_group" VALUES (17,12,1,2);
INSERT INTO "user_group" VALUES (25,12,1,2);
INSERT INTO "user_group" VALUES (26,12,1,2);
INSERT INTO "user_group" VALUES (27,12,1,2);
COMMIT;
