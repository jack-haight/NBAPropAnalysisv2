from config import STAT_TYPES


def classify_volatility(cv: float, stat_column: str) -> tuple[str, str]:
    """
    Classify a player as consistent, moderate, or volatile based on
    their coefficient of variation (CV) for a given stat type.

    Returns a (label, strategy) tuple.
    """

    # Each stat has different thresholds because some stats are
    # naturally more volatile than others — 3-pointers will always
    # have a higher CV than points, for example.
    thresholds = {
        "PTS":  (0.30, 0.45),
        "REB":  (0.25, 0.40),
        "AST":  (0.30, 0.50),
        "FG3M": (0.60, 0.80),
        "STL":  (0.70, 1.00),
        "BLK":  (0.70, 1.00),
        "TOV":  (0.40, 0.60),
    }

    low, high = thresholds.get(stat_column, (0.30, 0.50))

    if cv < low:
        label = "CONSISTENT"
        strategy = (
            f"Very predictable — CV of {cv:.2f} means low game-to-game variance. "
            f"Look for prop lines set 2+ units away from their average for the best value. "
            f"Avoid when the line is within 1 unit of their average."
        )
    elif cv < high:
        label = "MODERATE"
        strategy = (
            f"Moderately consistent — CV of {cv:.2f}. "
            f"Consider both season average and recent form together. "
            f"Factor in matchup difficulty and pace before betting."
        )
    else:
        label = "VOLATILE"
        strategy = (
            f"High variance player — CV of {cv:.2f} means big swings game to game. "
            f"Look for plus-money lines that don't account for ceiling games. "
            f"Higher risk but better reward — check pace and matchup carefully."
        )

    return label, strategy


def get_volatility_report(probs: dict) -> dict:
    """
    Takes the probability dict from calculate_probabilities() and
    returns a volatility classification and strategy recommendation.
    """
    cv = probs["cv"]
    stat = probs["stat"]
    stat_label = STAT_TYPES.get(stat, stat)

    label, strategy = classify_volatility(cv, stat)

    return {
        "stat_label":  stat_label,
        "cv":          cv,
        "volatility":  probs["std"],
        "label":       label,
        "strategy":    strategy,
    }