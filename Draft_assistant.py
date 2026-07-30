import random
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Superflex Draft Assistant", page_icon="🏈", layout="wide"
)


# Initialize Session State for Draft Board and Roster
if "drafted_ids" not in st.session_state:
    st.session_state.drafted_ids = set()

if "roster" not in st.session_state:
    st.session_state.roster = {
        "QB": [],
        "RB": [],
        "WR": [],
        "TE": [],
        "FLEX": [],
        "SUPERFLEX": [],
        "BN": [],
    }

# Generate baseline 150 player database tailored for Superflex Standard Scoring
@st.cache_data
def load_players():
    raw_players = [
        {"id": 1, "name": "Josh Allen", "pos": "QB", "team": "BUF", "bye": 12},
        {
            "id": 2,
            "name": "Patrick Mahomes",
            "pos": "QB",
            "team": "KC",
            "bye": 6,
        },
        {"id": 3, "name": "Lamar Jackson", "pos": "QB", "team": "BAL", "bye": 14},
        {"id": 4, "name": "Jalen Hurts", "pos": "QB", "team": "PHI", "bye": 5},
        {"id": 5, "name": "Joe Burrow", "pos": "QB", "team": "CIN", "bye": 12},
        {"id": 6, "name": "Saquon Barkley", "pos": "RB", "team": "PHI", "bye": 5},
        {"id": 7, "name": "Bijan Robinson", "pos": "RB", "team": "ATL", "bye": 11},
        {"id": 8, "name": "C.J. Stroud", "pos": "QB", "team": "HOU", "bye": 14},
        {
            "id": 9,
            "name": "Anthony Richardson",
            "pos": "QB",
            "team": "IND",
            "bye": 14,
        },
        {"id": 10, "name": "Ja'Marr Chase", "pos": "WR", "team": "CIN", "bye": 12},
        {
            "id": 11,
            "name": "Justin Jefferson",
            "pos": "WR",
            "team": "MIN",
            "bye": 6,
        },
        {"id": 12, "name": "CeeDee Lamb", "pos": "WR", "team": "DAL", "bye": 7},
        {"id": 13, "name": "Kyler Murray", "pos": "QB", "team": "ARI", "bye": 11},
        {"id": 14, "name": "Dak Prescott", "pos": "QB", "team": "DAL", "bye": 7},
        {"id": 15, "name": "Breece Hall", "pos": "RB", "team": "NYJ", "bye": 12},
        {
            "id": 16,
            "name": "Jonathan Taylor",
            "pos": "RB",
            "team": "IND",
            "bye": 14,
        },
        {
            "id": 17,
            "name": "Amon-Ra St. Brown",
            "pos": "WR",
            "team": "DET",
            "bye": 5,
        },
        {"id": 18, "name": "Tyreek Hill", "pos": "WR", "team": "MIA", "bye": 6},
        {"id": 19, "name": "Jordan Love", "pos": "QB", "team": "GB", "bye": 10},
        {"id": 20, "name": "Brock Purdy", "pos": "QB", "team": "SF", "bye": 9},
        {"id": 21, "name": "Jahmyr Gibbs", "pos": "RB", "team": "DET", "bye": 5},
        {
            "id": 22,
            "name": "Christian McCaffrey",
            "pos": "RB",
            "team": "SF",
            "bye": 9,
        },
        {"id": 23, "name": "A.J. Brown", "pos": "WR", "team": "PHI", "bye": 5},
        {"id": 24, "name": "Garrett Wilson", "pos": "WR", "team": "NYJ", "bye": 12},
        {
            "id": 25,
            "name": "Trevor Lawrence",
            "pos": "QB",
            "team": "JAX",
            "bye": 12,
        },
        {"id": 26, "name": "Caleb Williams", "pos": "QB", "team": "CHI", "bye": 7},
        {"id": 27, "name": "Derrick Henry", "pos": "RB", "team": "BAL", "bye": 14},
        {"id": 28, "name": "Kyren Williams", "pos": "RB", "team": "LAR", "bye": 6},
        {"id": 29, "name": "Drake London", "pos": "WR", "team": "ATL", "bye": 11},
        {
            "id": 30,
            "name": "Marvin Harrison Jr.",
            "pos": "WR",
            "team": "ARI",
            "bye": 11,
        },
        {"id": 31, "name": "Tua Tagovailoa", "pos": "QB", "team": "MIA", "bye": 6},
        {"id": 32, "name": "Kirk Cousins", "pos": "QB", "team": "ATL", "bye": 11},
        {
            "id": 33,
            "name": "Travis Etienne Jr.",
            "pos": "RB",
            "team": "JAX",
            "bye": 12,
        },
        {"id": 34, "name": "Isiah Pacheco", "pos": "RB", "team": "KC", "bye": 6},
        {"id": 35, "name": "Puka Nacua", "pos": "WR", "team": "LAR", "bye": 6},
        {"id": 36, "name": "Davante Adams", "pos": "WR", "team": "NYJ", "bye": 12},
        {"id": 37, "name": "Sam LaPorta", "pos": "TE", "team": "DET", "bye": 5},
        {"id": 38, "name": "Trey McBride", "pos": "TE", "team": "ARI", "bye": 11},
        {"id": 39, "name": "Jared Goff", "pos": "QB", "team": "DET", "bye": 5},
        {"id": 40, "name": "Baker Mayfield", "pos": "QB", "team": "TB", "bye": 11},
    ]

    positions = ["QB", "RB", "WR", "TE"]
    nfl_teams = [
        "BUF",
        "MIA",
        "NE",
        "NYJ",
        "BAL",
        "CIN",
        "CLE",
        "PIT",
        "HOU",
        "IND",
        "JAX",
        "TEN",
        "DEN",
        "KC",
        "LV",
        "LAC",
        "DAL",
        "NYG",
        "PHI",
        "WAS",
        "CHI",
        "DET",
        "GB",
        "MIN",
        "ATL",
        "CAR",
        "NO",
        "TB",
        "ARI",
        "LAR",
        "SF",
        "SEA",
    ]

    current_id = len(raw_players) + 1
    while len(raw_players) < 150:
        pos_choice = random.choice(positions)
        if random.random() > 0.8:
            pos_choice = "TE"

        raw_players.append(
            {
                "id": current_id,
                "name": f"Player {current_id} ({pos_choice})",
                "pos": pos_choice,
                "team": random.choice(nfl_teams),
                "bye": random.randint(5, 14),
            }
        )
        current_id += 1

    return pd.DataFrame(raw_players)


