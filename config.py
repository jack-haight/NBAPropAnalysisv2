# ── Data ──────────────────────────────────────────────────────
GITHUB_DATA_BASE_URL = "https://raw.githubusercontent.com/jack-haight/NBAPropAnalysisv2/main/player_data_cache/"
LOCAL_CACHE_DIR = "player_data_cache"
DEFAULT_SEASON = "2025-26"
MIN_GAMES_THRESHOLD = 10

# ── Analysis ──────────────────────────────────────────────────
EDGE_THRESHOLD = 0.05        # Minimum edge to recommend a bet (5%)
RECENT_GAMES_WINDOW = 10     # Games used for "recent form" calculation
BACKTEST_TEST_GAMES = 10     # Default games held out for backtesting

# ── Supported stat types ───────────────────────────────────────
STAT_TYPES = {
    "PTS":  "Points",
    "REB":  "Rebounds",
    "AST":  "Assists",
    "FG3M": "Three-Pointers Made",
    "STL":  "Steals",
    "BLK":  "Blocks",
    "TOV":  "Turnovers",
}