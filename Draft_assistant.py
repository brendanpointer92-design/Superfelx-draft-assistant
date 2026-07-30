import streamlit as st
import pandas as pd
import requests

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="2026 Fantasy Football Superflex Draft Board",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with responsive grid and horizontal scroll support for mobile
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
    
    .draft-card {
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 4px;
        margin-bottom: 4px;
        font-size: 0.75rem;
        background-color: #161b22;
        text-align: center;
        min-height: 48px;
        word-wrap: break-word;
    }
    .draft-card-qb { border-left: 4px solid #e63946; }
    .draft-card-rb { border-left: 4px solid #2a9d8f; }
    .draft-card-wr { border-left: 4px solid #457b9d; }
    .draft-card-te { border-left: 4px solid #e9c46a; }
    .draft-card-dst { border-left: 4px solid #6c757d; }
    .draft-card-k { border-left: 4px solid #d62828; }
    .draft-card-empty { border: 1px dashed #484f58; background-color: transparent; color: #6e7681; }

    div[data-testid="stMetricValue"] {
        font-size: 1.3rem;
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

ROSTER_TARGETS = {'QB': 2, 'RB': 2, 'WR': 3, 'TE': 1}

# -----------------------------------------------------------------------------
# 3. SLEEPER API HELPER FUNCTIONS
# -----------------------------------------------------------------------------
@st.cache_data(ttl=86400)
def fetch_sleeper_players():
    url = "https://api.sleeper.app/v1/players/nfl"
    response = requests.get(url)
    if response.status_code == 200:
        players = response.json()
        return {
            pid: {
                "name": f"{p.get('first_name', '')} {p.get('last_name', '')}".strip(),
                "position": p.get("position"),
                "team": p.get("team")
            }
            for pid, p in players.items()
        }
    return {}

def get_sleeper_user(username):
    url = f"https://api.sleeper.app/v1/user/{username}"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else None

def get_user_leagues(user_id, season="2026"):
    url = f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{season}"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else []

def get_league_drafts(league_id):
    url = f"https://api.sleeper.app/v1/league/{league_id}/drafts"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else []

def get_draft_details(draft_id):
    url = f"https://api.sleeper.app/v1/draft/{draft_id}"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else None

def get_draft_picks(draft_id):
    url = f"https://api.sleeper.app/v1/draft/{draft_id}/picks"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else []

# -----------------------------------------------------------------------------
# 4. SESSION STATE INITIALIZATION
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
# 5. DRAFT LOGIC HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def get_on_the_clock_team(pick_num, total_teams):
    round_num = (pick_num - 1) // total_teams + 1
    pick_in_round = (pick_num - 1) % total_teams + 1
    if round_num % 2 == 1:
        return pick_in_round
    else:
        return total_teams - pick_in_round + 1

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

def evaluate_team_needs(team_num):
    roster = st.session_state.players_df[st.session_state.players_df['Drafted_By'] == team_num]
    counts = roster['Pos'].value_counts().to_dict()
    needs = {}
    for pos, target in ROSTER_TARGETS.items():
        curr = counts.get(pos, 0)
        if curr < target:
            needs[pos] = 2.0 if curr == 0 else 1.2
        elif curr == target:
            needs[pos] = 0.8
        else:
            needs[pos] = 0.4
    return needs

def get_player_suggestions(team_num, top_n=3):
    needs = evaluate_team_needs(team_num)
    undrafted = st.session_state.players_df[st.session_state.players_df['Drafted'] == False].copy()
    
    if undrafted.empty:
        return pd.DataFrame()
    
    undrafted['Need_Multiplier'] = undrafted['Pos'].map(lambda p: needs.get(p, 0.5))
    undrafted['Rec_Score'] = undrafted['Need_Multiplier'] * (105 - undrafted['Rank'])
    
    best_overall_rank = undrafted['Rank'].min()
    reasons = []
    for idx, row in undrafted.iterrows():
        pos_need = needs.get(row['Pos'], 0.5)
        is_bpa = (row['Rank'] == best_overall_rank)
        
        if is_bpa and pos_need >= 1.2:
            reasons.append("🔥 Best Available & High Need")
        elif is_bpa:
            reasons.append("⭐ Best Player Available")
        elif pos_need >= 2.0:
            reasons.append("⚠️ Critical Roster Need")
        elif pos_need >= 1.2:
            reasons.append("🎯 High Positional Need")
        else:
            reasons.append("👍 Solid Value Pick")
            
    undrafted['Reason'] = reasons
    return undrafted.sort_values(by='Rec_Score', ascending=False).head(top_n)

def sync_sleeper_draft(draft_id, user_id):
    with st.spinner("Syncing Sleeper picks..."):
        sleeper_players = fetch_sleeper_players()
        draft_info = get_draft_details(draft_id)
        
        if draft_info:
            st.session_state.num_teams = int(draft_info.get("settings", {}).get("teams", st.session_state.num_teams))
            st.session_state.num_rounds = int(draft_info.get("settings", {}).get("rounds", st.session_state.num_rounds))
            draft_order = draft_info.get("draft_order", {})
            if user_id in draft_order:
                st.session_state.user_team_num = int(draft_order[user_id])

        picks = get_draft_picks(draft_id)
        if not picks:
            st.sidebar.info("No picks recorded yet in this draft.")
            return

        st.session_state.players_df['Drafted'] = False
        st.session_state.players_df['Drafted_By'] = None
        st.session_state.players_df['Pick_Num'] = None
        st.session_state.draft_history = []
        
        synced_count = 0
        for p in picks:
            pid = p.get("player_id")
            pick_no = p.get("pick_no")
            draft_slot = p.get("draft_slot")
            
            player_data = sleeper_players.get(pid, {})
            p_name = player_data.get("name", "").strip().lower()
            
            if not p_name:
                continue

            match = st.session_state.players_df[
                st.session_state.players_df['Name'].str.lower() == p_name
            ]
            
            if not match.empty:
                idx = match.index[0]
                st.session_state.players_df.loc[idx, 'Drafted'] = True
                st.session_state.players_df.loc[idx, 'Drafted_By'] = int(draft_slot)
                st.session_state.players_df.loc[idx, 'Pick_Num'] = int(pick_no)
                st.session_state.draft_history.append((idx, pick_no))
                synced_count += 1

        st.session_state.current_pick = len(picks) + 1
        st.sidebar.success(f"Successfully synced {synced_count} picks!")

# -----------------------------------------------------------------------------
# 6. SIDEBAR CONTROLS & SLEEPER INTEGRATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ League Settings")
    st.session_state.num_teams = st.number_input("Number of Teams", min_value=4, max_value=20, value=st.session_state.num_teams)
    st.session_state.num_rounds = st.number_input("Number of Rounds", min_value=1, max_value=30, value=st.session_state.num_rounds)
    st.session_state.user_team_num = st.selectbox(
        "Your Pick Position",
        options=list(range(1, st.session_state.num_teams + 1)),
        index=min(st.session_state.user_team_num - 1, st.session_state.num_teams - 1)
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

    st.divider()
    st.subheader("🏈 Sleeper Live Sync")
    
    sleeper_user = st.text_input("Sleeper Username", placeholder="e.g. SleeperUser")
    season_val = st.text_input("Season Year", value="2026")
    
    if sleeper_user:
        user_info = get_sleeper_user(sleeper_user)
        if user_info and "user_id" in user_info:
            u_id = user_info["user_id"]
            leagues = get_user_leagues(u_id, season_val)
            
           
