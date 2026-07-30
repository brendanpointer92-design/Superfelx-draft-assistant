import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="10-Team Superflex Draft Assistant",
    page_icon="🏈",
    layout="wide",
)

st.title("🏈 10-Team NFL Superflex Draft Assistant")

# --- CSV Upload Sidebar ---
st.sidebar.header("📁 Import Rankings")
uploaded_file = st.sidebar.file_uploader(
    "Upload FantasyPros Superflex CSV", type=["csv"]
)

# Expanded Default Player Pool (FantasyPros Consensus Superflex)
DEFAULT_PLAYERS = [
    # TIER 1
    {
        "Rank": 1,
        "Name": "Josh Allen",
        "Pos": "QB",
        "Team": "BUF",
        "Tier": 1,
        "Bye": 7,
    },
    {
        "Rank": 2,
        "Name": "Drake Maye",
        "Pos": "QB",
        "Team": "NE",
        "Tier": 1,
        "Bye": 11,
    },
    {
        "Rank": 3,
        "Name": "Jayden Daniels",
        "Pos": "QB",
        "Team": "WAS",
        "Tier": 1,
        "Bye": 7,
    },
    {
        "Rank": 4,
        "Name": "Ja'Marr Chase",
        "Pos": "WR",
        "Team": "CIN",
        "Tier": 1,
        "Bye": 6,
    },
    {
        "Rank": 5,
        "Name": "Lamar Jackson",
        "Pos": "QB",
        "Team": "BAL",
        "Tier": 1,
        "Bye": 13,
    },
    # TIER 2
    {
        "Rank": 6,
        "Name": "Jaxon Smith-Njigba",
        "Pos": "WR",
        "Team": "SEA",
        "Tier": 2,
        "Bye": 11,
    },
    {
        "Rank": 7,
        "Name": "Joe Burrow",
        "Pos": "QB",
        "Team": "CIN",
        "Tier": 2,
        "Bye": 6,
    },
    {
        "Rank": 8,
        "Name": "Puka Nacua",
        "Pos": "WR",
        "Team": "LAR",
        "Tier": 2,
        "Bye": 11,
    },
    {
        "Rank": 9,
        "Name": "Bijan Robinson",
        "Pos": "RB",
        "Team": "ATL",
        "Tier": 2,
        "Bye": 11,
    },
    {
        "Rank": 10,
        "Name": "Caleb Williams",
        "Pos": "QB",
        "Team": "CHI",
        "Tier": 2,
        "Bye": 10,
    },
    {
        "Rank": 11,
        "Name": "Jahmyr Gibbs",
        "Pos": "RB",
        "Team": "DET",
        "Tier": 2,
        "Bye": 6,
    },
    # TIER 3
    {
        "Rank": 12,
        "Name": "Justin Herbert",
        "Pos": "QB",
        "Team": "LAC",
        "Tier": 3,
        "Bye": 7,
    },
    {
        "Rank": 13,
        "Name": "Patrick Mahomes",
        "Pos": "QB",
        "Team": "KC",
        "Tier": 3,
        "Bye": 10,
    },
    {
        "Rank": 14,
        "Name": "Jalen Hurts",
        "Pos": "QB",
        "Team": "PHI",
        "Tier": 3,
        "Bye": 10,
    },
    {
        "Rank": 15,
        "Name": "Amon-Ra St. Brown",
        "Pos": "WR",
        "Team": "DET",
        "Tier": 3,
        "Bye": 6,
    },
    {
        "Rank": 16,
        "Name": "Justin Jefferson",
        "Pos": "WR",
        "Team": "MIN",
        "Tier": 3,
        "Bye": 6,
    },
    {
        "Rank": 17,
        "Name": "Trevor Lawrence",
        "Pos": "QB",
        "Team": "JAC",
        "Tier": 3,
        "Bye": 7,
    },
    {
        "Rank": 18,
        "Name": "Ashton Jeanty",
        "Pos": "RB",
        "Team": "LV",
        "Tier": 3,
        "Bye": 10,
    },
    {
        "Rank": 19,
        "Name": "CeeDee Lamb",
        "Pos": "WR",
        "Team": "DAL",
        "Tier": 3,
        "Bye": 14,
    },
    {
        "Rank": 20,
        "Name": "Malik Nabers",
        "Pos": "WR",
        "Team": "NYG",
        "Tier": 3,
        "Bye": 12,
    },
    # TIER 4
    {
        "Rank": 21,
        "Name": "Christian McCaffrey",
        "Pos": "RB",
        "Team": "SF",
        "Tier": 4,
        "Bye": 8,
    },
    {
        "Rank": 22,
        "Name": "Jonathan Taylor",
        "Pos": "RB",
        "Team": "IND",
        "Tier": 4,
        "Bye": 13,
    },
    {
        "Rank": 23,
        "Name": "Dak Prescott",
        "Pos": "QB",
        "Team": "DAL",
        "Tier": 4,
        "Bye": 14,
    },
    {
        "Rank": 24,
        "Name": "Jaxson Dart",
        "Pos": "QB",
        "Team": "NYG",
        "Tier": 4,
        "Bye": 12,
    },
    {
        "Rank": 25,
        "Name": "Brock Purdy",
        "Pos": "QB",
        "Team": "SF",
        "Tier": 4,
        "Bye": 8,
    },
    {
        "Rank": 26,
        "Name": "James Cook",
        "Pos": "RB",
        "Team": "BUF",
        "Tier": 4,
        "Bye": 7,
    },
    {
        "Rank": 27,
        "Name": "Bo Nix",
        "Pos": "QB",
        "Team": "DEN",
        "Tier": 4,
        "Bye": 14,
    },
    {
        "Rank": 28,
        "Name": "Drake London",
        "Pos": "WR",
        "Team": "ATL",
        "Tier": 4,
        "Bye": 11,
    },
    {
        "Rank": 29,
        "Name": "Jordan Love",
        "Pos": "QB",
        "Team": "GB",
        "Tier": 4,
        "Bye": 10,
    },
    {
        "Rank": 30,
        "Name": "Brock Bowers",
        "Pos": "TE",
        "Team": "LV",
        "Tier": 4,
        "Bye": 10,
    },
    # TIER 5
    {
        "Rank": 31,
        "Name": "Marvin Harrison Jr.",
        "Pos": "WR",
        "Team": "ARI",
        "Tier": 5,
        "Bye": 11,
    },
    {
        "Rank": 32,
        "Name": "Breece Hall",
        "Pos": "RB",
        "Team": "NYJ",
        "Tier": 5,
        "Bye": 12,
    },
    {
        "Rank": 33,
        "Name": "Kyler Murray",
        "Pos": "QB",
        "Team": "MIN",
        "Tier": 5,
        "Bye": 6,
    },
    {
        "Rank": 34,
        "Name": "Trey McBride",
        "Pos": "TE",
        "Team": "ARI",
        "Tier": 5,
        "Bye": 11,
    },
    {
        "Rank": 35,
        "Name": "Malik Willis",
        "Pos": "QB",
        "Team": "MIA",
        "Tier": 5,
        "Bye": 6,
    },
    {
        "Rank": 36,
        "Name": "Jared Goff",
        "Pos": "QB",
        "Team": "DET",
        "Tier": 5,
        "Bye": 6,
    },
    {
        "Rank": 37,
        "Name": "Baker Mayfield",
        "Pos": "QB",
        "Team": "TB",
        "Tier": 5,
        "Bye": 11,
    },
    {
        "Rank": 38,
        "Name": "C.J. Stroud",
        "Pos": "QB",
        "Team": "HOU",
        "Tier": 5,
        "Bye": 14,
    },
    {
        "Rank": 39,
        "Name": "Colston Loveland",
        "Pos": "TE",
        "Team": "CHI",
        "Tier": 5,
        "Bye": 10,
    },
    {
        "Rank": 40,
        "Name": "Nico Collins",
        "Pos": "WR",
        "Team": "HOU",
        "Tier": 5,
        "Bye": 14,
    },
]

