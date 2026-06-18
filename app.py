import streamlit as st
from data.fetcher import get_player_data
from analysis.probabilities import calculate_probabilities
from analysis.edge import calculate_edges
from analysis.volatility import get_volatility_report
from config import STAT_TYPES, DEFAULT_SEASON
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="NBA Prop Analyzer",
    page_icon="🏀",
    layout="wide"
)

st.title("🏀 NBA Prop Bet Analyzer")
st.caption("Analyze player props using historical data, probability modeling, and edge detection.")

# ── Sidebar inputs ─────────────────────────────────────────────
st.sidebar.header("Prop Details")

player_name = st.sidebar.text_input("Player Name", placeholder="e.g. LeBron James")
season = st.sidebar.text_input("Season", value=DEFAULT_SEASON)

stat_column = st.sidebar.selectbox(
    "Stat Type",
    options=list(STAT_TYPES.keys()),
    format_func=lambda x: f"{x} — {STAT_TYPES[x]}"
)

prop_line = st.sidebar.number_input("Prop Line", min_value=0.0, step=0.5, value=25.0)
over_odds = st.sidebar.number_input("Over Odds (American)", value=-110, step=5)
under_odds = st.sidebar.number_input("Under Odds (American)", value=-110, step=5)

analyze = st.sidebar.button("Analyze", use_container_width=True)

# ── Results ────────────────────────────────────────────────────
if analyze:
    if not player_name:
        st.warning("Please enter a player name.")
    else:
        with st.spinner(f"Loading data for {player_name}..."):
            df = get_player_data(player_name, season)

        if df is None:
            st.error(f"Could not load data for '{player_name}'. Check the spelling and try again.")
        else:
            edges = calculate_edges(df, prop_line, over_odds, under_odds, stat_column)
            volatility = get_volatility_report(edges)

            # ── Header ─────────────────────────────────────────
            st.subheader(f"{player_name} — {STAT_TYPES[stat_column]} {prop_line}")

            # ── Top metrics ────────────────────────────────────
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Player Average", f"{edges['mean']}")
            col2.metric("Historical Over", f"{edges['historical_over']:.1%}")
            col3.metric("Recent Form Over", f"{edges['recent_over']:.1%}")
            col4.metric("Normal Dist Over", f"{edges['normal_over']:.1%}")

            st.divider()

            # ── Edge analysis ──────────────────────────────────
            col5, col6 = st.columns(2)

            with col5:
                st.subheader("Edge Analysis")
                st.metric("Implied Over Prob", f"{edges['implied_over']:.1%}")
                st.metric("Historical Over Edge", f"{edges['historical_over_edge']:+.1%}")
                st.metric("Historical Under Edge", f"{edges['historical_under_edge']:+.1%}")

            with col6:
                st.subheader("Volatility")
                st.metric("Classification", volatility['label'])
                st.metric("Std Deviation", f"{volatility['volatility']:.1f}")
                st.metric("CV", f"{volatility['cv']:.2f}")

            st.divider()

            # ── Recommendation ─────────────────────────────────
            rec = edges['recommendation']
            if rec == "BET OVER":
                st.success(f"🎯 {rec} {prop_line} — Edge: {edges['best_edge']:+.1%}")
            elif rec == "BET UNDER":
                st.success(f"🎯 {rec} {prop_line} — Edge: {edges['best_edge']:+.1%}")
            else:
                st.warning(f"❌ NO BET — Max edge {edges['best_edge']:+.1%} is below threshold")

            # ── Strategy ───────────────────────────────────────
            st.subheader("Strategy Note")
            st.info(volatility['strategy'])

            # ── Chart ─────────────────────────────────────────
            st.subheader("Recent Game Log")

            chart_df = df[["GAME_DATE", stat_column]].copy()
            chart_df = chart_df.head(20)
            chart_df["GAME_DATE"] = pd.to_datetime(chart_df["GAME_DATE"])
            chart_df = chart_df.sort_values("GAME_DATE")
            chart_df["Result"] = chart_df[stat_column].apply(
                lambda x: "Over" if x > prop_line else "Under"
            )

            fig = px.scatter(
                chart_df,
                x="GAME_DATE",
                y=stat_column,
                color="Result",
                color_discrete_map={"Over": "#00C896", "Under": "#FF4B4B"},
                title=f"{player_name} — Last 20 {STAT_TYPES[stat_column]} Games",
            )

            fig.add_hline(
                y=prop_line,
                line_dash="dash",
                line_color="white",
                annotation_text=f"Prop Line {prop_line}",
                annotation_position="top left"
            )

            fig.add_hline(
                y=edges["mean"],
                line_dash="dot",
                line_color="yellow",
                annotation_text=f"Season Avg {edges['mean']}",
                annotation_position="bottom left"
            )

            fig.update_layout(
                plot_bgcolor="#0E1117",
                paper_bgcolor="#0E1117",
                font_color="white",
                xaxis_title="Date",
                yaxis_title=STAT_TYPES[stat_column],
            )

            st.plotly_chart(fig, use_container_width=True)