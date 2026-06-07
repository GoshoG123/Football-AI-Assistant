# import sys
# import os
# import random
# from datetime import datetime, timedelta
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# from db import get_connection
# from repositories.leagues_repo import get_league, get_league_teams


# def generate_matches(league_name, season, matches_per_team=5):
#     """
#     Генерира фиктивни изиграни мачове за дадена лига, така че всеки отбор да има поне `matches_per_team` мача.
#     Съществуващите вече изиграни мачове (status='played') се запазват, добавят се нови.
#     """
#     league = get_league(league_name, season)
#     if not league:
#         print(f"❌ Лига {league_name} {season} не съществува.")
#         return


#     league_id = league['id']
#     teams = get_league_teams(league_id)
#     if len(teams) < 2:
#         print("❌ Недостатъчно отбори в лигата.")
#         return


#     team_ids = [t['id'] for t in teams]
#     conn = get_connection()
#     cursor = conn.cursor()


#     # Колко мача вече има всеки отбор?
#     played_counts = {}
#     for tid in team_ids:
#         cursor.execute("""
#             SELECT COUNT(*) FROM matches
#             WHERE league_id = ? AND status = 'played' AND (home_club_id = ? OR away_club_id = ?)
#         """, (league_id, tid, tid))
#         played_counts[tid] = cursor.fetchone()[0]


#     # Идентифицираме кои отбори имат нужда от още мачове
#     needed = {tid: max(0, matches_per_team - played_counts[tid]) for tid in team_ids}
#     print(f"📊 Текущ брой изиграни мачове на отбор: {played_counts}")
#     print(f"📈 Необходими допълнителни мачове: {needed}")


#     # Генерираме необходимия брой мачове
#     new_matches = []
#     # За да не правим твърде много кръгове, ще правим ротация, докато всички нужди са покрити
#     # Ограничаваме до 200 опита
#     max_attempts = 200
#     attempt = 0
#     while any(v > 0 for v in needed.values()) and attempt < max_attempts:
#         # Избираме два различни отбора, които все още имат нужда
#         need_list = [tid for tid, cnt in needed.items() if cnt > 0]
#         if len(need_list) < 2:
#             # Ако остане само един отбор, го сдвояваме с произволен
#             home = need_list[0]
#             away = random.choice([t for t in team_ids if t != home])
#         else:
#             home = random.choice(need_list)
#             away = random.choice([t for t in need_list if t != home])


#         # Генерираме случаен резултат (реалистичен)
#         home_goals = random.randint(0, 4)
#         away_goals = random.randint(0, 4)
#         # Случайна дата в последните 3 месеца
#         fake_date = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d')


#         # Вмъкваме мача
#         cursor.execute("""
#             INSERT INTO matches (league_id, round_no, home_club_id, away_club_id, match_date, home_goals, away_goals, status)
#             VALUES (?, ?, ?, ?, ?, ?, ?, 'played')
#         """, (league_id, 999, home, away, fake_date, home_goals, away_goals))
#         new_matches.append((home, away, home_goals, away_goals))


#         # Намаляваме нуждите
#         needed[home] -= 1
#         needed[away] -= 1
#         attempt += 1


#     conn.commit()
#     conn.close()


#     print(f"✅ Генерирани {len(new_matches)} нови мача.")
#     for h, a, hg, ag in new_matches[:10]:  # показваме първите 10
#         print(f"   {h} vs {a} : {hg}-{ag}")
#     if len(new_matches) > 10:
#         print(f"   ... и още {len(new_matches)-10} мача.")


# if __name__ == "__main__":
#     from repositories.leagues_repo import get_all_leagues
#     leagues = get_all_leagues()
#     if not leagues:
#         print("Няма налични лиги! Моля, създайте лига първо.")
#     else:
#         last_league = leagues[-1]
#         print(f"Използвам последната лига: {last_league['name']} ({last_league['season']})")
#         generate_matches(last_league['name'], last_league['season'], matches_per_team=5)
