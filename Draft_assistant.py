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
# 3. 10-TEAM SUPERFLEX DEFAULT DATASET (QB PREMIUM VALUATION)
# -----------------------------------------------------------------------------
DEFAULT_PLAYERS = [
    {"Rank": 1, "Name": "Josh Allen", "Pos": "QB", "Team": "BUF", "Tier": 1, "ProjPts": 418.0, "Bye": 12},
    {"Rank": 2, "Name": "Lamar Jackson", "Pos": "QB", "Team": "BAL", "Tier": 1, "ProjPts": 405.0, "Bye": 14},
    {"Rank": 3, "Name": "Jalen Hurts", "Pos": "QB", "Team": "PHI", "Tier": 1, "ProjPts": 375.0, "Bye": 5},
    {"Rank": 4, "Name": "Jayden Daniels", "Pos": "QB", "Team": "WAS", "Tier": 1, "ProjPts": 365.0, "Bye": 14},
    {"Rank": 5, "Name": "Joe Burrow", "Pos": "QB", "Team": "CIN", "Tier": 2, "ProjPts": 345.0, "Bye": 12},
    {"Rank": 6, "Name": "Drake Maye", "Pos": "QB", "Team": "NE", "Tier": 2, "ProjPts": 340.0, "Bye": 11},
    {"Rank": 7, "Name": "Caleb Williams", "Pos": "QB", "Team": "CHI", "Tier": 2, "ProjPts": 330.0, "Bye": 7},
    {"Rank": 8, "Name": "Patrick Mahomes II", "Pos": "QB", "Team": "KC", "Tier": 2, "ProjPts": 315.0, "Bye": 6},
    {"Rank": 9, "Name": "Bijan Robinson", "Pos": "RB", "Team": "ATL", "Tier": 2, "ProjPts": 355.0, "Bye": 12},
    {"Rank": 10, "Name": "Justin Herbert", "Pos": "QB", "Team": "LAC", "Tier": 2, "ProjPts": 320.0, "Bye": 5},
    {"Rank": 11, "Name": "Jahmyr Gibbs", "Pos": "RB", "Team": "DET", "Tier": 2, "ProjPts": 340.0, "Bye": 5},
    {"Rank": 12, "Name": "Ja'Marr Chase", "Pos": "WR", "Team": "CIN", "Tier": 2, "ProjPts": 335.0, "Bye": 12},
    {"Rank": 13, "Name": "Justin Jefferson", "Pos": "WR", "Team": "MIN", "Tier": 3, "ProjPts": 330.0, "Bye": 6},
    {"Rank": 14, "Name": "CeeDee Lamb", "Pos": "WR", "Team": "DAL", "Tier": 3, "ProjPts": 325.0, "Bye": 7},
    {"Rank": 15, "Name": "Dak Prescott", "Pos": "QB", "Team": "DAL", "Tier": 3, "ProjPts": 305.0, "Bye": 7},
    {"Rank": 16, "Name": "Brock Purdy", "Pos": "QB", "Team": "SF", "Tier": 3, "ProjPts": 310.0, "Bye": 9},
    {"Rank": 17, "Name": "Puka Nacua", "Pos": "WR", "Team": "LAR", "Tier": 3, "ProjPts": 320.0, "Bye": 6},
    {"Rank": 18, "Name": "Saquon Barkley", "Pos": "RB", "Team": "PHI", "Tier": 3, "ProjPts": 315.0, "Bye": 5},
    {"Rank": 19, "Name": "Jonathan Taylor", "Pos": "RB", "Team": "IND", "Tier": 3, "ProjPts": 310.0, "Bye": 14},
    {"Rank": 20, "Name": "Trevor Lawrence", "Pos": "QB", "Team": "JAC", "Tier": 3, "ProjPts": 295.0, "Bye": 12},
    {"Rank": 21, "Name": "Christian McCaffrey", "Pos": "RB", "Team": "SF", "Tier": 4, "ProjPts": 305.0, "Bye": 9},
    {"Rank": 22, "Name": "Derrick Henry", "Pos": "RB", "Team": "BAL", "Tier": 4, "ProjPts": 290.0, "Bye": 14},
    {"Rank": 23, "Name": "Amon-Ra St. Brown", "Pos": "WR", "Team": "DET", "Tier": 4, "ProjPts": 315.0, "Bye": 5},
    {"Rank": 24, "Name": "Kyler Murray", "Pos": "QB", "Team": "MIN", "Tier": 4, "ProjPts": 295.0, "Bye": 6},
    {"Rank": 25, "Name": "Jordan Love", "Pos": "QB", "Team": "GB", "Tier": 4, "ProjPts": 290.0, "Bye": 10},
    {"Rank": 26, "Name": "Jaxson Dart", "Pos": "QB", "Team": "NYG", "Tier": 4, "ProjPts": 285.0, "Bye": 11},
    {"Rank": 27, "Name": "Bo Nix", "Pos": "QB", "Team": "DEN", "Tier": 4, "ProjPts": 280.0, "Bye": 14},
    {"Rank": 28, "Name": "Malik Nabers", "Pos": "WR", "Team": "NYG", "Tier": 4, "ProjPts": 295.0, "Bye": 11},
    {"Rank": 29, "Name": "Nico Collins", "Pos": "WR", "Team": "HOU", "Tier": 4, "ProjPts": 285.0, "Bye": 14},
    {"Rank": 30, "Name": "James Cook", "Pos": "RB", "Team": "BUF", "Tier": 4, "ProjPts": 280.0, "Bye": 12},
    {"Rank": 31, "Name": "Jaxon Smith-Njigba", "Pos": "WR", "Team": "SEA", "Tier": 5, "ProjPts": 290.0, "Bye": 10},
    {"Rank": 32, "Name": "A.J. Brown", "Pos": "WR", "Team": "NE", "Tier": 5, "ProjPts": 275.0, "Bye": 11},
    {"Rank": 33, "Name": "Brian Thomas Jr.", "Pos": "WR", "Team": "JAC", "Tier": 5, "ProjPts": 275.0, "Bye": 12},
    {"Rank": 34, "Name": "De'Von Achane", "Pos": "RB", "Team": "MIA", "Tier": 5, "ProjPts": 265.0, "Bye": 6},
    {"Rank": 35, "Name": "Ashton Jeanty", "Pos": "RB", "Team": "LV", "Tier": 5, "ProjPts": 260.0, "Bye": 10},
    {"Rank": 36, "Name": "Drake London", "Pos": "WR", "Team": "ATL", "Tier": 5, "ProjPts": 265.0, "Bye": 12},
    {"Rank": 37, "Name": "Bucky Irving", "Pos": "RB", "Team": "TB", "Tier": 5, "ProjPts": 255.0, "Bye": 11},
    {"Rank": 38, "Name": "Brock Bowers", "Pos": "TE", "Team": "LV", "Tier": 5, "ProjPts": 250.0, "Bye": 10},
    {"Rank": 39, "Name": "Trey McBride", "Pos": "TE", "Team": "ARI", "Tier": 5, "ProjPts": 240.0, "Bye": 11},
    {"Rank": 40, "Name": "George Kittle", "Pos": "TE", "Team": "SF", "Tier": 6, "ProjPts": 210.0, "Bye": 9}
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
    with col_f2: pos_filter = st.multiselect("Filter Position", ['QB', 'RB', 'WR', 'TE'], default=['QB', 'RB', 'WR', 'TE'])
    with col_f3: hide_drafted = st.checkbox("Hide Drafted", value=True)

    df_view = st.session_state.players_df.copy()
    if hide_drafted: df_view = df_view[df_view['Drafted'] == False]
    if pos_filter: df_view = df_view[df_view['Pos'].isin(pos_filter)]
    if search_query: df_view = df_view[df_view['Name'].str.lower().str.contains(search_query)]

    df_view = df_view.sort_values(by='VBD', ascending=False)
    
    for idx, row in df_view.head(25).iterrows():
        c1, c2, c3, c4, c5, c6 = st.columns([1, 3, 1, 1, 2, 2])
        c1.write(f"#{row['Rank']}")
        c2.write(f"**{row['Name']}** ({row['Team']})")
        c3.markdown(f"<span class='badge-{row['Pos'].lower()}'>{row['Pos']}</span>", unsafe_allow_html=True)
        c4.write(f"VBD: +{row['VBD']:.1f}")
        
        if not row['Drafted'] and current_pick <= max_picks:
            if c5.button(f"Draft → Team {on_the_clock}", key=f"d_{idx}", use_container_width=True):
                draft_player(idx, on_the_clock)
                st.rerun()
            if on_the_clock != st.session_state.user_team_num:
                if c6.button("Draft → MY Team", key=f"my_{idx}", use_container_width=True):
                    draft_player(idx, st.session_state.user_team_num)
                    st.rerun()
        elif row['Drafted']:
            c5.write(f"✅ Drafted Team {row['Drafted_By']}")

with tab_board:
    st.subheader("Full Draft Grid Board")
    drafted_df = st.session_state.players_df[st.session_state.players_df['Drafted'] == True]
    if not drafted_df.empty:
        summary_board = drafted_df[['Pick_Num', 'Drafted_By', 'Name', 'Pos', 'Team', 'Tier']].sort_values('Pick_Num')
        summary_board.columns = ['Pick', 'Team #', 'Player', 'Pos', 'NFL Team', 'Tier']
        st.dataframe(summary_board, hide_index=True, use_container_width=True)
    else:
        st.info("No picks recorded yet.")

with tab_rosters:
    st.subheader("Team Roster & Bye-Week Matrix")
    sel_team = st.selectbox("Select Team to Inspect", list(range(1, st.session_state.num_teams + 1)))
    team_roster = st.session_state.players_df[st.session_state.players_df['Drafted_By'] == sel_team]
    
    if not team_roster.empty:
        st.dataframe(team_roster[['Pick_Num', 'Name', 'Pos', 'Team', 'Bye', 'ProjPts']], hide_index=True, use_container_width=True)
        bye_counts = team_roster['Bye'].value_counts()
        heavy_byes = bye_counts[bye_counts >= 2]
        if not heavy_byes.empty:
            for bye_week, count in heavy_byes.items():
                st.warning(f"⚠️ **Bye Week Alert**: You have {count} players on Bye during Week {bye_week}!")
    else:
        st.info(f"Team {sel_team} has no rostered players.")

with tab_trade:
    st.subheader("In-Draft Pick & Player Trade Calculator")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("**Your Side (Giving Up)**")
        give_player = st.selectbox("Select Player to Trade Away", st.session_state.players_df['Name'].tolist(), key='give')
    with col_t2:
        st.markdown("**Receiving Side (Acquiring)**")
        get_player = st.selectbox("Select Player to Acquire", st.session_state.players_df['Name'].tolist(), key='get')
        
    if st.button("Evaluate Trade Fairness", type="primary"):
        p1_val = st.session_state.players_df.loc[st.session_state.players_df['Name'] == give_player, 'ProjPts'].values[0]
        p2_val = st.session_state.players_df.loc[st.session_state.players_df['Name'] == get_player, 'ProjPts'].values[0]
        diff = p2_val - p1_val
        
        if diff > 15:
            st.success(f"🔥 **Smash Accept!** You gain an estimated +{diff:.1f} projected season points.")
        elif diff < -15:
            st.error(f"🛑 **Reject Trade!** You lose an estimated {abs(diff):.1f} projected season points.")
        else:
            st.info(f"⚖️ **Fair Trade.** Minimal impact on projected points (Difference: {diff:+.1f} pts).")
    
