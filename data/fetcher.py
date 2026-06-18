import os
import time
import urllib.request
import urllib.error
import pandas as pd
from config import GITHUB_DATA_BASE_URL, LOCAL_CACHE_DIR, DEFAULT_SEASON, MIN_GAMES_THRESHOLD


def get_filename(player_name: str, season: str) -> str:
    """Consistent filename used for both local cache and GitHub."""
    return f"{player_name.replace(' ', '_')}_{season}.csv"


def get_local_path(player_name: str, season: str) -> str:
    return os.path.join(LOCAL_CACHE_DIR, get_filename(player_name, season))


def load_from_github(player_name: str, season: str) -> pd.DataFrame | None:
    url = GITHUB_DATA_BASE_URL + get_filename(player_name, season)
    try:
        print(f"Checking GitHub for {player_name}...")
        with urllib.request.urlopen(url, timeout=10) as response:
            df = pd.read_csv(response)
        if len(df) >= MIN_GAMES_THRESHOLD:
            return df
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"GitHub fetch failed (HTTP {e.code})")
    except Exception:
        pass
    return None


def load_from_local_cache(player_name: str, season: str) -> pd.DataFrame | None:
    path = get_local_path(player_name, season)
    if not os.path.exists(path):
        return None
    try:
        df = pd.read_csv(path)
        if len(df) >= MIN_GAMES_THRESHOLD:
            print(f"Loaded {player_name} from local cache")
            return df
    except Exception:
        pass
    return None


def load_from_api(player_name: str, season: str) -> pd.DataFrame | None:
    try:
        from nba_api.stats.endpoints import playergamelog
        from nba_api.stats.static import players as nba_players

        print(f"Fetching {player_name} from nba_api...")
        found = nba_players.find_players_by_full_name(player_name)
        if not found:
            print(f"Player '{player_name}' not found")
            return None

        player_id = found[0]['id']
        gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season)
        df = gamelog.get_data_frames()[0]

        if df.empty:
            return None

        # Save to local cache
        os.makedirs(LOCAL_CACHE_DIR, exist_ok=True)
        df.to_csv(get_local_path(player_name, season), index=False)
        print(f"Saved to local cache — commit to GitHub to skip API next time")
        return df

    except ImportError:
        print("nba_api not installed. Run: pip install nba_api")
        return None
    except Exception as e:
        print(f"API error: {e}")
        return None


def get_player_data(player_name: str, season: str = DEFAULT_SEASON) -> pd.DataFrame | None:
    """
    Load player game log data using three-tier fallback:
      1. GitHub CSV  → instant, no API needed
      2. Local cache → from a previous API fetch
      3. nba_api     → live fetch, result saved to local cache
    """
    df = load_from_github(player_name, season)
    if df is not None:
        return df

    df = load_from_local_cache(player_name, season)
    if df is not None:
        return df

    return load_from_api(player_name, season)