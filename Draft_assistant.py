import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="10-Team Superflex Standard Draft Assistant",
    page_icon="🏈",
    layout="wide",
)

st.title("🏈 10-Team NFL Superflex Draft Assistant (Standard Scoring)")
st.caption(
    "Live draft tracker tailored for 10-Team Superflex formats using Standard (Non-PPR) FantasyPros Consensus Rankings."
)

# ---------------------------------------------------------
# FANTASYPROS CONSENSUS SUPERFLEX TOP 100 (STANDARD SCORING)
# ---------------------------------------------------------
DEFAULT_PLAYERS = [
    # TIER 1 - Elite QBs & Tier-1 Workhorse RBs
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
        "Name": "Lamar Jackson",
        "Pos": "QB",
        "Team": "BAL",
        "Tier": 1,
        "Bye": 13,
    },
    {
        "Rank": 3,
        "Name": "Drake Maye",
        "Pos": "QB",
        "Team": "NE",
        "Tier": 1,
        "Bye": 11,
    },
    {
        "Rank": 4,
        "Name": "Joe Burrow",
        "Pos": "QB",
        "Team": "CIN",
        "Tier": 1,
        "Bye": 6,
    },
    {
        "Rank": 5,
        "Name": "Jayden Daniels",
        "Pos": "QB",
        "Team": "WAS",
        "Tier": 1,
        "Bye": 7,
    },
    {
        "Rank": 6,
        "Name": "Jalen Hurts",
        "Pos": "QB",
        "Team": "PHI",
        "Tier": 1,
        "Bye": 10,
    },
    {
        "Rank": 7,
        "Name": "Bijan Robinson",
        "Pos": "RB",
        "Team": "ATL",
        "Tier": 1,
        "Bye": 11,
    },
    {
        "Rank": 8,
        "Name": "Jahmyr Gibbs",
        "Pos": "RB",
        "Team": "DET",
        "Tier": 1,
        "Bye": 6,
    },
    {
        "Rank": 9,
        "Name": "Ja'Marr Chase",
        "Pos": "WR",
        "Team": "CIN",
        "Tier": 1,
        "Bye": 6,
    },
    {
        "Rank": 10,
        "Name": "Justin Herbert",
        "Pos": "QB",
        "Team": "LAC",
        "Tier": 1,
        "Bye": 7,
    },
    # TIER 2 - Core Starting QBs & Top Skill Players
    {
        "Rank": 11,
        "Name": "Caleb Williams",
        "Pos": "QB",
        "Team": "CHI",
        "Tier": 2,
        "Bye": 10,
    },
    {
        "Rank": 12,
        "Name": "Christian McCaffrey",
        "Pos": "RB",
        "Team": "SF",
        "Tier": 2,
        "Bye": 8,
    },
    {
        "Rank": 13,
        "Name": "Puka Nacua",
        "Pos": "WR",
        "Team": "LAR",
        "Tier": 2,
        "Bye": 11,
    },
    {
        "Rank": 14,
        "Name": "Jaxon Smith-Njigba",
        "Pos": "WR",
        "Team": "SEA",
        "Tier": 2,
        "Bye": 11,
    },
    {
        "Rank": 15,
        "Name": "Trevor Lawrence",
        "Pos": "QB",
        "Team": "JAC",
        "Tier": 2,
        "Bye": 7,
    },
    {
        "Rank": 16,
        "Name": "Dak Prescott",
        "Pos": "QB",
        "Team": "DAL",
        "Tier": 2,
        "Bye": 14,
    },
    {
        "Rank": 17,
        "Name": "Jonathan Taylor",
        "Pos": "RB",
        "Team": "IND",
        "Tier": 2,
        "Bye": 13,
    },
    {
        "Rank": 18,
        "Name": "Amon-Ra St. Brown",
        "Pos": "WR",
        "Team": "DET",
        "Tier": 2,
        "Bye": 6,
    },
    {
        "Rank": 19,
        "Name": "CeeDee Lamb",
        "Pos": "WR",
        "Team": "DAL",
        "Tier": 2,
        "Bye": 14,
    },
    {
        "Rank": 20,
        "Name": "Jaxson Dart",
        "Pos": "QB",
        "Team": "NYG",
        "Tier": 2,
        "Bye": 12,
    },
    # TIER 3 - Strong QB2s & High-Touch Workhorse RBs
    {
        "Rank": 21,
        "Name": "Brock Purdy",
        "Pos": "QB",
        "Team": "SF",
        "Tier": 3,
        "Bye": 8,
    },
    {
        "Rank": 22,
        "Name": "Justin Jefferson",
        "Pos": "WR",
        "Team": "MIN",
        "Tier": 3,
        "Bye": 6,
    },
    {
        "Rank": 23,
        "Name": "James Cook III",
        "Pos": "RB",
        "Team": "BUF",
        "Tier": 3,
        "Bye": 7,
    },
    {
        "Rank": 24,
        "Name": "Bo Nix",
        "Pos": "QB",
        "Team": "DEN",
        "Tier": 3,
        "Bye": 14,
    },
    {
        "Rank": 25,
        "Name": "Patrick Mahomes II",
        "Pos": "QB",
        "Team": "KC",
        "Tier": 3,
        "Bye": 10,
    },
    {
        "Rank": 26,
        "Name": "Ashton Jeanty",
        "Pos": "RB",
        "Team": "LV",
        "Tier": 3,
        "Bye": 13,
    },
    {
        "Rank": 27,
        "Name": "Derrick Henry",
        "Pos": "RB",
        "Team": "BAL",
        "Tier": 3,
        "Bye": 13,
    },
    {
        "Rank": 28,
        "Name": "De'Von Achane",
        "Pos": "RB",
        "Team": "MIA",
        "Tier": 3,
        "Bye": 6,
    },
    {
        "Rank": 29,
        "Name": "Saquon Barkley",
        "Pos": "RB",
        "Team": "PHI",
        "Tier": 3,
        "Bye": 10,
    },
    {
        "Rank": 30,
        "Name": "Jordan Love",
        "Pos": "QB",
        "Team": "GB",
        "Tier": 3,
        "Bye": 10,
    },
    # TIER 4 - Standard Value RBs & Primary Wideouts
    {
        "Rank": 31,
        "Name": "Breece Hall",
        "Pos": "RB",
        "Team": "NYJ",
        "Tier": 4,
        "Bye": 12,
    },
    {
        "Rank": 32,
        "Name": "Drake London",
        "Pos": "WR",
        "Team": "ATL",
        "Tier": 4,
        "Bye": 11,
    },
    {
        "Rank": 33,
        "Name": "Matthew Stafford",
        "Pos": "QB",
        "Team": "LAR",
        "Tier": 4,
        "Bye": 11,
    },
    {
        "Rank": 34,
        "Name": "A.J. Brown",
        "Pos": "WR",
        "Team": "NE",
        "Tier": 4,
        "Bye": 11,
    },
    {
        "Rank": 35,
        "Name": "Chase Brown",
        "Pos": "RB",
        "Team": "CIN",
        "Tier": 4,
        "Bye": 6,
    },
    {
        "Rank": 36,
        "Name": "Brock Bowers",
        "Pos": "TE",
        "Team": "LV",
        "Tier": 4,
        "Bye": 13,
    },
    {
        "Rank": 37,
        "Name": "Nico Collins",
        "Pos": "WR",
        "Team": "HOU",
        "Tier": 4,
        "Bye": 8,
    },
    {
        "Rank": 38,
        "Name": "Omarion Hampton",
        "Pos": "RB",
        "Team": "LAC",
        "Tier": 4,
        "Bye": 7,
    },
    {
        "Rank": 39,
        "Name": "Jared Goff",
        "Pos": "QB",
        "Team": "DET",
        "Tier": 4,
        "Bye": 6,
    },
    {
        "Rank": 40,
        "Name": "George Pickens",
        "Pos": "WR",
        "Team": "DAL",
        "Tier": 4,
        "Bye": 14,
    },
    # TIER 5 - Tier-2 QBs & Mid-Round Standard Weapons
    {
        "Rank": 41,
        "Name": "Kyler Murray",
        "Pos": "QB",
        "Team": "MIN",
        "Tier": 5,
        "Bye": 6,
    },
    {
        "Rank": 42,
        "Name": "Trey McBride",
        "Pos": "TE",
        "Team": "ARI",
        "Tier": 5,
        "Bye": 14,
    },
    {
        "Rank": 43,
        "Name": "Marvin Harrison Jr.",
        "Pos": "WR",
        "Team": "ARI",
        "Tier": 5,
        "Bye": 11,
    },
    {
        "Rank": 44,
        "Name": "Josh Jacobs",
        "Pos": "RB",
        "Team": "GB",
        "Tier": 5,
        "Bye": 10,
    },
    {
        "Rank": 45,
        "Name": "Kenneth Walker III",
        "Pos": "RB",
        "Team": "SEA",
        "Tier": 5,
        "Bye": 11,
    },
    {
        "Rank": 46,
        "Name": "Kyren Williams",
        "Pos": "RB",
        "Team": "LAR",
        "Tier": 5,
        "Bye": 11,
    },
    {
        "Rank": 47,
        "Name": "Baker Mayfield",
        "Pos": "QB",
        "Team": "TB",
        "Tier": 5,
        "Bye": 11,
    },
    {
        "Rank": 48,
        "Name": "C.J. Stroud",
        "Pos": "QB",
        "Team": "HOU",
        "Tier": 5,
        "Bye": 14,
    },
    {
        "Rank": 49,
        "Name": "Malik Nabers",
        "Pos": "WR",
        "Team": "NYG",
        "Tier": 5,
        "Bye": 12,
    },
    {
        "Rank": 50,
        "Name": "Colston Loveland",
        "Pos": "TE",
        "Team": "CHI",
        "Tier": 5,
        "Bye": 10,
    },
    # TIER 6 - High-TD Potential Skill & QB Targets
    {
        "Rank": 51,
        "Name": "Chuba Hubbard",
        "Pos": "RB",
        "Team": "CAR",
        "Tier": 6,
        "Bye": 11,
    },
    {
        "Rank": 52,
        "Name": "Rhamondre Stevenson",
        "Pos": "RB",
        "Team": "NE",
        "Tier": 6,
        "Bye": 11,
    },
    {
        "Rank": 53,
        "Name": "Terry McLaurin",
        "Pos": "WR",
        "Team": "WAS",
        "Tier": 6,
        "Bye": 7,
    },
    {
        "Rank": 54,
        "Name": "Brian Thomas Jr.",
        "Pos": "WR",
        "Team": "JAC",
        "Tier": 6,
        "Bye": 7,
    },
    {
        "Rank": 55,
        "Name": "Sam Darnold",
        "Pos": "QB",
        "Team": "SEA",
        "Tier": 6,
        "Bye": 11,
    },
    {
        "Rank": 56,
        "Name": "Tua Tagovailoa",
        "Pos": "QB",
        "Team": "MIA",
        "Tier": 6,
        "Bye": 6,
    },
    {
        "Rank": 57,
        "Name": "Travis Etienne Jr.",
        "Pos": "RB",
        "Team": "JAC",
        "Tier": 6,
        "Bye": 7,
    },
    {
        "Rank": 58,
        "Name": "David Montgomery",
        "Pos": "RB",
        "Team": "DET",
        "Tier": 6,
        "Bye": 6,
    },
    {
        "Rank": 59,
        "Name": "Isiah Pacheco",
        "Pos": "RB",
        "Team": "KC",
        "Tier": 6,
        "Bye": 10,
    },
    {
        "Rank": 60,
        "Name": "Devonta Smith",
        "Pos": "WR",
        "Team": "PHI",
        "Tier": 6,
        "Bye": 10,
    },
    # TIER 7 - Core WR2/RB2 Depth & Superflex QBs
    {
        "Rank": 61,
        "Name": "Tee Higgins",
        "Pos": "WR",
        "Team": "CIN",
        "Tier": 7,
        "Bye": 6,
    },
    {
        "Rank": 62,
        "Name": "DK Metcalf",
        "Pos": "WR",
        "Team": "SEA",
        "Tier": 7,
        "Bye": 11,
    },
    {
        "Rank": 63,
        "Name": "Aaron Jones",
        "Pos": "RB",
        "Team": "MIN",
        "Tier": 7,
        "Bye": 6,
    },
    {
        "Rank": 64,
        "Name": "Tony Pollard",
        "Pos": "RB",
        "Team": "TEN",
        "Tier": 7,
        "Bye": 12,
    },
    {
        "Rank": 65,
        "Name": "Will Levis",
        "Pos": "QB",
        "Team": "TEN",
        "Tier": 7,
        "Bye": 12,
    },
    {
        "Rank": 66,
        "Name": "Geno Smith",
        "Pos": "QB",
        "Team": "LV",
        "Tier": 7,
        "Bye": 10,
    },
    {
        "Rank": 67,
        "Name": "DeAndre Hopkins",
        "Pos": "WR",
        "Team": "KC",
        "Tier": 7,
        "Bye": 10,
    },
    {
        "Rank": 68,
        "Name": "George Kittle",
        "Pos": "TE",
        "Team": "SF",
        "Tier": 7,
        "Bye": 8,
    },
    {
        "Rank": 69,
        "Name": "James Conner",
        "Pos": "RB",
        "Team": "ARI",
        "Tier": 7,
        "Bye": 11,
    },
    {
        "Rank": 70,
        "Name": "Brian Robinson Jr.",
        "Pos": "RB",
        "Team": "WAS",
        "Tier": 7,
        "Bye": 7,
    },
    # TIER 8 - Flex Play Options & High upside QBs
    {
        "Rank": 71,
        "Name": "Bryce Young",
        "Pos": "QB",
        "Team": "CAR",
        "Tier": 8,
        "Bye": 11,
    },
    {
        "Rank": 72,
        "Name": "Russell Wilson",
        "Pos": "QB",
        "Team": "PIT",
        "Tier": 8,
        "Bye": 9,
    },
    {
        "Rank": 73,
        "Name": "Jaylen Waddle",
        "Pos": "WR",
        "Team": "MIA",
        "Tier": 8,
        "Bye": 6,
    },
    {
        "Rank": 74,
        "Name": "Zay Flowers",
        "Pos": "WR",
        "Team": "BAL",
        "Tier": 8,
        "Bye": 13,
    },
    {
        "Rank": 75,
        "Name": "D'Andre Swift",
        "Pos": "RB",
        "Team": "CHI",
        "Tier": 8,
        "Bye": 10,
    },
    {
        "Rank": 76,
        "Name": "Najee Harris",
        "Pos": "RB",
        "Team": "PIT",
        "Tier": 8,
        "Bye": 9,
    },
    {
        "Rank": 77,
        "Name": "Rachaad White",
        "Pos": "RB",
        "Team": "TB",
        "Tier": 8,
        "Bye": 11,
    },
    {
        "Rank": 78,
        "Name": "Evan Engram",
        "Pos": "TE",
        "Team": "JAC",
        "Tier": 8,
        "Bye": 7,
    },
    {
        "Rank": 79,
        "Name": "Michael Pittman Jr.",
        "Pos": "WR",
        "Team": "IND",
        "Tier": 8,
        "Bye": 13,
    },
    {
        "Rank": 80,
        "Name": "Xavier Worthy",
        "Pos": "WR",
        "Team": "KC",
        "Tier": 8,
        "Bye": 10,
    },
    # TIER 9 - Standard Bench RBs & Solid WR Targets
    {
        "Rank": 81,
        "Name": "Jonathon Brooks",
        "Pos": "RB",
        "Team": "CAR",
        "Tier": 9,
        "Bye": 11,
    },
    {
        "Rank": 82,
        "Name": "Zach Charbonnet",
        "Pos": "RB",
        "Team": "SEA",
        "Tier": 9,
        "Bye": 11,
    },
    {
        "Rank": 83,
        "Name": "Chris Godwin",
        "Pos": "WR",
        "Team": "TB",
        "Tier": 9,
        "Bye": 11,
    },
    {
        "Rank": 84,
        "Name": "Cooper Kupp",
        "Pos": "WR",
        "Team": "LAR",
        "Tier": 9,
        "Bye": 11,
    },
    {
        "Rank": 85,
        "Name": "Deshaun Watson",
        "Pos": "QB",
        "Team": "CLE",
        "Tier": 9,
        "Bye": 10,
    },
    {
        "Rank": 86,
        "Name": "Daniel Jones",
        "Pos": "QB",
        "Team": "NYG",
        "Tier": 9,
        "Bye": 12,
    },
    {
        "Rank": 87,
        "Name": "Jaylen Warren",
        "Pos": "RB",
        "Team": "PIT",
        "Tier": 9,
        "Bye": 9,
    },
    {
        "Rank": 88,
        "Name": "Nick Chubb",
        "Pos": "RB",
        "Team": "CLE",
        "Tier": 9,
        "Bye": 10,
    },
    {
        "Rank": 89,
        "Name": "Calvin Ridley",
        "Pos": "WR",
        "Team": "TEN",
        "Tier": 9,
        "Bye": 12,
    },
    {
        "Rank": 90,
        "Name": "Christian Kirk",
        "Pos": "WR",
        "Team": "JAC",
        "Tier": 9,
        "Bye": 7,
    },
    # TIER 10 - Late Round Upside & QB3 Targets
    {
        "Rank": 91,
        "Name": "David Njoku",
        "Pos": "TE",
        "Team": "CLE",
        "Tier": 10,
        "Bye": 10,
    },
    {
        "Rank": 92,
        "Name": "Dallas Goedert",
        "Pos": "TE",
        "Team": "PHI",
        "Tier": 10,
        "Bye": 10,
    },
    {
        "Rank": 93,
        "Name": "Javonte Williams",
        "Pos": "RB",
        "Team": "DEN",
        "Tier": 10,
        "Bye": 14,
    },
    {
        "Rank": 94,
        "Name": "Ty Chandler",
        "Pos": "RB",
        "Team": "MIN",
        "Tier": 10,
        "Bye": 6,
    },
    {
        "Rank": 95,
        "Name": "Rondale Moore",
        "Pos": "WR",
        "Team": "ATL",
        "Tier": 10,
        "Bye": 11,
    },
    {
        "Rank": 96,
        "Name": "Keon Coleman",
        "Pos": "WR",
        "Team": "BUF",
        "Tier": 10,
        "Bye": 7,
    },
    {
        "Rank": 97,
        "Name": "Ladd McConkey",
        "Pos": "WR",
        "Team": "LAC",
        "Tier": 10,
        "Bye": 7,
    },
    {
        "Rank": 98,
        "Name": "Sam Howell",
        "Pos": "QB",
        "Team": "SEA",
        "Tier": 10,
        "Bye": 11,
    },
    {
        "Rank": 99,
        "Name": "Jacoby Brissett",
        "Pos": "QB",
        "Team": "NE",
        "Tier": 10,
        "Bye": 11,
    },
    {
        "Rank": 100,
        "Name": "Ray Davis",
        "Pos": "RB",
        "Team": "BUF",
        "Tier": 10,
        "Bye": 7,
    },
]

