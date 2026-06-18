# 🏀 NBA Prop Bet Analyzer

A data-driven web app for analyzing NBA player prop bets using historical game log data,
probability modeling, and edge detection against bookmaker odds.

Built with Python and Streamlit.

---

## Features

### Three-Tier Data Loading
Player data is loaded using a prioritized fallback system designed to minimize
unnecessary API calls:
1. **GitHub CSV** — instantly loads a pre-cached CSV from a GitHub repository
2. **Local Cache** — falls back to a CSV saved from a previous API fetch on your machine
3. **nba_api** — live fetch as a last resort; result is automatically saved locally
   so future runs skip the API entirely

### Probability Calculation
For any player and prop line, three independent probability estimates are calculated:
- **Historical** — the raw percentage of games the player has gone over the line
- **Normal Distribution** — fits a bell curve to the player's stats and calculates
  the theoretical probability; handles small sample sizes better than raw counting
- **Recent Form** — same as historical but limited to the last 10 games to capture
  hot and cold streaks that season averages miss

### Edge Detection
Converts bookmaker odds (American or decimal format) into implied probabilities
and compares them against our calculated probabilities. The difference is the edge —
a positive edge means the market is underpricing the true probability, which is
where betting value lives. A recommendation is only generated when the edge
exceeds a configurable threshold (default 5%).

### Volatility Classification
Each player is classified as Consistent, Moderate, or Volatile using their
coefficient of variation (CV) — standard deviation divided by mean. Thresholds
are calibrated per stat type since three-pointers are inherently streakier than
points, rebounds behave differently than assists, and so on. The classification
drives a plain-English strategy note tailored to the player and stat.

---

## Project Structure
nba-prop-analyzer/

├── app.py                  # Streamlit UI

├── config.py               # All settings and thresholds

├── data/

│   └── fetcher.py          # Three-tier data loading

├── analysis/

│   ├── probabilities.py    # Historical, normal dist, recent form

│   ├── edges.py            # Implied probability and edge calculation

│   └── volatility.py       # CV-based classification and strategy

└── requirements.txt

---

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/nba-prop-analyzer.git
cd nba-prop-analyzer
pip install -r requirements.txt
streamlit run app.py
```

---

## Configuration

All settings live in `config.py`:

| Setting | Default | Description |
|---|---|---|
| `GITHUB_DATA_BASE_URL` | — | Raw GitHub URL for pre-cached CSVs |
| `DEFAULT_SEASON` | `2024-25` | NBA season to pull |
| `EDGE_THRESHOLD` | `0.05` | Minimum edge to recommend a bet |
| `RECENT_GAMES_WINDOW` | `10` | Games used for recent form calculation |

---

## Tech Stack

- **Python** — core logic
- **Streamlit** — web interface
- **nba_api** — NBA game log data
- **pandas** — data processing
- **scipy** — normal distribution modeling
- **plotly** — interactive charts