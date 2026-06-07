# src/ai/train_ai.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ========= НОВО: определяме tools папката =========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(BASE_DIR, 'tools')
os.makedirs(TOOLS_DIR, exist_ok=True)   # създава папката, ако не съществува
# =================================================


from ai.features import build_dataset_from_matches, get_team_features
from ai.model import FootballPredictor
from ai.chart import plot_feature_importance
from ai.export_csv import export_training_data
from ai.data_generator import generate_synthetic_matches
from repositories.leagues_repo import get_league


def train(league_name, season, force_synthetic=False):
    print(f"🔍 Зареждане на лига: {league_name} {season}")
    league = get_league(league_name, season)
    if not league:
        print("❌ Лигата не съществува.")
        return
    league_id = league['id']


    # Реални мачове
    dataset_real, _ = build_dataset_from_matches(league_id)
    print(f"📊 Реални мачове: {len(dataset_real)}")


    # Ако са твърде малко, генерираме синтетични
    min_matches_needed = 50
    if len(dataset_real) < min_matches_needed or force_synthetic:
        print(f"⚠️ Недостатъчно реални данни ({len(dataset_real)} < {min_matches_needed}). Генериране на синтетични мачове...")
        synthetic_matches = generate_synthetic_matches(league_id, num_matches=500)
        synthetic_dataset = []
        for m in synthetic_matches:
            home_feat = get_team_features(m['home_id'], league_id, is_home=True, before_date=None)
            away_feat = get_team_features(m['away_id'], league_id, is_home=False, before_date=None)
            feats = [
                home_feat['form'], home_feat['avg_goals_scored'], home_feat['avg_goals_conceded'],
                home_feat['position'], home_feat['points'], home_feat['goal_diff'], home_feat['home_advantage'],
                away_feat['form'], away_feat['avg_goals_scored'], away_feat['avg_goals_conceded'],
                away_feat['position'], away_feat['points'], away_feat['goal_diff'], away_feat['home_advantage']
            ]
            if m['home_goals'] > m['away_goals']:
                label = 0
            elif m['home_goals'] == m['away_goals']:
                label = 1
            else:
                label = 2
            synthetic_dataset.append((feats, label))
        dataset = dataset_real + synthetic_dataset
        print(f"➕ Общ брой тренировъчни примери: {len(dataset)} (реални + синтетични)")
    else:
        dataset = dataset_real


    if len(dataset) < 10:
        print("❌ Твърде малко данни за обучение (дори със синтетични).")
        return


    X = [item[0] for item in dataset]
    y = [item[1] for item in dataset]


    # Имена на характеристиките
    feature_names = [
        'home_form', 'home_avg_scored', 'home_avg_conceded',
        'home_position', 'home_points', 'home_gd', 'home_advantage',
        'away_form', 'away_avg_scored', 'away_avg_conceded',
        'away_position', 'away_points', 'away_gd', 'away_advantage'
    ]


    # ========= Променени пътища – всичко в tools/ =========
    csv_path = os.path.join(TOOLS_DIR, 'training_data.csv')
    model_path = os.path.join(TOOLS_DIR, 'xgboost_model.pkl')
    importance_path = os.path.join(TOOLS_DIR, 'feature_importance.png')
    # =====================================================


    # Експорт на CSV
    export_training_data(X, y, feature_names, csv_path)


    # Обучение на модела (подаваме пътя до .pkl)
    predictor = FootballPredictor(model_path=model_path)
    acc, loss, cv_scores = predictor.train(X, y)


    # Feature importance графика
    importance = predictor.feature_importance(feature_names)
    plot_feature_importance(importance, importance_path)


    print("\n🎉 Обучението завърши успешно!")
    print(f"Точност: {acc:.3f}, Log Loss: {loss:.3f}, CV accuracy: {cv_scores.mean():.3f}")


if __name__ == '__main__':
    train('Първа лига', '2025/2026', force_synthetic=False)
