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

-- CLUBS
INSERT INTO clubs (name, city, founded_year) VALUES
('Левски София', 'София', 1914),
('ЦСКА София', 'София', 1948),
('Лудогорец', 'Разград', 2001),
('Ботев Пловдив', 'Пловдив', 1912);

-- PLAYERS
INSERT INTO players (name, nationality, position, number, club_id) VALUES
('Иван Петров', 'България', 'FW', 9, 1),
('Георги Иванов', 'България', 'MF', 8, 1),
('Марселино', 'Бразилия', 'FW', 11, 3);

-- LEAGUE
INSERT INTO leagues (name, season) VALUES
('Първа лига', '2025/2026');

-- LEAGUE TEAMS
INSERT INTO league_teams VALUES
(1,1),(1,2),(1,3),(1,4);

-- MATCH
INSERT INTO matches (league_id, home_club_id, away_club_id, match_date, home_goals, away_goals)
VALUES (1, 1, 4, '2025-09-01', 3, 0);

-- GOALS
INSERT INTO goals (match_id, player_id, minute) VALUES
(1, 1, 23),
(1, 1, 55),
(1, 2, 78);

-- CARD
INSERT INTO cards (match_id, player_id, card_type, minute)
VALUES (1, 3, 'yellow', 60);