df_players = load_players()

# App Layout Header
st.title("🏈 Superflex Draft Assistant")
st.markdown("**10-Team • Standard Scoring • Top 150 Players Pool**")
st.markdown("---")

# Layout: Main Table (Left) & Roster/Advice (Right)
col_left, col_right = st.columns([2, 1])

with col_right:
    st.subheader("💡 Strategy Advice")
    qb_count = len(st.session_state.roster["QB"]) + len(
        [
            p
            for p in st.session_state.roster["SUPERFLEX"]
            if p["pos"] == "QB"
        ]
    )

    if qb_count == 0:
        st.warning(
            "**Priority Warning:** You have no starting Quarterback. In Superflex, starting QBs drive weekly ceiling. Consider locking one down immediately."
        )
    elif qb_count == 1:
        st.info(
            "**Strategy Tip:** You have your anchor QB. Look to secure tier-1 running backs or high-target wide receivers before your Superflex pick."
        )
    else:
        st.success(
            "**Balanced Build:** Your quarterback setup is secure. Focus heavily on high-floor standard scoring running backs and reliable wideouts."
        )

    st.markdown("---")
    st.subheader("📋 My Starting Roster")

    # Render Roster Slots
    slots = [
        ("QB", "Quarterback (QB)", 0),
        ("RB", "Running Back (RB)", 0),
        ("RB", "Running Back (RB)", 1),
        ("WR", "Wide Receiver (WR)", 0),
        ("WR", "Wide Receiver (WR)", 1),
        ("TE", "Tight End (TE)", 0),
        ("FLEX", "Flex (RB/WR/TE)", 0),
        ("SUPERFLEX", "Superflex (QB/FLEX)", 0),
    ]

    for cat, label, idx in slots:
        assigned_player = (
            st.session_state.roster[cat][idx]
            if len(st.session_state.roster[cat]) > idx
            else None
        )
        player_str = (
            f"**{assigned_player['name']}** ({assigned_player['pos']} - {assigned_player['team']})"
            if assigned_player
            else "— Empty —"
        )
        st.markdown(f"*{label}*<br>{player_str}", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Reset Draft Board", type="primary", use_container_width=True):
        st.session_state.drafted_ids = set()
        st.session_state.roster = {
            "QB": [],
            "RB": [],
            "WR": [],
            "TE": [],
            "FLEX": [],
            "SUPERFLEX": [],
            "BN": [],
        }
        st.rerun()

with col_left:
    st.subheader("Available Player Pool")

    # Filter Controls
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        search_query = st.text_input(
            "Search player name or team", placeholder="e.g. Josh Allen, BUF"
        )
    with f_col2:
        pos_filter = st.selectbox(
            "Filter by Position", ["ALL", "QB", "RB", "WR", "TE"]
        )

    # Filter dataframe based on search, position, and drafted status
    filtered_df = df_players[
        ~df_players["id"].isin(st.session_state.drafted_ids)
    ]

    if pos_filter != "ALL":
        filtered_df = filtered_df[filtered_df["pos"] == pos_filter]

    if search_query:
        filtered_df = filtered_df[
            filtered_df["name"]
            .str.lower()
            .str.contains(search_query.lower())
            | filtered_df["team"]
            .str.lower()
            .str.contains(search_query.lower())
        ]

    # Render Interactive Draft Rows
    for _, row in filtered_df.head(50).iterrows():
        c1, c2, c3, c4, c5 = st.columns([1, 3, 1, 1, 1])
        c1.write(f"#{row['id']}")
        c2.markdown(f"**{row['name']}**")
        c3.code(row["pos"])
        c4.text(row["team"])

        if c5.button("Draft", key=f"draft_{row['id']}"):
            player_obj = row.to_dict()
            st.session_state.drafted_ids.add(row["id"])

            # Smart Superflex Roster Routing Logic
            r = st.session_state.roster
            if player_obj["pos"] == "QB" and len(r["QB"]) < 1:
                r["QB"].append(player_obj)
            elif player_obj["pos"] == "RB" and len(r["RB"]) < 2:
                r["RB"].append(player_obj)
            elif player_obj["pos"] == "WR" and len(r["WR"]) < 2:
                r["WR"].append(player_obj)
            elif player_obj["pos"] == "TE" and len(r["TE"]) < 1:
                r["TE"].append(player_obj)
            elif player_obj["pos"] == "QB" and len(r["SUPERFLEX"]) < 1:
                r["SUPERFLEX"].append(player_obj)
            elif (
                player_obj["pos"] in ["RB", "WR", "TE"] and len(r["FLEX"]) < 1
            ):
                r["FLEX"].append(player_obj)
            elif len(r["SUPERFLEX"]) < 1:
                r["SUPERFLEX"].append(player_obj)
            else:
                r["BN"].append(player_obj)

            st.rerun()
            
