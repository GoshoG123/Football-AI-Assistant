# src/ai/features.py
import sqlite3
from datetime import datetime
from collections import defaultdict
from db import get_connection


def get_manual_strength(club_name):
    manual_attack = {
    "Лудогорец": 1.16,
    "Левски София": 1.10,
    "ЦСКА София": 1.06,
    "Ботев Пловдив": 1.02,
    "Черно море": 1.00,
    "Арда": 0.98,
    "Славия": 0.96,
    "Локомотив Пловдив": 0.97,
    "Берое": 0.92,
    "Пирин Благоевград": 0.92
    }

    manual_defense = {
    "Лудогорец": 0.92,
    "Левски София": 0.96,
    "ЦСКА София": 0.98,
    "Ботев Пловдив": 1.00,
    "Черно море": 1.01,
    "Арда": 1.03,
    "Славия": 1.05,
    "Локомотив Пловдив": 1.03,
    "Берое": 1.09,
    "Пирин Благоевград": 1.09
    }
    return manual_attack.get(club_name, 1.0), manual_defense.get(club_name, 1.0)

def get_club_name_by_id(club_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM clubs WHERE id = ?", (club_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_manual_position(team_id, league_id):
    """Връща позиция в класирането според атакуващата сила (по-високата атака = по-добра позиция)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT club_id FROM league_teams WHERE league_id = ?", (league_id,))
    team_ids = [row[0] for row in cursor.fetchall()]
    conn.close()
    strengths = []
    for tid in team_ids:
        name = get_club_name_by_id(tid)
        attack, _ = get_manual_strength(name)
        strengths.append((tid, attack))
    strengths.sort(key=lambda x: x[1], reverse=True)
    for pos, (tid, _) in enumerate(strengths, 1):
        if tid == team_id:
            return pos
    return len(team_ids)  # last


def get_team_season_stats(team_id, league_id, before_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    if before_date:
        date_cond = "AND match_date < ?"
    else:
        date_cond = ""
    query = f"""
        SELECT
            COUNT(*) as mp,
            SUM(CASE
                WHEN home_club_id = ? AND home_goals > away_goals THEN 3
                WHEN home_club_id = ? AND home_goals = away_goals THEN 1
                WHEN home_club_id = ? AND home_goals < away_goals THEN 0
                WHEN away_club_id = ? AND away_goals > home_goals THEN 3
                WHEN away_club_id = ? AND away_goals = home_goals THEN 1
                WHEN away_club_id = ? AND away_goals < home_goals THEN 0
            END) as points,
            SUM(CASE WHEN home_club_id = ? THEN home_goals ELSE away_goals END) as gf,
            SUM(CASE WHEN home_club_id = ? THEN away_goals ELSE home_goals END) as ga
        FROM matches
        WHERE status = 'played'
        AND league_id = ?
        AND (home_club_id = ? OR away_club_id = ?)
        {date_cond}
    """
    base_params = (team_id,) * 8 + (league_id, team_id, team_id)
    if before_date:
        full_params = base_params + (before_date,)
    else:
        full_params = base_params
    cursor.execute(query, full_params)
    row = cursor.fetchone()
    conn.close()
    if row and row[0] > 0:
        return row[0], row[1], row[2], row[3]
    return 0, 0, 0, 0

def get_last_n_matches_form(team_id, league_id, n=5, before_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    date_cond = "AND match_date < ?" if before_date else ""
    query = f"""
        SELECT
            CASE
                WHEN home_club_id = ? AND home_goals > away_goals THEN 3
                WHEN home_club_id = ? AND home_goals = away_goals THEN 1
                WHEN home_club_id = ? AND home_goals < away_goals THEN 0
                WHEN away_club_id = ? AND away_goals > home_goals THEN 3
                WHEN away_club_id = ? AND away_goals = home_goals THEN 1
                WHEN away_club_id = ? AND away_goals < home_goals THEN 0
            END as points
        FROM matches
        WHERE status = 'played'
        AND league_id = ?
        AND (home_club_id = ? OR away_club_id = ?)
        {date_cond}
        ORDER BY match_date DESC
        LIMIT ?
    """
    if before_date:
        params = [team_id] * 6 + [league_id, team_id, team_id, before_date, n]
        cursor.execute(query, params)
    else:
        base_params = (team_id,) * 6 + (league_id, team_id, team_id, n)
        cursor.execute(query, base_params)
    rows = cursor.fetchall()
    conn.close()
    total_points = sum(row[0] for row in rows)
    return total_points

def get_standings_position(team_id, league_id, before_date=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT club_id FROM league_teams WHERE league_id = ?", (league_id,))
    all_teams = [row[0] for row in cursor.fetchall()]
    stats = []
    for tid in all_teams:
        mp, pts, gf, ga = get_team_season_stats(tid, league_id, before_date)
        gd = gf - ga
        stats.append((tid, pts, gd, gf))
    stats.sort(key=lambda x: (x[1], x[2], x[3]), reverse=True)
    for pos, (tid, _, _, _) in enumerate(stats, 1):
        if tid == team_id:
            conn.close()
            return pos
    conn.close()
    return len(all_teams)

def get_team_features(team_id, league_id, is_home, before_date=None):
    mp, pts, gf, ga = get_team_season_stats(team_id, league_id, before_date)
    if mp == 0:
        # Няма реални мачове – използваме ръчните атака/защита
        club_name = get_club_name_by_id(team_id)
        attack, defense = get_manual_strength(club_name)
        avg_gf = attack
        avg_ga = defense
        position = get_manual_position(team_id, league_id)
        form = 0
        gd = 0
        pts = 0
    else:
        form = get_last_n_matches_form(team_id, league_id, 5, before_date)
        avg_gf = gf / mp
        avg_ga = ga / mp
        position = get_standings_position(team_id, league_id, before_date)
        gd = gf - ga
    return {
        'form': form,
        'avg_goals_scored': avg_gf,
        'avg_goals_conceded': avg_ga,
        'position': position,
        'points': pts,
        'goal_diff': gd,
        'home_advantage': 1 if is_home else 0
    }

def build_match_features(home_id, away_id, league_id, match_date=None):
    home_feat = get_team_features(home_id, league_id, is_home=True, before_date=match_date)
    away_feat = get_team_features(away_id, league_id, is_home=False, before_date=match_date)
    features = [
        home_feat['form'], home_feat['avg_goals_scored'], home_feat['avg_goals_conceded'],
        home_feat['position'], home_feat['points'], home_feat['goal_diff'], home_feat['home_advantage'],
        away_feat['form'], away_feat['avg_goals_scored'], away_feat['avg_goals_conceded'],
        away_feat['position'], away_feat['points'], away_feat['goal_diff'], away_feat['home_advantage']
    ]
    return features

def build_dataset_from_matches(league_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, home_club_id, away_club_id, home_goals, away_goals, match_date
        FROM matches
        WHERE league_id = ? AND status = 'played'
        ORDER BY match_date
    """, (league_id,))
    matches = cursor.fetchall()
    conn.close()
    dataset = []
    match_ids = []
    for m in matches:
        match_id, home_id, away_id, hg, ag, match_date = m
        if hg is None or ag is None:
            continue
        if hg > ag:
            label = 0
        elif hg == ag:
            label = 1
        else:
            label = 2
        feats = build_match_features(home_id, away_id, league_id, match_date)
        dataset.append((feats, label))
        match_ids.append(match_id)
    return dataset, match_ids