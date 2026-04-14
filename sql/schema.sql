PRAGMA foreign_keys = ON;

-- =========================
-- CLUBS
-- =========================
CREATE TABLE clubs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    city TEXT,
    founded_year INTEGER
);

-- =========================
-- PLAYERS
-- =========================
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    nationality TEXT NOT NULL,
    position TEXT NOT NULL CHECK(position IN ('GK','DF','MF','FW')),
    number INTEGER NOT NULL CHECK(number BETWEEN 1 AND 99),
    status TEXT NOT NULL DEFAULT 'active',
    club_id INTEGER NOT NULL,
    FOREIGN KEY (club_id) REFERENCES clubs(id)
);

-- =========================
-- TRANSFERS
-- =========================
CREATE TABLE transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    from_club_id INTEGER,
    to_club_id INTEGER,
    transfer_date DATE,
    fee REAL,
    note TEXT,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (from_club_id) REFERENCES clubs(id),
    FOREIGN KEY (to_club_id) REFERENCES clubs(id)
);

-- =========================
-- LEAGUES
-- =========================
CREATE TABLE leagues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    season TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, season)
);


-- =========================
-- LEAGUE TEAMS
-- =========================
CREATE TABLE league_teams (
    league_id INTEGER,
    club_id INTEGER,
    joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (league_id, club_id),
    FOREIGN KEY (league_id) REFERENCES leagues(id),
    FOREIGN KEY (club_id) REFERENCES clubs(id)
);


-- =========================
-- MATCHES
-- =========================
CREATE TABLE matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER,
    round_no INTEGER NOT NULL,
    home_club_id INTEGER,
    away_club_id INTEGER,
    match_date DATE,
    home_goals INTEGER DEFAULT NULL,
    away_goals INTEGER DEFAULT NULL,
    FOREIGN KEY (league_id) REFERENCES leagues(id),
    FOREIGN KEY (home_club_id) REFERENCES clubs(id),
    FOREIGN KEY (away_club_id) REFERENCES clubs(id)
);


-- =========================
-- GOALS
-- =========================
CREATE TABLE goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    player_id INTEGER,
    minute INTEGER,
    FOREIGN KEY (match_id) REFERENCES matches(id),
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- =========================
-- CARDS
-- =========================
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    player_id INTEGER,
    card_type TEXT CHECK(card_type IN ('yellow','red')),
    minute INTEGER,
    FOREIGN KEY (match_id) REFERENCES matches(id),
    FOREIGN KEY (player_id) REFERENCES players(id)
);


-- =========================
-- INSERTS
-- =========================

-- CLUBS (10)
INSERT INTO clubs (name, city, founded_year) VALUES
('Левски София', 'София', 1914),
('ЦСКА София', 'София', 1948),
('Лудогорец', 'Разград', 2001),
('Ботев Пловдив', 'Пловдив', 1912),
('Берое', 'Стара Загора', 1916),
('Черно море', 'Варна', 1913),
('Славия', 'София', 1913),
('Арда', 'Кърджали', 1924),
('Локомотив Пловдив', 'Пловдив', 1926),
('Пирин Благоевград', 'Благоевград', 1922);


-- PLAYERS (10 x 11)

-- 1. ЛЕВСКИ
INSERT INTO players VALUES
(NULL,'Пламен Андреев','2004-09-15','България','GK',1,'active',1),
(NULL,'Жереми Петрис','1997-02-24','Франция','DF',2,'active',1),
(NULL,'Хосе Кордоба','2001-01-15','Панама','DF',3,'active',1),
(NULL,'Ноа Сонко Сундберг','1996-06-06','Гамбия','DF',4,'active',1),
(NULL,'Цунами','1996-01-14','Бразилия','DF',5,'active',1),
(NULL,'Андриан Краев','1999-02-14','България','MF',6,'active',1),
(NULL,'Ивелин Попов','1987-10-26','България','MF',10,'active',1),
(NULL,'Роналдо','2000-05-28','Бразилия','MF',7,'active',1),
(NULL,'Уелтон','1997-08-06','Бразилия','FW',11,'active',1),
(NULL,'Рикардиньо','2001-03-05','Бразилия','FW',9,'active',1),
(NULL,'Марин Петков','2003-10-02','България','FW',17,'active',1);

