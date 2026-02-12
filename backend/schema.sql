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
    name TEXT NOT NULL,
    birth_date DATE,
    nationality TEXT,
    position TEXT CHECK(position IN ('GK','DF','MF','FW')),
    number INTEGER,
    status TEXT DEFAULT 'active',
    club_id INTEGER,
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
INSERT INTO players (name, nationality, position, number, club_id) VALUES
('Иван Петров', 'България', 'FW', 9, 1),
('Георги Иванов', 'България', 'MF', 8, 1),
('Николай Стоянов', 'България', 'DF', 5, 2),
('Димитър Костов', 'България', 'GK', 1, 2),
('Марселино', 'Бразилия', 'FW', 11, 3),
('Кирил Десподов', 'България', 'FW', 7, 3),
('Тодор Неделев', 'България', 'MF', 8, 4),
('Мартин Камбуров', 'България', 'FW', 9, 4),
('Стефан Велев', 'България', 'MF', 6, 5),
('Илиян Илиев', 'България', 'MF', 10, 6),
('Владимир Николов', 'България', 'FW', 19, 7),
('Радослав Цонев', 'България', 'MF', 17, 1),
('Антон Недялков', 'България', 'DF', 3, 3),
('Петър Витанов', 'България', 'MF', 21, 2),
('Станислав Иванов', 'България', 'FW', 99, 8),
('Иван Бандаловски', 'България', 'DF', 2, 9),
('Даниел Наумов', 'България', 'GK', 12, 10),
('Александър Василев', 'България', 'DF', 4, 5),
('Борис Тютюков', 'България', 'FW', 18, 6),
('Михаил Александров', 'България', 'FW', 77, 7);


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