# --- Load Dataset ---
if uploaded_file is not None:
    df_all = pd.read_csv(uploaded_file)
else:
    df_all = pd.DataFrame(DEFAULT_PLAYERS)

# Track State
if "drafted_players" not in st.session_state:
    st.session_state.drafted_players = []
if "my_roster" not in st.session_state:
    st.session_state.my_roster = []

# Sidebar Draft Inputs
st.sidebar.header("Draft Settings")
pick_number = st.sidebar.number_input(
    "Current Pick", min_value=1, max_value=200, value=1
)
user_draft_spot = st.sidebar.number_input(
    "Your Spot (1-10)", min_value=1, max_value=10, value=1
)

if st.sidebar.button("Reset Draft"):
    st.session_state.drafted_players = []
    st.session_state.my_roster = []
    st.rerun()

# Available Players
available_df = df_all[~df_all["Name"].isin(st.session_state.drafted_players)]

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Pick #{pick_number}")

    # Position filters
    positions = st.multiselect(
        "Filter Positions:",
        ["QB", "RB", "WR", "TE"],
        default=["QB", "RB", "WR", "TE"],
    )
    filtered_df = available_df[available_df["Pos"].isin(positions)]

    player_name = st.selectbox(
        "Select Player Drafted:", filtered_df["Name"].tolist()
    )

    b1, b2 = st.columns(2)
    with b1:
        if st.button("Drafted by Other Team"):
            st.session_state.drafted_players.append(player_name)
            st.rerun()
    with b2:
        if st.button("Draft to MY TEAM"):
            st.session_state.drafted_players.append(player_name)
            st.session_state.my_roster.append(player_name)
            st.rerun()

    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("📋 My Roster")
    my_roster_df = df_all[df_all["Name"].isin(st.session_state.my_roster)]

    qbs = len(my_roster_df[my_roster_df["Pos"] == "QB"])
    st.metric("QBs Drafted (Goal: 3)", f"{qbs}/3")
    st.dataframe(
        my_roster_df[["Name", "Pos", "Tier"]],
        use_container_width=True,
        hide_index=True,
    )