# --- Optional CSV Upload Sidebar ---
st.sidebar.header("📁 Data Options")
uploaded_file = st.sidebar.file_uploader(
    "Upload Custom FantasyPros CSV", type=["csv"]
)

if uploaded_file is not None:
    df_all = pd.read_csv(uploaded_file)
else:
    df_all = pd.DataFrame(DEFAULT_PLAYERS)

# --- Session State Management ---
if "drafted_players" not in st.session_state:
    st.session_state.drafted_players = []

if "my_roster" not in st.session_state:
    st.session_state.my_roster = []

# --- Sidebar Draft Controls ---
st.sidebar.header("Draft Controls")
pick_number = st.sidebar.number_input(
    "Current Overall Pick", min_value=1, max_value=160, value=1
)
user_draft_spot = st.sidebar.number_input(
    "Your Draft Spot (1-10)", min_value=1, max_value=10, value=1
)


def reset_draft():
    st.session_state.drafted_players = []
    st.session_state.my_roster = []


st.sidebar.button("Reset Draft", on_click=reset_draft)

# Round & Pick Calculations (10-Team Snake)
current_round = ((pick_number - 1) // 10) + 1
current_pick_in_round = ((pick_number - 1) % 10) + 1

is_user_pick = False
if current_round % 2 != 0:  # Odd round
    if current_pick_in_round == user_draft_spot:
        is_user_pick = True
else:  # Even round
    if current_pick_in_round == (11 - user_draft_spot):
        is_user_pick = True

# --- Main App Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(
        f"Round {current_round}, Pick {current_pick_in_round} (Overall: #{pick_number})"
    )
    if is_user_pick:
        st.success("🚨 YOU ARE ON THE CLOCK! 🚨")

    # Available Players Board
    available_df = df_all[
        ~df_all["Name"].isin(st.session_state.drafted_players)
    ]

    st.write("### Draft Player Action")
    selected_player = st.selectbox(
        "Select player taken at this pick:", available_df["Name"].tolist()
    )

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("Drafted by Someone Else"):
            st.session_state.drafted_players.append(selected_player)
            st.rerun()

    with btn_col2:
        if st.button("Draft to MY TEAM"):
            st.session_state.drafted_players.append(selected_player)
            st.session_state.my_roster.append(selected_player)
            st.rerun()

    # Filterable Available Player Table
    st.write("### Top Available Players")
    pos_filter = st.multiselect(
        "Filter Positions:",
        ["QB", "RB", "WR", "TE"],
        default=["QB", "RB", "WR", "TE"],
    )
    filtered_df = available_df[available_df["Pos"].isin(pos_filter)]
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("📋 My Roster Tracker")
    my_roster_df = df_all[df_all["Name"].isin(st.session_state.my_roster)]

    qb_count = len(my_roster_df[my_roster_df["Pos"] == "QB"])
    rb_count = len(my_roster_df[my_roster_df["Pos"] == "RB"])
    wr_count = len(my_roster_df[my_roster_df["Pos"] == "WR"])
    te_count = len(my_roster_df[my_roster_df["Pos"] == "TE"])

    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric("QBs (Goal: 3)", f"{qb_count}/3")
        st.metric("RBs", f"{rb_count}")
    with m_col2:
        st.metric("WRs", f"{wr_count}")
        st.metric("TEs", f"{te_count}")

    st.table(my_roster_df[["Name", "Pos", "Tier", "Bye"]])

    st.markdown("---")
    st.markdown("### 💡 Superflex Advice")
    if qb_count == 0 and current_round >= 2:
        st.warning("⚠️ Target your QB1 soon! QBs standard value is high.")
    elif qb_count == 1 and current_round >= 5:
        st.info("💡 Look for your QB2 in Rounds 5-7 to secure starting depth.")
    elif qb_count >= 2:
        st.success("✅ Solid QB base. Load up on Workhorse RBs and Alpha WRs!")
