import pandas as pd
import numpy as np
from scipy import stats
from config import RECENT_GAMES_WINDOW


def calculate_probabilities(df: pd.DataFrame, prop_line: float, stat_column: str) -> dict | None:
    """
    Given a player's game log, calculate the probability of going
    over a prop line using three different methods.
    """
    if stat_column not in df.columns:
        print(f"Stat '{stat_column}' not found in data")
        return None

    values = df[stat_column].dropna()

    if len(values) == 0:
        return None

    mean = values.mean()
    std = values.std()

    # ── Method 1: Historical ──────────────────────────────────
    # Simply count how many games the player actually went over
    historical_over = (values > prop_line).mean()

    # ── Method 2: Normal distribution ────────────────────────
    # Fits a bell curve to the data and calculates the probability
    # Works better when sample size is small
    if std > 0:
        z_score = (prop_line - mean) / std
        normal_over = 1 - stats.norm.cdf(z_score)
    else:
        normal_over = 1.0 if mean > prop_line else 0.0

    # ── Method 3: Recent form ─────────────────────────────────
    # Same as historical but only looks at the last N games
    # Captures hot/cold streaks that season averages miss
    recent = values.tail(RECENT_GAMES_WINDOW)
    recent_over = (recent > prop_line).mean()

    return {
        "prop_line":       prop_line,
        "stat":            stat_column,
        "mean":            round(mean, 2),
        "std":             round(std, 2),
        "total_games":     len(values),
        "historical_over": round(historical_over, 4),
        "historical_under": round(1 - historical_over, 4),
        "normal_over":     round(normal_over, 4),
        "normal_under":    round(1 - normal_over, 4),
        "recent_over":     round(recent_over, 4),
        "cv":              round(std / mean, 4) if mean != 0 else 0,
    }


