import random
import numpy as np
from datetime import datetime, timedelta
from db import get_connection



def estimate_team_strength(league_id):
    """
    Връща речник {team_id: (attack, defense)} само от ръчните стойности.
    Игнорира реални мачове и случайности.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT club_id FROM league_teams WHERE league_id = ?", (league_id,))
    teams = [row[0] for row in cursor.fetchall()]
    
    # Ръчни стойности за атака и защита (напиши тук меките стойности)
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
    
    strengths = {}
    for tid in teams:
        cursor.execute("SELECT name FROM clubs WHERE id = ?", (tid,))
        club_name = cursor.fetchone()[0]
        attack = manual_attack.get(club_name, 1.0)
        defense = manual_defense.get(club_name, 1.0)
        strengths[tid] = (attack, defense)
    
    conn.close()
    return strengths



def generate_synthetic_matches(league_id, num_matches=1000):
    """
    Генерира num_matches синтетични мача за дадена лига.
    Връща списък от речници: {'home_id', 'away_id', 'home_goals', 'away_goals', 'match_date'}
    """
    
    np.random.seed(42)
    random.seed(42)

    strengths = estimate_team_strength(league_id)   # връща {team_id: (attack, defense)}
    team_ids = list(strengths.keys())
    if len(team_ids) < 2:
        raise ValueError("Недостатъчно отбори за генериране на мачове.")

    synthetic_matches = []
    start_date = datetime(2024, 1, 1)
    for i in range(num_matches):
        home = random.choice(team_ids)
        away = random.choice([t for t in team_ids if t != home])
        
        # Вземаме атака и защита за двата отбора
        home_attack, home_defense = strengths[home]
        away_attack, away_defense = strengths[away]

        # Очаквани голове с домакинско предимство
        expected_home = home_attack * away_defense * 1.05
        expected_away = away_attack * home_defense * 0.95

        # Генерираме голове по Поасон
        home_goals = np.random.poisson(expected_home)
        away_goals = np.random.poisson(expected_away)

        # Случайна дата в рамките на сезона
        match_date = start_date + timedelta(days=random.randint(0, 365))
        synthetic_matches.append({
            'home_id': home,
            'away_id': away,
            'home_goals': home_goals,
            'away_goals': away_goals,
            'match_date': match_date.strftime('%Y-%m-%d')


        
        })
        if i < 5:
            print(f"Example {i}: home_attack={home_attack}, home_defense={home_defense}, away_attack={away_attack}, away_defense={away_defense}")
    return synthetic_matches