-- 2. ЦСКА
INSERT INTO players VALUES
(NULL,'Густаво Бусато','1990-08-23','Бразилия','GK',1,'active',2),
(NULL,'Иван Турицов','1999-07-18','България','DF',19,'active',2),
(NULL,'Юрген Матей','1993-04-28','Нидерландия','DF',4,'active',2),
(NULL,'Мено Кох','1994-07-02','Нидерландия','DF',5,'active',2),
(NULL,'Брадли де Нойер','1997-11-29','Нидерландия','DF',3,'active',2),
(NULL,'Амос Юга','1992-12-08','ЦАР','MF',6,'active',2),
(NULL,'Тобиас Хайнц','1998-01-13','Норвегия','MF',8,'active',2),
(NULL,'Джонатан Линдсет','1996-02-25','Норвегия','MF',7,'active',2),
(NULL,'Дюкенс Назон','1994-04-07','Хаити','FW',9,'active',2),
(NULL,'Матиас Фаетон','2000-01-08','Гваделупа','FW',11,'active',2),
(NULL,'Данило Асприля','1989-01-25','Колумбия','FW',10,'active',2);

-- 3. ЛУДОГОРЕЦ
INSERT INTO players VALUES
(NULL,'Серхио Падт','1990-06-06','Нидерландия','GK',1,'active',3),
(NULL,'Сисиньо','1988-04-23','Бразилия','DF',2,'active',3),
(NULL,'Оливие Вердон','1995-10-05','Бенин','DF',24,'active',3),
(NULL,'Антон Недялков','1993-04-30','България','DF',3,'active',3),
(NULL,'Ноа Сон','1997-08-10','Франция','DF',5,'active',3),
(NULL,'Якуб Пьотровски','1997-10-04','Полша','MF',6,'active',3),
(NULL,'Доминик Янков','2000-07-28','България','MF',8,'active',3),
(NULL,'Каули Оливейра','1995-11-15','Бразилия','MF',10,'active',3),
(NULL,'Кирил Десподов','1996-11-11','България','FW',7,'active',3),
(NULL,'Бернард Текпетей','1997-10-23','Гана','FW',37,'active',3),
(NULL,'Руан Круз','2001-05-20','Бразилия','FW',9,'active',3);

-- 4. БОТЕВ ПЛОВДИВ
INSERT INTO players VALUES
(NULL,'Даниел Наумов','1998-03-29','България','GK',1,'active',4),
(NULL,'Йонас Там','1999-02-15','Естония','DF',2,'active',4),
(NULL,'Антоан Бароан','2000-06-14','Франция','DF',3,'active',4),
(NULL,'Па Конате','1994-04-25','Швеция','DF',4,'active',4),
(NULL,'Самуел Супрайен','1989-12-07','Франция','DF',5,'active',4),
(NULL,'Тодор Неделев','1993-02-07','България','MF',8,'active',4),
(NULL,'Джеймс Етоо','2001-11-19','Камерун','MF',6,'active',4),
(NULL,'Антонио Перера','1997-03-12','Португалия','MF',7,'active',4),
(NULL,'Уме Емануел','2003-03-05','Нигерия','FW',9,'active',4),
(NULL,'Анвар Ел Гази','1995-05-03','Нидерландия','FW',10,'active',4),
(NULL,'Николай Минков','1997-09-13','България','FW',11,'active',4);

