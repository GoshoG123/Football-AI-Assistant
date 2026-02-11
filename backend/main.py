from services.clubs import (
    add_club,
    get_all_clubs,
    get_club_by_name,
    update_club,
    delete_club
)



# =========================
# TEST CREATE
# =========================
print("Adding club...")
add_club("Берое", "Стара Загора", 1916)

# =========================
# TEST READ ALL
# =========================
print("\nAll clubs:")
clubs = get_all_clubs()
for club in clubs:
    print(dict(club))

# =========================
# TEST READ ONE
# =========================
print("\nGet club by name:")
club = get_club_by_name("Берое")
if club:
    print(dict(club))

# =========================
# TEST UPDATE
# =========================
print("\nUpdating club...")
update_club("Берое", "Стара Загора", 1920)

print("After update:")
club = get_club_by_name("Берое")
if club:
    print(dict(club))

# =========================
# TEST DELETE
# =========================
print("\nDeleting club...")
delete_club("Берое")

print("After delete:")
club = get_club_by_name("Берое")
print(club)
