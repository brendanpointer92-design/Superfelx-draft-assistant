import streamlit as st
import pandas as pd
import requests
import numpy as np

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="2026 10-Team Superflex Fantasy Draft Assistant",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .badge-qb { background-color: #e63946; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    .badge-rb { background-color: #2a9d8f; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    .badge-wr { background-color: #457b9d; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    .badge-te { background-color: #e9c46a; color: #1d3557; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. 10-TEAM SUPERFLEX DEFAULT DATASET (QB PREMIUM VALUATION - 98 PLAYERS)
# -----------------------------------------------------------------------------
DEFAULT_PLAYERS = [
    {"Rank": 1, "Name": "Josh Allen", "Pos": "QB", "Team": "BUF", "Tier": 1, "ProjPts": 427.8, "Bye": 7},
    {"Rank": 2, "Name": "Lamar Jackson", "Pos": "QB", "Team": "BAL", "Tier": 1, "ProjPts": 425.6, "Bye": 13},
    {"Rank": 3, "Name": "Drake Maye", "Pos": "QB", "Team": "NE", "Tier": 1, "ProjPts": 423.4, "Bye": 11},
    {"Rank": 4, "Name": "Joe Burrow", "Pos": "QB", "Team": "CIN", "Tier": 1, "ProjPts": 421.2, "Bye": 6},
    {"Rank": 5, "Name": "Jayden Daniels", "Pos": "QB", "Team": "WAS", "Tier": 2, "ProjPts": 419.0, "Bye": 7},
    {"Rank": 6, "Name": "Jalen Hurts", "Pos": "QB", "Team": "PHI", "Tier": 2, "ProjPts": 416.8, "Bye": 10},
    {"Rank": 7, "Name": "Jahmyr Gibbs", "Pos": "RB", "Team": "DET", "Tier": 2, "ProjPts": 414.6, "Bye": 5},
    {"Rank": 8, "Name": "Bijan Robinson", "Pos": "RB", "Team": "ATL", "Tier": 2, "ProjPts": 412.4, "Bye": 11},
    {"Rank": 9, "Name": "Caleb Williams", "Pos": "QB", "Team": "CHI", "Tier": 2, "ProjPts": 410.2, "Bye": 10},
    {"Rank": 10, "Name": "Ja'Marr Chase", "Pos": "WR", "Team": "CIN", "Tier": 2, "ProjPts": 408.0, "Bye": 6},
    {"Rank": 11, "Name": "Justin Herbert", "Pos": "QB", "Team": "LAC", "Tier": 2, "ProjPts": 405.8, "Bye": 7},
    {"Rank": 12, "Name": "Puka Nacua", "Pos": "WR", "Team": "LAR", "Tier": 3, "ProjPts": 403.6, "Bye": 11},
    {"Rank": 13, "Name": "Trevor Lawrence", "Pos": "QB", "Team": "JAC", "Tier": 3, "ProjPts": 401.4, "Bye": 7},
    {"Rank": 14, "Name": "Jaxon Smith-Njigba", "Pos": "WR", "Team": "SEA", "Tier": 3, "ProjPts": 399.2, "Bye": 11},
    {"Rank": 15, "Name": "Dak Prescott", "Pos": "QB", "Team": "DAL", "Tier": 3, "ProjPts": 397.0, "Bye": 14},
    {"Rank": 16, "Name": "Amon-Ra St. Brown", "Pos": "WR", "Team": "DET", "Tier": 3, "ProjPts": 394.8, "Bye": 6},
    {"Rank": 17, "Name": "Jonathan Taylor", "Pos": "RB", "Team": "IND", "Tier": 3, "ProjPts": 392.6, "Bye": 13},
    {"Rank": 18, "Name": "Brock Purdy", "Pos": "QB", "Team": "SF", "Tier": 3, "ProjPts": 390.4, "Bye": 9},
    {"Rank": 19, "Name": "Christian McCaffrey", "Pos": "RB", "Team": "SF", "Tier": 3, "ProjPts": 388.2, "Bye": 9},
    {"Rank": 20, "Name": "Jaxson Dart", "Pos": "QB", "Team": "NYG", "Tier": 3, "ProjPts": 386.0, "Bye": 8},
    {"Rank": 21, "Name": "CeeDee Lamb", "Pos": "WR", "Team": "DAL", "Tier": 4, "ProjPts": 383.8, "Bye": 14},
    {"Rank": 22, "Name": "James Cook", "Pos": "RB", "Team": "BUF", "Tier": 4, "ProjPts": 381.6, "Bye": 7},
    {"Rank": 23, "Name": "Justin Jefferson", "Pos": "WR", "Team": "MIN", "Tier": 4, "ProjPts": 379.4, "Bye": 6},
    {"Rank": 24, "Name": "Patrick Mahomes II", "Pos": "QB", "Team": "KC", "Tier": 4, "ProjPts": 377.2, "Bye": 6},
    {"Rank": 25, "Name": "Bo Nix", "Pos": "QB", "Team": "DEN", "Tier": 4, "ProjPts": 375.0, "Bye": 14},
    {"Rank": 26, "Name": "Derrick Henry", "Pos": "RB", "Team": "BAL", "Tier": 4, "ProjPts": 372.8, "Bye": 13},
    {"Rank": 27, "Name": "Nico Collins", "Pos": "WR", "Team": "HOU", "Tier": 4, "ProjPts": 370.6, "Bye": 8},
    {"Rank": 28, "Name": "A.J. Brown", "Pos": "WR", "Team": "NE", "Tier": 4, "ProjPts": 368.4, "Bye": 11},
    {"Rank": 29, "Name": "Drake London", "Pos": "WR", "Team": "ATL", "Tier": 4, "ProjPts": 366.2, "Bye": 11},
    {"Rank": 30, "Name": "Matthew Stafford", "Pos": "QB", "Team": "LAR", "Tier": 4, "ProjPts": 364.0, "Bye": 11},
    {"Rank": 31, "Name": "Saquon Barkley", "Pos": "RB", "Team": "PHI", "Tier": 4, "ProjPts": 361.8, "Bye": 10},
    {"Rank": 32, "Name": "Ashton Jeanty", "Pos": "RB", "Team": "LV", "Tier": 4, "ProjPts": 359.6, "Bye": 13},
    {"Rank": 33, "Name": "Brock Bowers", "Pos": "TE", "Team": "LV", "Tier": 5, "ProjPts": 357.4, "Bye": 13},
    {"Rank": 34, "Name": "George Pickens", "Pos": "WR", "Team": "DAL", "Tier": 5, "ProjPts": 355.2, "Bye": 14},
    {"Rank": 35, "Name": "Jared Goff", "Pos": "QB", "Team": "DET", "Tier": 5, "ProjPts": 353.0, "Bye": 6},
    {"Rank": 36, "Name": "Kyler Murray", "Pos": "QB", "Team": "MIN", "Tier": 5, "ProjPts": 350.8, "Bye": 6},
    {"Rank": 37, "Name": "Omarion Hampton", "Pos": "RB", "Team": "LAC", "Tier": 5, "ProjPts": 348.6, "Bye": 7},
    {"Rank": 38, "Name": "Kenneth Walker III", "Pos": "RB", "Team": "KC", "Tier": 5, "ProjPts": 346.4, "Bye": 5},
    {"Rank": 39, "Name": "Trey McBride", "Pos": "TE", "Team": "ARI", "Tier": 5, "ProjPts": 344.2, "Bye": 14},
    {"Rank": 40, "Name": "Chase Brown", "Pos": "RB", "Team": "CIN", "Tier": 5, "ProjPts": 342.0, "Bye": 6},
    {"Rank": 41, "Name": "Rashee Rice", "Pos": "WR", "Team": "KC", "Tier": 5, "ProjPts": 339.8, "Bye": 5},
    {"Rank": 42, "Name": "De'Von Achane", "Pos": "RB", "Team": "MIA", "Tier": 5, "ProjPts": 337.6, "Bye": 6},
    {"Rank": 43, "Name": "Chris Olave", "Pos": "WR", "Team": "NO", "Tier": 5, "ProjPts": 335.4, "Bye": 8},
    {"Rank": 44, "Name": "Jordan Love", "Pos": "QB", "Team": "GB", "Tier": 5, "ProjPts": 333.2, "Bye": 10},
    {"Rank": 45, "Name": "Baker Mayfield", "Pos": "QB", "Team": "TB", "Tier": 5, "ProjPts": 331.0, "Bye": 11},
    {"Rank": 46, "Name": "Tyler Shough", "Pos": "QB", "Team": "NO", "Tier": 5, "ProjPts": 328.8, "Bye": 8},
    {"Rank": 47, "Name": "Tee Higgins", "Pos": "WR", "Team": "CIN", "Tier": 6, "ProjPts": 326.6, "Bye": 6},
    {"Rank": 48, "Name": "Zay Flowers", "Pos": "WR", "Team": "BAL", "Tier": 6, "ProjPts": 324.4, "Bye": 13},
    {"Rank": 49, "Name": "Kyren Williams", "Pos": "RB", "Team": "LAR", "Tier": 6, "ProjPts": 322.2, "Bye": 10},
    {"Rank": 50, "Name": "Devonta Smith", "Pos": "WR", "Team": "PHI", "Tier": 6, "ProjPts": 320.0, "Bye": 10},
    {"Rank": 51, "Name": "Josh Jacobs", "Pos": "RB", "Team": "GB", "Tier": 6, "ProjPts": 317.8, "Bye": 11},
    {"Rank": 52, "Name": "Tetairoa McMillan", "Pos": "WR", "Team": "CAR", "Tier": 6, "ProjPts": 315.6, "Bye": 5},
    {"Rank": 53, "Name": "Emeka Egbuka", "Pos": "WR", "Team": "TB", "Tier": 6, "ProjPts": 313.4, "Bye": 11},
    {"Rank": 54, "Name": "Malik Willis", "Pos": "QB", "Team": "MIA", "Tier": 6, "ProjPts": 311.2, "Bye": 6},
    {"Rank": 55, "Name": "Javonte Williams", "Pos": "RB", "Team": "DAL", "Tier": 6, "ProjPts": 309.0, "Bye": 14},
    {"Rank": 56, "Name": "Colston Loveland", "Pos": "TE", "Team": "CHI", "Tier": 6, "ProjPts": 306.8, "Bye": 10},
    {"Rank": 57, "Name": "Breece Hall", "Pos": "RB", "Team": "NYJ", "Tier": 6, "ProjPts": 304.6, "Bye": 13},
    {"Rank": 58, "Name": "Malik Nabers", "Pos": "WR", "Team": "NYG", "Tier": 6, "ProjPts": 302.4, "Bye": 8},
    {"Rank": 59, "Name": "Jeremiah Love", "Pos": "RB", "Team": "ARI", "Tier": 6, "ProjPts": 300.2, "Bye": 14},
    {"Rank": 60, "Name": "C.J. Stroud", "Pos": "QB", "Team": "HOU", "Tier": 6, "ProjPts": 298.0, "Bye": 8},
    {"Rank": 61, "Name": "Ladd McConkey", "Pos": "WR", "Team": "LAC", "Tier": 7, "ProjPts": 295.8, "Bye": 7},
    {"Rank": 62, "Name": "Jamesion Williams", "Pos": "WR", "Team": "DET", "Tier": 7, "ProjPts": 293.6, "Bye": 6},
    {"Rank": 63, "Name": "Jaylen Waddle", "Pos": "WR", "Team": "DEN", "Tier": 7, "ProjPts": 291.4, "Bye": 10},
    {"Rank": 64, "Name": "Cam Ward", "Pos": "QB", "Team": "TEN", "Tier": 7, "ProjPts": 289.2, "Bye": 9},
    {"Rank": 65, "Name": "Christian Watson", "Pos": "WR", "Team": "GB", "Tier": 7, "ProjPts": 287.0, "Bye": 9},
    {"Rank": 66, "Name": "Travis Etienne Jr.", "Pos": "RB", "Team": "NO", "Tier": 7, "ProjPts": 284.8, "Bye": 8},
    {"Rank": 67, "Name": "Garrett Wilson", "Pos": "WR", "Team": "NYJ", "Tier": 7, "ProjPts": 282.6, "Bye": 13},
    {"Rank": 68, "Name": "Mike Evans", "Pos": "WR", "Team": "TB", "Tier": 7, "ProjPts": 280.4, "Bye": 8},
    {"Rank": 69, "Name": "Cam Skattebo", "Pos": "RB", "Team": "SF", "Tier": 7, "ProjPts": 278.2, "Bye": 8},
    {"Rank": 70, "Name": "Quinshon Judkins", "Pos": "RB", "Team": "CLE", "Tier": 7, "ProjPts": 276.0, "Bye": 11},
    {"Rank": 71, "Name": "Bucky Irving", "Pos": "RB", "Team": "TB", "Tier": 7, "ProjPts": 273.8, "Bye": 10},
    {"Rank": 72, "Name": "Tucker Kraft", "Pos": "TE", "Team": "GB", "Tier": 7, "ProjPts": 271.6, "Bye": 11},
    {"Rank": 73, "Name": "Luther Burden III", "Pos": "WR", "Team": "CHI", "Tier": 7, "ProjPts": 269.4, "Bye": 10},
    {"Rank": 74, "Name": "Daniel Jones", "Pos": "QB", "Team": "IND", "Tier": 7, "ProjPts": 267.2, "Bye": 13},
    {"Rank": 75, "Name": "D'Andre Swift", "Pos": "RB", "Team": "CHI", "Tier": 7, "ProjPts": 265.0, "Bye": 10},
    {"Rank": 76, "Name": "Bryce Young", "Pos": "QB", "Team": "CAR", "Tier": 7, "ProjPts": 262.8, "Bye": 5},
    {"Rank": 77, "Name": "Rome Odunze", "Pos": "WR", "Team": "CHI", "Tier": 7, "ProjPts": 260.6, "Bye": 10},
    {"Rank": 78, "Name": "David Montgomery", "Pos": "RB", "Team": "HOU", "Tier": 7, "ProjPts": 258.4, "Bye": 8},
    {"Rank": 79, "Name": "Drake Maye", "Pos": "QB", "Team": "NE", "Tier": 7, "ProjPts": 256.2, "Bye": 11},
    {"Rank": 80, "Name": "DJ Moore", "Pos": "WR", "Team": "BUF", "Tier": 7, "ProjPts": 254.0, "Bye": 7},
    {"Rank": 81, "Name": "Bhayshul Tuten", "Pos": "RB", "Team": "JAC", "Tier": 7, "ProjPts": 251.8, "Bye": 7},
    {"Rank": 82, "Name": "Jacoby Brissett", "Pos": "QB", "Team": "ARI", "Tier": 7, "ProjPts": 249.6, "Bye": 14},
    {"Rank": 83, "Name": "Tyler Warren", "Pos": "TE", "Team": "IND", "Tier": 7, "ProjPts": 247.4, "Bye": 13},
    {"Rank": 84, "Name": "Jadarian Price", "Pos": "RB", "Team": "SEA", "Tier": 7, "ProjPts": 245.2, "Bye": 11},
    {"Rank": 85, "Name": "Alec Pierce", "Pos": "WR", "Team": "IND", "Tier": 8, "ProjPts": 243.0, "Bye": 13},
    {"Rank": 86, "Name": "Marvin Harrison Jr.", "Pos": "WR", "Team": "ARI", "Tier": 8, "ProjPts": 240.8, "Bye": 14},
    {"Rank": 87, "Name": "Tony Pollard", "Pos": "RB", "Team": "TEN", "Tier": 8, "ProjPts": 238.6, "Bye": 9},
    {"Rank": 88, "Name": "Carnell Tate", "Pos": "WR", "Team": "TEN", "Tier": 8, "ProjPts": 236.4, "Bye": 9},
    {"Rank": 89, "Name": "Jaylen Warren", "Pos": "RB", "Team": "PIT", "Tier": 8, "ProjPts": 234.2, "Bye": 9},
    {"Rank": 90, "Name": "Brian Thomas Jr.", "Pos": "WR", "Team": "JAC", "Tier": 8, "ProjPts": 232.0, "Bye": 7},
    {"Rank": 91, "Name": "DK Metcalf", "Pos": "WR", "Team": "NYG", "Tier": 8, "ProjPts": 229.8, "Bye": 9},
    {"Rank": 92, "Name": "Sam LaPorta", "Pos": "TE", "Team": "DET", "Tier": 8, "ProjPts": 227.6, "Bye": 6},
    {"Rank": 93, "Name": "Rhamondre Stevenson", "Pos": "RB", "Team": "NE", "Tier": 8, "ProjPts": 225.4, "Bye": 11},
    {"Rank": 94, "Name": "Chuba Hubbard", "Pos": "RB", "Team": "CAR", "Tier": 8, "ProjPts": 223.2, "Bye": 5},
    {"Rank": 95, "Name": "TreVeyon Henderson", "Pos": "RB", "Team": "CAR", "Tier": 8, "ProjPts": 221.0, "Bye": 11},
    {"Rank": 96, "Name": "Courtland Sutton", "Pos": "WR", "Team": "DEN", "Tier": 8, "ProjPts": 218.8, "Bye": 7},
    {"Rank": 97, "Name": "Parker Washington", "Pos": "WR", "Team": "JAC", "Tier": 8, "ProjPts": 216.6, "Bye": 7},
    {"Rank": 98, "Name": "J.K. Dobbins", "Pos": "RB", "Team": "LAC", "Tier": 8, "ProjPts": 214.4, "Bye": 10}
]

# -----------------------------------------------------------------------------
# 4. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if 'players_df' not in st.session_state:
    df_init = pd.DataFrame(DEFAULT_PLAYERS)
    df_init['Drafted'] = False
    df_init['Drafted_By'] = None
    df_init['Pick_Num'] = None
    st.session_state.players_df = df_init

if 'num_teams' not in st.session_state: st.session_state.num_teams = 10
if 'num_rounds' not in st.session_state: st.session_state.num_rounds = 15
if 'user_team_num' not in st.session_state: st.session_state.user_team_num = 1
if 'current_pick' not in st.session_state: st.session_state.current_pick = 1
if 'draft_history' not in st.session_state: st.session_state.draft_history = []
if 'is_mock_mode' not in st.session_state: st.session_state.is_mock_mode = False

# -----------------------------------------------------------------------------
# 5. SUPERFLEX VBD CALCULATIONS
# -----------------------------------------------------------------------------
def calculate_vbd(df, te_premium=1.0):
    working_df = df.copy()
    working_df.loc[working_df['Pos'] == 'TE', 'ProjPts'] *= te_premium
    
    baselines = {}
    replacement_ranks = {'QB': 20, 'RB': 25, 'WR': 30, 'TE': 10}
    
    for pos, rank_idx in replacement_ranks.items():
        pos_df = working_df[working_df['Pos'] == pos].sort_values(by='ProjPts', ascending=False)
        if len(pos_df) >= rank_idx:
            baselines[pos] = pos_df.iloc[rank_idx - 1]['ProjPts']
        elif not pos_df.empty:
            baselines[pos] = pos_df.iloc[-1]['ProjPts']
        else:
            baselines[pos] = 0.0
            
    working_df['VBD'] = working_df.apply(lambda row: row['ProjPts'] - baselines.get(row['Pos'], 0.0), axis=1)
    return working_df

# -----------------------------------------------------------------------------
# 6. HELPERS & AUTOMATION
# -----------------------------------------------------------------------------
def draft_player(player_index, team_num):
    st.session_state.players_df.loc[player_index, 'Drafted'] = True
    st.session_state.players_df.loc[player_index, 'Drafted_By'] = int(team_num)
    st.session_state.players_df.loc[player_index, 'Pick_Num'] = int(st.session_state.current_pick)
    st.session_state.draft_history.append((player_index, st.session_state.current_pick))
    st.session_state.current_pick += 1

def undo_last_pick():
    if st.session_state.draft_history:
        last_index, last_pick = st.session_state.draft_history.pop()
        st.session_state.players_df.loc[last_index, 'Drafted'] = False
        st.session_state.players_df.loc[last_index, 'Drafted_By'] = None
        st.session_state.players_df.loc[last_index, 'Pick_Num'] = None
        st.session_state.current_pick = last_pick

def get_on_the_clock_team(pick_num, total_teams):
    round_num = (pick_num - 1) // total_teams + 1
    pick_in_round = (pick_num - 1) % total_teams + 1
    return pick_in_round if round_num % 2 == 1 else total_teams - pick_in_round + 1

# -----------------------------------------------------------------------------
# 7. SIDEBAR COMMAND CENTER & LEAGUE SETTINGS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ 10-Team Superflex Settings")
    st.markdown("*(Superflex Mode: QBs Heavily Valued)*")
    st.session_state.num_teams = st.number_input("Number of Teams", 4, 20, int(st.session_state.num_teams))
    st.session_state.num_rounds = st.number_input("Number of Rounds", 1, 30, int(st.session_state.num_rounds))
    st.session_state.user_team_num = st.selectbox("Your Pick Position", list(range(1, st.session_state.num_teams + 1)))
    
    st.divider()
    te_premium_val = st.slider("TE Premium Bonus Multiplier", 1.0, 2.0, 1.0, 0.5)
    
    st.divider()
    st.subheader("📁 Upload Custom CSV Rankings")
    uploaded_file = st.file_uploader("Upload custom CSV file (Columns required: Rank, Name, Pos, Team, ProjPts)", type=["csv"])
    
    if uploaded_file is not None:
        try:
            custom_df = pd.read_csv(uploaded_file)
            required_cols = ['Rank', 'Name', 'Pos', 'Team', 'ProjPts']
            if all(col in custom_df.columns for col in required_cols):
                if 'Tier' not in custom_df.columns:
                    custom_df['Tier'] = 3
                if 'Bye' not in custom_df.columns:
                    custom_df['Bye'] = 8
                
                custom_df['Drafted'] = False
                custom_df['Drafted_By'] = None
                custom_df['Pick_Num'] = None
                st.session_state.players_df = custom_df
                st.success(f"Successfully loaded {len(custom_df)} players from CSV!")
            else:
                st.error(f"CSV must contain columns: {required_cols}")
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")

    st.divider()
    col_u1, col_u2 = st.columns(2)
    with col_u1:
        if st.button("↩️ Undo", use_container_width=True):
            undo_last_pick()
            st.rerun()
    with col_u2:
        if st.button("🔄 Reset", type="primary", use_container_width=True):
            st.session_state.players_df['Drafted'] = False
            st.session_state.players_df['Drafted_By'] = None
            st.session_state.players_df['Pick_Num'] = None
            st.session_state.current_pick = 1
            st.session_state.draft_history = []
            st.rerun()

st.session_state.players_df = calculate_vbd(st.session_state.players_df, te_premium=te_premium_val)

# -----------------------------------------------------------------------------
# 8. HEADER METRICS STATUS BAR
# -----------------------------------------------------------------------------
current_pick = st.session_state.current_pick
max_picks = st.session_state.num_teams * st.session_state.num_rounds

if current_pick <= max_picks:
    on_the_clock = get_on_the_clock_team(current_pick, st.session_state.num_teams)
    is_user_turn = (on_the_clock == st.session_state.user_team_num)
else:
    on_the_clock = None
    is_user_turn = False

if on_the_clock and on_the_clock != st.session_state.user_team_num and st.session_state.is_mock_mode:
    undrafted_pool = st.session_state.players_df[st.session_state.players_df['Drafted'] == False]
    if not undrafted_pool.empty:
        best_ai_pick = undrafted_pool.sort_values(by='VBD', ascending=False).index[0]
        draft_player(best_ai_pick, on_the_clock)
        st.rerun()

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1: st.metric("Overall Pick", f"#{current_pick}" if current_pick <= max_picks else "Complete")
with col_m2: st.metric("Round / Pick", f"R{(current_pick-1)//st.session_state.num_teams+1} . P{(current_pick-1)%st.session_state.num_teams+1}")
with col_m3: st.metric("On The Clock", f"Team {on_the_clock}" + (" (YOU!) 🎉" if is_user_turn else ""))
with col_m4: 
    mock_toggle = st.toggle("🤖 AI Mock Auto-Pilot", value=st.session_state.is_mock_mode)
    if mock_toggle != st.session_state.is_mock_mode:
        st.session_state.is_mock_mode = mock_toggle
        st.rerun()

st.divider()

# -----------------------------------------------------------------------------
# 9. TABS INTERFACE
# -----------------------------------------------------------------------------
tab_cheat, tab_board, tab_rosters, tab_trade = st.tabs([
    "📋 Cheat Sheet & VBD", "🗺️ Visual Draft Board", "🛡️ Rosters & Bye Tracker", "⚖️ In-Draft Trade Analyzer"
])

with tab_cheat:
    col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
    with col_f1: search_query = st.text_input("🔍 Search Player", placeholder="Search name...").strip().lower()
   