-- 5. БЕРОЕ
INSERT INTO players VALUES
(NULL,'Георги Аргилашки','1991-06-15','България','GK',1,'active',5),
(NULL,'Крум Стоянов','1991-08-24','България','DF',2,'active',5),
(NULL,'Симеон Мечев','1990-03-16','България','DF',3,'active',5),
(NULL,'Васил Панайотов','1990-07-16','България','DF',4,'active',5),
(NULL,'Александър Цветков','1990-08-31','България','DF',5,'active',5),
(NULL,'Илиян Стефанов','1998-12-28','България','MF',6,'active',5),
(NULL,'Радослав Цонев','1995-04-29','България','MF',7,'active',5),
(NULL,'Стефан Велев','1989-05-12','България','MF',8,'active',5),
(NULL,'Винисиус Белоти','1998-02-02','Бразилия','FW',9,'active',5),
(NULL,'Абубакар Тунгара','1994-07-03','Мали','FW',10,'active',5),
(NULL,'Дамян Йорданов','2000-01-01','България','FW',11,'active',5);

-- 6. ЧЕРНО МОРЕ
INSERT INTO players VALUES
(NULL,'Иван Дюлгеров','1999-07-15','България','GK',1,'active',6),
(NULL,'Виктор Попов','2000-03-05','България','DF',2,'active',6),
(NULL,'Живко Атанасов','1991-02-03','България','DF',3,'active',6),
(NULL,'Даниел Димов','1989-01-21','България','DF',4,'active',6),
(NULL,'Цветомир Панов','1990-01-21','България','DF',5,'active',6),
(NULL,'Илиян Илиев','1999-12-24','България','MF',8,'active',6),
(NULL,'Васил Панайотов','1990-07-16','България','MF',6,'active',6),
(NULL,'Пабло Гарсия','2000-05-15','Испания','MF',7,'active',6),
(NULL,'Атанас Илиев','1994-10-09','България','FW',9,'active',6),
(NULL,'Исмаил Иса','1989-06-26','България','FW',10,'active',6),
(NULL,'Зе Гомеш','1999-02-10','Португалия','FW',11,'active',6);

-- 7. СЛАВИЯ
INSERT INTO players VALUES
(NULL,'Светослав Вуцов','2002-07-09','България','GK',1,'active',7),
(NULL,'Емил Мартинов','1992-03-15','България','DF',2,'active',7),
(NULL,'Венцислав Керчев','1997-03-08','България','DF',3,'active',7),
(NULL,'Кристиан Добрев','2001-01-10','България','DF',4,'active',7),
(NULL,'Мартин Георгиев','2001-02-15','България','DF',5,'active',7),
(NULL,'Ивайло Димитров','1989-11-21','България','MF',6,'active',7),
(NULL,'Галин Иванов','1988-04-15','България','MF',7,'active',7),
(NULL,'Ерол Дост','1999-06-10','Турция','MF',8,'active',7),
(NULL,'Владимир Николов','2001-06-05','България','FW',9,'active',7),
(NULL,'Ахмед Ахмедов','1995-03-04','България','FW',10,'active',7),
(NULL,'Кристиан Стоянов','2003-01-01','България','FW',11,'active',7);

-- 8. АРДА
INSERT INTO players VALUES
(NULL,'Анатоли Господинов','1994-04-21','България','GK',1,'active',8),
(NULL,'Иван Коконов','1991-03-24','България','DF',2,'active',8),
(NULL,'Пламен Крачунов','1989-08-12','България','DF',3,'active',8),
(NULL,'Милен Стоев','1998-01-01','България','DF',4,'active',8),
(NULL,'Лъчезар Котев','1998-02-15','България','DF',5,'active',8),
(NULL,'Светослав Ковачев','1998-03-14','България','MF',6,'active',8),
(NULL,'Радослав Цонев','1995-04-29','България','MF',7,'active',8),
(NULL,'Илия Юруков','2000-01-01','България','MF',8,'active',8),
(NULL,'Станислав Иванов','1999-04-16','България','FW',9,'active',8),
(NULL,'Преслав Боруков','2000-01-01','България','FW',10,'active',8),
(NULL,'Тонислав Йорданов','1998-11-09','България','FW',11,'active',8);

