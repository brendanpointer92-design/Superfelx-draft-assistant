import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="2026 Fantasy Football Superflex Draft Board",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI, color-coded position badges, and draft board grid
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
    .badge-dst { background-color: #6c757d; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    .badge-k { background-color: #d62828; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    
    .rec-card {
        border: 1px solid #1f6beb;
        background-color: #0d1117;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    
    .draft-card {
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 6px;
        margin-bottom: 6px;
        font-size: 0.85rem;
        background-color: #161b22;
        text-align: center;
        min-height: 52px;
    }
    .draft-card-qb { border-left: 4px solid #e63946; }
    .draft-card-rb { border-left: 4px solid #2a9d8f; }
    .draft-card-wr { border-left: 4px solid #457b9d; }
    .draft-card-te { border-left: 4px solid #e9c46a; }
    .draft-card-dst { border-left: 4px solid #6c757d; }
    .draft-card-k { border-left: 4px solid #d62828; }
    .draft-card-empty { border: 1px dashed #484f58; background-color: transparent; color: #6e7681; }

    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DEFAULT PLAYERS DATASET (Top 100 - Superflex Standard Consensus)
# -----------------------------------------------------------------------------
DEFAULT_PLAYERS = [
    # Tier 1
    {"Rank": 1, "Name": "Josh Allen", "Pos": "QB", "Team": "BUF", "Tier": 1},
    {"Rank": 2, "Name": "Lamar Jackson", "Pos": "QB", "Team": "BAL", "Tier": 1},
    {"Rank": 3, "Name": "Drake Maye", "Pos": "QB", "Team": "NE", "Tier": 1},
    {"Rank": 4, "Name": "Joe Burrow", "Pos": "QB", "Team": "CIN", "Tier": 1},
    # Tier 2
    {"Rank": 5, "Name": "Jayden Daniels", "Pos": "QB", "Team": "WAS", "Tier": 2},
    {"Rank": 6, "Name": "Jalen Hurts", "Pos": "QB", "Team": "PHI", "Tier": 2},
    {"Rank": 7, "Name": "Jahmyr Gibbs", "Pos": "RB", "Team": "DET", "Tier": 2},
    {"Rank": 8, "Name": "Bijan Robinson", "Pos": "RB", "Team": "ATL", "Tier": 2},
    {"Rank": 9, "Name": "Ja'Marr Chase", "Pos": "WR", "Team": "CIN", "Tier": 2},
    {"Rank": 10, "Name": "Caleb Williams", "Pos": "QB", "Team": "CHI", "Tier": 2},
    {"Rank": 11, "Name": "Justin Herbert", "Pos": "QB", "Team": "LAC", "Tier": 2},
    {"Rank": 12, "Name": "Puka Nacua", "Pos": "WR", "Team": "LAR", "Tier": 2},
    # Tier 3
    {"Rank": 13, "Name": "Dak Prescott", "Pos": "QB", "Team": "DAL", "Tier": 3},
    {"Rank": 14, "Name": "Trevor Lawrence", "Pos": "QB", "Team": "JAC", "Tier": 3},
    {"Rank": 15, "Name": "Jaxon Smith-Njigba", "Pos": "WR", "Team": "SEA", "Tier": 3},
    {"Rank": 16, "Name": "Amon-Ra St. Brown", "Pos": "WR", "Team": "DET", "Tier": 3},
    {"Rank": 17, "Name": "Jonathan Taylor", "Pos": "RB", "Team": "IND", "Tier": 3},
    {"Rank": 18, "Name": "Brock Purdy", "Pos": "QB", "Team": "SF", "Tier": 3},
    {"Rank": 19, "Name": "Christian McCaffrey", "Pos": "RB", "Team": "SF", "Tier": 3},
    {"Rank": 20, "Name": "Jaxson Dart", "Pos": "QB", "Team": "NYG", "Tier": 3},
    # Tier 4
    {"Rank": 21, "Name": "CeeDee Lamb", "Pos": "WR", "Team": "DAL", "Tier": 4},
    {"Rank": 22, "Name": "Justin Jefferson", "Pos": "WR", "Team": "MIN", "Tier": 4},
    {"Rank": 23, "Name": "Saquon Barkley", "Pos": "RB", "Team": "PHI", "Tier": 4},
    {"Rank": 24, "Name": "James Cook", "Pos": "RB", "Team": "BUF", "Tier": 4},
    {"Rank": 25, "Name": "Derrick Henry", "Pos": "RB", "Team": "BAL", "Tier": 4},
    {"Rank": 26, "Name": "Malik Nabers", "Pos": "WR", "Team": "NYG", "Tier": 4},
    {"Rank": 27, "Name": "Nico Collins", "Pos": "WR", "Team": "HOU", "Tier": 4},
    {"Rank": 28, "Name": "Brian Thomas Jr.", "Pos": "WR", "Team": "JAC", "Tier": 4},
    {"Rank": 29, "Name": "Patrick Mahomes II", "Pos": "QB", "Team": "KC", "Tier": 4},
    # Tier 5
    {"Rank": 30, "Name": "Brock Bowers", "Pos": "TE", "Team": "LV", "Tier": 5},
    {"Rank": 31, "Name": "Trey McBride", "Pos": "TE", "Team": "ARI", "Tier": 5},
    {"Rank": 32, "Name": "Bo Nix", "Pos": "QB", "Team": "DEN", "Tier": 5},
    {"Rank": 33, "Name": "Kyler Murray", "Pos": "QB", "Team": "MIN", "Tier": 5},
    {"Rank": 34, "Name": "Bucky Irving", "Pos": "RB", "Team": "TB", "Tier": 5},
    {"Rank": 35, "Name": "De'Von Achane", "Pos": "RB", "Team": "MIA", "Tier": 5},
    {"Rank": 36, "Name": "Ashton Jeanty", "Pos": "RB", "Team": "LV", "Tier": 5},
    {"Rank": 37, "Name": "Jordan Love", "Pos": "QB", "Team": "GB", "Tier": 5},
    {"Rank": 38, "Name": "A.J. Brown", "Pos": "WR", "Team": "NE", "Tier": 5},
    {"Rank": 39, "Name": "Drake London", "Pos": "WR", "Team": "ATL", "Tier": 5},
    # Tier 6
    {"Rank": 40, "Name": "George Kittle", "Pos": "TE", "Team": "SF", "Tier": 6},
    {"Rank": 41, "Name": "Josh Jacobs", "Pos": "RB", "Team": "GB", "Tier": 6},
    {"Rank": 42, "Name": "C.J. Stroud", "Pos": "QB", "Team": "HOU", "Tier": 6},
    {"Rank": 43, "Name": "Baker Mayfield", "Pos": "QB", "Team": "TB", "Tier": 6},
    {"Rank": 44, "Name": "Ladd McConkey", "Pos": "WR", "Team": "LAC", "Tier": 6},
    {"Rank": 45, "Name": "Tee Higgins", "Pos": "WR", "Team": "CIN", "Tier": 6},
    {"Rank": 46, "Name": "Garrett Wilson", "Pos": "WR", "Team": "NYJ", "Tier": 6},
    {"Rank": 47, "Name": "Kyren Williams", "Pos": "RB", "Team": "LAR", "Tier": 6},
    {"Rank": 48, "Name": "Kenneth Walker III", "Pos": "RB", "Team": "KC", "Tier": 6},
    {"Rank": 49, "Name": "Tua Tagovailoa", "Pos": "QB", "Team": "MIA", "Tier": 6},
    {"Rank": 50, "Name": "Geno Smith", "Pos": "QB", "Team": "SEA", "Tier": 6},
    # Tier 7
    {"Rank": 51, "Name": "Rashee Rice", "Pos": "WR", "Team": "KC", "Tier": 7},
    {"Rank": 52, "Name": "George Pickens", "Pos": "WR", "Team": "DAL", "Tier": 7},
    {"Rank": 53, "Name": "Omarion Hampton", "Pos": "RB", "Team": "LAC", "Tier": 7},
    {"Rank": 54, "Name": "Chase Brown", "Pos": "RB", "Team": "CIN", "Tier": 7},
    {"Rank": 55, "Name": "Marvin Harrison Jr.", "Pos": "WR", "Team": "ARI", "Tier": 7},
    {"Rank": 56, "Name": "Xavier Worthy", "Pos": "WR", "Team": "KC", "Tier": 7},
    {"Rank": 57, "Name": "David Montgomery", "Pos": "RB", "Team": "DET", "Tier": 7},
    {"Rank": 58, "Name": "Isiah Pacheco", "Pos": "RB", "Team": "KC", "Tier": 7},
    {"Rank": 59, "Name": "Michael Penix Jr.", "Pos": "QB", "Team": "ATL", "Tier": 7},
    {"Rank": 60, "Name": "Bryce Young", "Pos": "QB", "Team": "CAR", "Tier": 7},
    # Tier 8
    {"Rank": 61, "Name": "Colston Loveland", "Pos": "TE", "Team": "CHI", "Tier": 8},
    {"Rank": 62, "Name": "Tucker Kraft", "Pos": "TE", "Team": "GB", "Tier": 8},
    {"Rank": 63, "Name": "Devonta Smith", "Pos": "WR", "Team": "PHI", "Tier": 8},
    {"Rank": 64, "Name": "DK Metcalf", "Pos": "WR", "Team": "SEA", "Tier": 8},
    {"Rank": 65, "Name": "Terry McLaurin", "Pos": "WR", "Team": "WAS", "Tier": 8},
    {"Rank": 66, "Name": "Rhamondre Stevenson", "Pos": "RB", "Team": "NE", "Tier": 8},
    {"Rank": 67, "Name": "Chuba Hubbard", "Pos": "RB", "Team": "CAR", "Tier": 8},
    {"Rank": 68, "Name": "Anthony Richardson", "Pos": "QB", "Team": "IND", "Tier": 8},
    {"Rank": 69, "Name": "Deshaun Watson", "Pos": "QB", "Team": "CLE", "Tier": 8},
    {"Rank": 70, "Name": "J.J. McCarthy", "Pos": "QB", "Team": "MIN", "Tier": 8},
    # Tier 9
    {"Rank": 71, "Name": "James Conner", "Pos": "RB", "Team": "ARI", "Tier": 9},
    {"Rank": 72, "Name": "Tony Pollard", "Pos": "RB", "Team": "TEN", "Tier": 9},
    {"Rank": 73, "Name": "Aaron Jones", "Pos": "RB", "Team": "MIN", "Tier": 9},
    {"Rank": 74, "Name": "DJ Moore", "Pos": "WR", "Team": "CHI", "Tier": 9},
    {"Rank": 75, "Name": "Jaylen Waddle", "Pos": "WR", "Team": "MIA", "Tier": 9},
    {"Rank": 76, "Name": "Chris Olave", "Pos": "WR", "Team": "NO", "Tier": 9},
    {"Rank": 77, "Name": "Zay Flowers", "Pos": "WR", "Team": "BAL", "Tier": 9},
    {"Rank": 78, "Name": "Tyler Warren", "Pos": "TE", "Team": "IND", "Tier": 9},
    {"Rank": 79, "Name": "Sam LaPorta", "Pos": "TE", "Team": "DET", "Tier": 9},
    {"Rank": 80, "Name": "Matthew Stafford", "Pos": "QB", "Team": "LAR", "Tier": 9},
    # Tier 10
    {"Rank": 81, "Name": "Javonte Williams", "Pos": "RB", "Team": "DEN", "Tier": 10},
    {"Rank": 82, "Name": "Rachaad White", "Pos": "RB", "Team": "TB", "Tier": 10},
    {"Rank": 83, "Name": "D'Andre Swift", "Pos": "RB", "Team": "CHI", "Tier": 10},
    {"Rank": 84, "Name": "Tank Dell", "Pos": "WR", "Team": "HOU", "Tier": 10},
    {"Rank": 85, "Name": "Keon Coleman", "Pos": "WR", "Team": "BUF", "Tier": 10},
    {"Rank": 86, "Name": "Rome Odunze", "Pos": "WR", "Team": "CHI", "Tier": 10},
    {"Rank": 87, "Name": "Calvin Ridley", "Pos": "WR", "Team": "TEN", "Tier": 10},
    {"Rank": 88, "Name": "Harold Fannin Jr.", "Pos": "TE", "Team": "CLE", "Tier": 10},
    {"Rank": 89, "Name": "Kyle Pitts Sr.", "Pos": "TE", "Team": "ATL", "Tier": 10},
    {"Rank": 90, "Name": "Aaron Rodgers", "Pos": "QB", "Team": "NYJ", "Tier": 10},
    # Tier 11
    {"Rank": 91, "Name": "Najee Harris", "Pos": "RB", "Team": "PIT", "Tier": 11},
    {"Rank": 92, "Name": "Brian Robinson Jr.", "Pos": "RB", "Team": "WAS", "Tier": 11},
    {"Rank": 93, "Name": "Zach Charbonnet", "Pos": "RB", "Team": "SEA", "Tier": 11},
    {"Rank": 94, "Name": "Christian Kirk", "Pos": "WR", "Team": "JAC", "Tier": 11},
    {"Rank": 95, "Name": "DeMario Douglas", "Pos": "WR", "Team": "NE", "Tier": 11},
    {"Rank": 96, "Name": "Jerry Jeudy", "Pos": "WR", "Team": "CLE", "Tier": 11},
    {"Rank": 97, "Name": "Dalton Kincaid", "Pos": "TE", "Team": "BUF", "Tier": 11},
    {"Rank": 98, "Name": "Travis Kelce", "Pos": "TE", "Team": "KC", "Tier": 11},
    {"Rank": 99, "Name": "Russell Wilson", "Pos": "QB", "Team": "PIT", "Tier": 11},
    {"Rank": 100, "Name": "Will Levis", "Pos": "QB", "Team": "TEN", "Tier": 11},
]

# Target roster construct for Superflex League (1QB, 2RB, 2WR, 1TE, 1FLEX, 1SFLEX)
ROSTER_TARGETS = {
    'QB': 2,   # 1 Starter + 1 Superflex
    'RB': 2,   # Starters
    'WR': 3,   # Starters
    'TE': 1    # Starter
}

# -----------------------------------------------------------------------------
# 3. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if 'players_df' not in st.session_state:
    df_init = pd.DataFrame(DEFAULT_PLAYERS)
    df_init['Drafted'] = False
    df_init['Drafted_By'] = None
    df_init['Pick_Num'] = None
    st.session_state.players_df = df_init

if 'num_teams' not in st.session_state:
    st.session_state.num_teams = 12

if 'num_rounds' not in st.session_state:
    st.session_state.num_rounds = 15

if 'user_team_num' not in st.session_state:
    st.session_state.user_team_num = 1

if 'current_pick' not in st.session_state:
    st.session_state.current_pick = 1

if 'draft_history' not in st.session_state:
    st.session_state.draft_history = []

# -----------------------------------------------------------------------------
# 4. HELPER FUNCTIONS & SUGGESTION ENGINE
# -----------------------------------------------------------------------------
def get_on_the_clock_team(pick_num, total_teams):
    """Calculates team number on the clock using standard snake logic."""
    round_num = (pick_num - 1) // total_teams + 1
    pick_in_round = (pick_num - 1) % total_teams + 1
    if round_num % 2 == 1:
        return pick_in_round
    else:
        return total_teams - pick_in_round + 1

def draft_player(player_index, team_num):
    """Assigns a player to a team and advances the draft."""
    st.session_state.players_df.loc[player_index, 'Drafted'] = True
    st.session_state.players_df.loc[player_index, 'Drafted_By'] = int(team_num)
    st.session_state.players_df.loc[player_index, 'Pick_Num'] = int(st.session_state.current_pick)
    
    st.session_state.draft_history.append((player_index, st.session_state.current_pick))
    st.session_state.current_pick += 1

def undo_last_pick():
    """Undoes the last pick."""
    if st.session_state.draft_history:
        last_index, last_pick = st.session_state.draft_history.pop()
        st.session_state.players_df.loc[last_index, 'Drafted'] = False
        st.session_state.players_df.loc[last_index, 'Drafted_By'] = None
        st.session_state.players_df.loc[last_index, 'Pick_Num'] = None
        st.session_state.current_pick = last_pick

def get_badge_html(pos):
    return f'<span class="badge-{str(pos).lower()}">{str(pos)}</span>'

def evaluate_team_needs(team_num):
    """Evaluates positional need scores (High, Med, Low) based on current roster."""
    roster = st.session_state.players_df[st.session_state.players_df['Drafted_By'] == team_num]
    counts = roster['Pos'].value_counts().to_dict()
    
    needs = {}
    for pos, target in ROSTER_TARGETS.items():
        curr = counts.get(pos, 0)
        if curr < target:
            # Urgent need if missing core starters
            needs[pos] = 2.0 if curr == 0 else 1.2
        elif curr == target:
            needs[pos] = 0.8 # Moderate need for depth/flex
        else:
            needs[pos] = 0.4 # Low need
    return needs

def get_player_suggestions(team_num, top_n=3):
    """Generates player suggestions combining positional need and best available rank."""
    needs = evaluate_team_needs(team_num)
    undrafted = st.session_state.players_df[st.session_state.players_df['Drafted'] == False].copy()
    
    if undrafted.empty:
        return pd.DataFrame()
    
    # Calculate dynamic recommendation score
    undrafted['Need_Multiplier'] = undrafted['Pos'].map(lambda p: needs.get(p, 0.5))
    undrafted['Rec_Score'] = undrafted['Need_Multiplier'] * (105 - undrafted['Rank'])
    
    # Identify best overall player available regardless of need
    best_overall_rank = undrafted['Rank'].min()
    
    # Generate reason flags
    reasons = []
    for idx, row in undrafted.iterrows():
        pos_need = needs.get(row['Pos'], 0.5)
        is_bpa = (row['Rank'] == best_overall_rank)
        
        if is_bpa and pos_need >= 1.2:
            reasons.append("🔥 Best Available & High Positional Need")
        elif is_bpa:
            reasons.append("⭐ Best Player Available (BPA)")
        elif pos_need >= 2.0:
            reasons.append("⚠️ Critical Roster Need")
        elif pos_need >= 1.2:
            reasons.append("🎯 High Positional Need")
        elif row['Tier'] <= 3:
            reasons.append("💎 Elite Tier Remaining")
        else:
            reasons.append("👍 Solid Value Pick")
            
    undrafted['Reason'] = reasons
    return undrafted.sort_values(by='Rec_Score', ascending=False).head(top_n)

# -----------------------------------------------------------------------------
# 5. SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ League Settings")
    
    st.session_state.num_teams = st.number_input("Number of Teams", min_value=4, max_value=20, value=st.session_state.num_teams)
    st.session_state.num_rounds = st.number_input("Number of Rounds", min_value=1, max_value=30, value=st.session_state.num_rounds)
    st.session_state.user_team_num = st.selectbox(
        "Your Pick Position",
        options=list(range(1, st.session_state.num_teams + 1)),
        index=st.session_state.user_team_num - 1
    )
    
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

# -----------------------------------------------------------------------------
# 6. DRAFT STATUS HEADER
# -----------------------------------------------------------------------------
current_pick = st.session_state.current_pick
max_picks = st.session_state.num_teams * st.session_state.num_rounds

if current_pick <= max_picks:
    current_round = (current_pick - 1) // st.session_state.num_teams + 1
    current_pick_in_round = (current_pick - 1) % st.session_state.num_teams + 1
    on_the_clock = get_on_the_clock_team(current_pick, st.session_state.num_teams)
    is_user_turn = (on_the_clock == st.session_state.user_team_num)
else:
    current_round = st.session_state.num_rounds
    current_pick_in_round = st.session_state.num_teams
    on_the_clock = None
    is_user_turn = False

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Overall Pick", f"#{current_pick}" if current_pick <= max_picks else "Complete")
with col_m2:
    st.metric("Round / Pick", f"R{current_round} . P{current_pick_in_round}")
with col_m3:
    clock_label = f"Team {on_the_clock}" if on_the_clock else "Ended"
    if is_user_turn:
        clock_label += " (YOU!) 🎉"
    st.metric("On The Clock", clock_label)
with col_m4:
    user_qbs = len(st.session_state.players_df[
        (st.session_state.players_df['Drafted_By'] == st.session_state.user_team_num) & 
        (st.session_state.players_df['Pos'] == 'QB')
    ])
    st.metric("Your QBs Drafted", f"{user_qbs} QBs")

st.divider()

# -----------------------------------------------------------------------------
# 7. MAIN INTERFACE TABS
# -----------------------------------------------------------------------------
tab_cheat, tab_board, tab_rosters = st.tabs(["📋 Cheat Sheet & Quick Draft", "🗺️ Visual Draft Board", "🛡️ Team Rosters"])

# -----------------------------------------------------------------------------
# TAB 1: CHEAT SHEET & QUICK DRAFT
# -----------------------------------------------------------------------------
with tab_cheat:
    if on_the_clock and current_pick <= max_picks:
        user_turn_text = " *(YOUR TURN)*" if is_user_turn else ""
        st.markdown(f"### 💡 Recommended Targets for **Team {on_the_clock}**{user_turn_text}")
        suggestions = get_player_suggestions(on_the_clock, top_n=3)
        
        if not suggestions.empty:
            s_cols = st.columns(len(suggestions))
            for idx, (_, s_player) in enumerate(suggestions.iterrows()):
                with s_cols[idx]:
                    pos_lower = str(s_player['Pos']).lower()
                    card_html = f"""
                    <div class="rec-card">
                        <span class="badge-{pos_lower}">{s_player['Pos']}</span> <b>{s_player['Name']}</b> ({s_player['Team']})<br/>
                        <small><b>Rank:</b> #{s_player['Rank']} | <b>Tier:</b> {s_player['Tier']}</small><br/>
                        <small style="color: #58a6ff;">{s_player['Reason']}</small>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
    
