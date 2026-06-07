import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from ai.features import build_match_features
from ai.model import FootballPredictor
from repositories.leagues_repo import get_league, team_exists_in_league
from services.clubs_service import get_club_by_name
from db import get_connection


# Определяне на tools папката
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')
os.makedirs(TOOLS_DIR, exist_ok=True)


class AIService:
    def __init__(self):
        self.predictor = FootballPredictor()
        try:
            self.predictor.load()
        except FileNotFoundError:
            print("⚠️ Моделът не е обучен. Моля, стартирайте train_ai.py първо.")
            self.predictor.model = None


    def predict_match(self, team1_name, team2_name, league_name, season):
        # Валидация на отборите
        club1 = get_club_by_name(team1_name)
        club2 = get_club_by_name(team2_name)
        if not club1:
            return None, f"Отбор '{team1_name}' не съществува."
        if not club2:
            return None, f"Отбор '{team2_name}' не съществува."


        league = get_league(league_name, season)
        if not league:
            return None, "Лигата не съществува."


        league_id = league['id']
        if not team_exists_in_league(league_id, club1['id']) or not team_exists_in_league(league_id, club2['id']):
            return None, "Отборите не са в една и съща лига."


        # Проверка за минимум 5 изиграни мача на отбор
        def count_played_matches(club_id, league_id):
            conn = get_connection()
            c = conn.cursor()
            c.execute("""
                SELECT COUNT(*) FROM matches
                WHERE league_id = ? AND status='played' AND (home_club_id = ? OR away_club_id = ?)
            """, (league_id, club_id, club_id))
            cnt = c.fetchone()[0]
            conn.close()
            return cnt


        # if count_played_matches(club1['id'], league_id) < 1 or count_played_matches(club2['id'], league_id) < 1:
        #     return None, "Един от отборите няма достатъчно изиграни мачове (минимум 1)."


        # Извличане на характеристиките за този мач (към днешна дата)
        features = build_match_features(club1['id'], club2['id'], league_id, match_date=None)
        if self.predictor.model is None:
            return None, "Моделът не е зареден. Моля, обучете модела чрез train_ai.py."

        
        probs = self.predictor.predict_proba(features)
        home_prob, draw_prob, away_prob = [p * 100 for p in probs]


        total = home_prob + draw_prob + away_prob
        if abs(total - 100) > 0.01:
            factor = 100 / total
            home_prob *= factor
            draw_prob *= factor
            away_prob *= factor


        return {
            'home_win': round(home_prob, 1),
            'draw': round(draw_prob, 1),
            'away_win': round(away_prob, 1)
        }, None


    def generate_chart(self, team1_name, team2_name, league_name, season, save_path=None):
        if save_path is None:
            save_path = os.path.join(TOOLS_DIR, 'prediction_chart.png')
        result, err = self.predict_match(team1_name, team2_name, league_name, season)
        if err:
            return err
        from ai.chart import plot_probabilities
        plot_probabilities([result['home_win'], result['draw'], result['away_win']],
                           team1_name, team2_name, save_path)
        return f"Графиката е запазена в {save_path}"