-- 9. ЛОКОМОТИВ ПЛОВДИВ
INSERT INTO players VALUES
(NULL,'Динко Хоркаш','1999-03-10','Хърватия','GK',1,'active',9),
(NULL,'Петър Витанов','1995-02-10','България','DF',2,'active',9),
(NULL,'Кристиан Гомис','1998-08-10','Сенегал','DF',3,'active',9),
(NULL,'Мартин Паскалев','2001-01-01','България','DF',4,'active',9),
(NULL,'Ангел Лясков','1998-03-05','България','DF',5,'active',9),
(NULL,'Димитър Илиев','1988-07-25','България','MF',7,'active',9),
(NULL,'Парвиз Умарбаев','1994-11-01','Таджикистан','MF',6,'active',9),
(NULL,'Бабакар Дион','1997-01-01','Сенегал','MF',8,'active',9),
(NULL,'Джовани','1996-05-05','Бразилия','FW',9,'active',9),
(NULL,'Евандро','1996-07-19','Бразилия','FW',10,'active',9),
(NULL,'Бирсент Карагарен','1992-12-06','България','FW',11,'active',9);

-- 10. ПИРИН
INSERT INTO players VALUES
(NULL,'Максим Ковальов','1998-05-05','Украйна','GK',1,'active',10),
(NULL,'Александър Дюлгеров','1990-07-15','България','DF',2,'active',10),
(NULL,'Юлиан Попев','1990-01-01','България','DF',3,'active',10),
(NULL,'Николай Бодуров','1986-05-30','България','DF',4,'active',10),
(NULL,'Станислав Манолев','1985-12-16','България','DF',5,'active',10),
(NULL,'Красимир Станоев','1988-01-01','България','MF',6,'active',10),
(NULL,'Аймен Суда','1997-02-01','Алжир','MF',7,'active',10),
(NULL,'Александър Тодоров','2000-01-01','България','MF',8,'active',10),
(NULL,'Станислав Костов','1991-09-15','България','FW',9,'active',10),
(NULL,'Преслав Йорданов','1989-06-27','България','FW',10,'active',10),
(NULL,'Мохамед Брахими','1998-01-01','Алжир','FW',11,'active',10);


-- LEAGUE
INSERT INTO leagues (name, season) VALUES
('Първа лига', '2025/2026');


-- LEAGUE TEAMS (10)
INSERT INTO league_teams (league_id, club_id) VALUES
(1,1),(1,2),(1,3),(1,4),(1,5),
(1,6),(1,7),(1,8),(1,9),(1,10);


-- MATCHES (5)
INSERT INTO matches (league_id, round_no, home_club_id, away_club_id, match_date, home_goals, away_goals) VALUES
(1, 1, 1, 2, '2025-09-01', 2, 1),
(1, 1, 3, 4, '2025-09-02', 3, 0),
(1, 1, 5, 6, '2025-09-03', 1, 1),
(1, 1, 7, 8, '2025-09-04', 0, 2),
(1, 1, 9, 10, '2025-09-05', 4, 2);


-- GOALS
INSERT INTO goals (match_id, player_id, minute) VALUES
(1, 1, 23),
(1, 12, 55),
(1, 3, 70),
(2, 5, 12),
(2, 6, 48),
(2, 13, 75),
(3, 9, 33),
(3, 10, 60),
(4, 15, 22),
(4, 15, 80),
(5, 16, 10),
(5, 16, 40),
(5, 16, 65),
(5, 17, 78);


-- CARDS
INSERT INTO cards (match_id, player_id, card_type, minute) VALUES
(1, 2, 'yellow', 30),
(2, 7, 'yellow', 50),
(3, 9, 'red', 88),
(4, 15, 'yellow', 15),
(5, 16, 'yellow', 44);


-- TRANSFERS
INSERT INTO transfers (player_id, from_club_id, to_club_id, transfer_date, fee) VALUES
(12, 1, 2, '2025-07-01', 500000),
(15, 8, 3, '2025-07-10', 750000),
(17, 10, 5, '2025-06-20', 300000);
