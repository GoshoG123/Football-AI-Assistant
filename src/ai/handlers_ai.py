# src/ai/handlers_ai.py
from ai.ai_service import AIService
from services.clubs_service import get_all_clubs




ai_service = AIService()




def find_club_by_name_partial(name):
    """
    ВИНАГИ връща (club, error_message)
    """
    clubs = get_all_clubs()
    if not clubs:
        return (None, "Няма добавени клубове в базата. Изпълнете 'Покажи всички клубове' за да проверите.")




    name_lower = name.strip().lower()
   
    # Точен match
    for club in clubs:
        if club['name'].lower() == name_lower:
            return (club, None)




    # Частичен match
    matches = [c for c in clubs if name_lower in c['name'].lower()]
    if len(matches) == 1:
        return (matches[0], None)
    elif len(matches) > 1:
        club_names = ', '.join([c['name'] for c in matches])
        return (None, f"Няколко отбора съвпадат с '{name}': {club_names}")
    else:
        all_names = ', '.join([c['name'] for c in clubs])
        return (None, f"Няма отбор, съдържащ '{name}'. Налични: {all_names}")




def handle_prediction(match):
    if match is None or not hasattr(match, 'groups'):
        return "❌ Вътрешна грешка: липсва информация за мача."




    try:
        team1_raw = match.group(1).strip()
        team2_raw = match.group(2).strip()
    except IndexError:
        return "❌ Невалиден формат. Използвайте: Прогноза Отбор1 срещу Отбор2"




    club1, err1 = find_club_by_name_partial(team1_raw)
    if err1:
        return f"❌ {err1}"
    if club1 is None:
        return f"❌ Не можах да идентифицирам отбор '{team1_raw}'."




    club2, err2 = find_club_by_name_partial(team2_raw)
    if err2:
        return f"❌ {err2}"
    if club2 is None:
        return f"❌ Не можах да идентифицирам отбор '{team2_raw}'."




    team1 = club1['name']
    team2 = club2['name']




    # Определяне на лига
    from repositories.leagues_repo import get_all_leagues
    leagues = get_all_leagues()
    if not leagues:
        return "❌ Няма създадена лига. Първо създайте лига с 'Създай лига Име Сезон'"




    league = leagues[-1]  # последно създадена
    league_name = league['name']
    season = league['season']




    # Прогноза
    result, error = ai_service.predict_match(team1, team2, league_name, season)
    if error:
        return f"❌ Грешка от модела: {error}"




    # Графика
    chart_msg = ai_service.generate_chart(team1, team2, league_name, season)




    return (f"📊 Прогноза за мача {team1} срещу {team2}:\n"
            f"🏠 {team1}: {result['home_win']}%\n"
            f"🤝 Равен: {result['draw']}%\n"
            f"✈️ {team2}: {result['away_win']}%\n"
            f"📈 {chart_msg}")
