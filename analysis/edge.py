from .probabilities import calculate_probabilities
from config import EDGE_THRESHOLD


def american_to_implied_prob(odds: int) -> float:
    """Convert American odds to the implied probability the bookmaker is pricing in."""
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return abs(odds) / (abs(odds) + 100)


def decimal_to_american(decimal_odds: float) -> int:
    """Convert decimal odds (e.g. 1.91) to American odds (e.g. -110)."""
    if decimal_odds >= 2.0:
        return int((decimal_odds - 1) * 100)
    else:
        return int(-100 / (decimal_odds - 1))


def normalize_odds(odds: float) -> int:
    """
    Accept either American (-110) or decimal (1.91) odds and
    always return American format as an integer.
    """
    if 1.0 < odds < 10.0:
        return decimal_to_american(odds)
    return int(odds)


def calculate_edges(df, prop_line: float, over_odds: float,
                    under_odds: float, stat_column: str) -> dict | None:
    """
    Compare our calculated probabilities against the bookmaker's
    implied probabilities to find edges.

    A positive edge means we think the true probability is higher
    than what the odds are pricing in — potential value bet.
    """
    probs = calculate_probabilities(df, prop_line, stat_column)
    if not probs:
        return None

    over_odds = normalize_odds(over_odds)
    under_odds = normalize_odds(under_odds)

    implied_over = american_to_implied_prob(over_odds)
    implied_under = american_to_implied_prob(under_odds)

    # Edge = our probability minus the bookmaker's implied probability
    historical_over_edge  = probs["historical_over"]  - implied_over
    historical_under_edge = probs["historical_under"] - implied_under
    normal_over_edge      = probs["normal_over"]      - implied_over
    normal_under_edge     = probs["normal_under"]     - implied_under

    # Recommendation based on historical edge vs threshold in config.py
    best_edge = max(historical_over_edge, historical_under_edge)
    if historical_over_edge > historical_under_edge and best_edge >= EDGE_THRESHOLD:
        recommendation = "BET OVER"
    elif historical_under_edge > historical_over_edge and best_edge >= EDGE_THRESHOLD:
        recommendation = "BET UNDER"
    else:
        recommendation = "NO BET"

    return {
        # Odds
        "over_odds":            over_odds,
        "under_odds":           under_odds,
        "implied_over":         round(implied_over, 4),
        "implied_under":        round(implied_under, 4),
        # Edges
        "historical_over_edge":  round(historical_over_edge, 4),
        "historical_under_edge": round(historical_under_edge, 4),
        "normal_over_edge":      round(normal_over_edge, 4),
        "normal_under_edge":     round(normal_under_edge, 4),
        # Recommendation
        "best_edge":            round(best_edge, 4),
        "recommendation":       recommendation,
        # Pass through probabilities so the UI only needs one dict
        **probs,
    }