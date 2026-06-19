from data.fetcher import get_player_data

players = [
    "LeBron James",
    "Stephen Curry",
    "Luka Doncic",
    "Nikola Jokic",
    "Giannis Antetokounmpo"
]

for player in players:
    df = get_player_data(player)
    if df is not None:
        print(f"✅ {player}: {len(df)} games cached")
    else:
        print(f"❌ {player}: failed")