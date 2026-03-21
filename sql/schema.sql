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
    season TEXT NOT NULL
);

-- =========================
-- LEAGUE TEAMS
-- =========================
CREATE TABLE league_teams (
    league_id INTEGER,
    club_id INTEGER,
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
    home_club_id INTEGER,
    away_club_id INTEGER,
    match_date DATE,
    home_goals INTEGER DEFAULT 0,
    away_goals INTEGER DEFAULT 0,
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


-- PLAYERS (20)
INSERT INTO players (full_name, birth_date, nationality, position, number, status, club_id) VALUES
('Иван Петров', '1995-05-12', 'България', 'FW', 9, 'active', 1),
('Георги Иванов', '1997-03-18', 'България', 'MF', 8, 'active', 1),
('Николай Стоянов', '1994-07-22', 'България', 'DF', 5, 'active', 2),
('Димитър Костов', '1992-11-02', 'България', 'GK', 1, 'active', 2),
('Марселино', '1990-01-10', 'Бразилия', 'FW', 11, 'active', 3),
('Кирил Десподов', '1996-11-11', 'България', 'FW', 7, 'active', 3),
('Тодор Неделев', '1993-02-07', 'България', 'MF', 8, 'active', 4),
('Мартин Камбуров', '1980-10-13', 'България', 'FW', 9, 'active', 4),
('Стефан Велев', '1989-05-12', 'България', 'MF', 6, 'active', 5),
('Илиян Илиев', '1999-12-24', 'България', 'MF', 10, 'active', 6),
('Владимир Николов', '2001-06-05', 'България', 'FW', 19, 'active', 7),
('Радослав Цонев', '1995-04-29', 'България', 'MF', 17, 'active', 1),
('Антон Недялков', '1993-04-30', 'България', 'DF', 3, 'active', 3),
('Петър Витанов', '1995-02-10', 'България', 'MF', 21, 'active', 2),
('Станислав Иванов', '1999-04-16', 'България', 'FW', 99, 'active', 8),
('Иван Бандаловски', '1986-11-19', 'България', 'DF', 2, 'active', 9),
('Даниел Наумов', '1998-03-29', 'България', 'GK', 12, 'active', 10),
('Александър Василев', '1995-04-27', 'България', 'DF', 4, 'active', 5),
('Борис Тютюков', '1998-03-14', 'България', 'FW', 18, 'active', 6),
('Михаил Александров', '1989-08-11', 'България', 'FW', 77, 'active', 7);


-- LEAGUE
INSERT INTO leagues (name, season) VALUES
('Първа лига', '2025/2026');


-- LEAGUE TEAMS (10)
INSERT INTO league_teams VALUES
(1,1),(1,2),(1,3),(1,4),(1,5),
(1,6),(1,7),(1,8),(1,9),(1,10);


-- MATCHES (5)
INSERT INTO matches (league_id, home_club_id, away_club_id, match_date, home_goals, away_goals) VALUES
(1, 1, 2, '2025-09-01', 2, 1),
(1, 3, 4, '2025-09-02', 3, 0),
(1, 5, 6, '2025-09-03', 1, 1),
(1, 7, 8, '2025-09-04', 0, 2),
(1, 9, 10, '2025-09-05', 4, 2);


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
