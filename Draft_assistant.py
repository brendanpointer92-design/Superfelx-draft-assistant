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
]

ROSTER_TARGETS = {'QB': 2, 'RB': 2, 'WR': 3, 'TE': 1}

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
    st.metric("Your QBs", f"{user_qbs} Drafted")

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
                    # Clean Streamlit container wrapper guarantees buttons stay visible!
                    with st.container(border=True):
                        st.markdown(f"<span class='badge-{s_player['Pos'].lower()}'>{s_player['Pos']}</span> **{s_player['Name']}** ({s_player['Team']})", unsafe_allow_html=True)
                        st.caption(f"Rank #{s_player['Rank']} | Tier {s_player['Tier']}")
                        st.markdown(f"<small style='color: #58a6ff;'>{s_player['Reason']}</small>", unsafe_allow_html=True)
                        st.write("")
                        
                        btn_label = f"Draft to Team {on_the_clock}"
                        if st.button(btn_label, key=f"rec_btn_{s_player['Rank']}", type="primary", use_container_width=True):
                            p_idx = st.session_state.players_df[st.session_state.players_df['Rank'] == s_player['Rank']].index[0]
                            draft_player(p_idx, on_the_clock)
                            st.rerun()
            st.divider()

    # Filters
    col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
    with col_f1:
        search_query = st.text_input("🔍 Search Player", placeholder="Search by name or team...").strip().lower()
    with col_f2:
        pos_filter = st.multiselect("Filter Position", options=['QB', 'RB', 'WR', 'TE', 'DST', 'K'], default=['QB', 'RB', 'WR', 'TE'])
    with col_f3:
        hide_drafted = st.checkbox("Hide Drafted", value=True)

    df = st.session_state.players_df.copy()
    if hide_drafted:
        df = df[df['Drafted'] == False]
    if pos_filter:
        df = df[df['Pos'].isin(pos_filter)]
    if search_query:
        df = df[df['Name'].str.lower().str.contains(search_query) | df['Team'].str.lower().str.contains(search_query)]

    st.write(f"Showing **{len(df)}** players")
    
    # Table headers
    h_rank, h_name, h_pos, h_team, h_act1, h_act2 = st.columns([1, 3, 1, 1, 2, 2])
    h_rank.markdown("**Rank**")
    h_name.markdown("**Player**")
    h_pos.markdown("**Pos**")
    h_team.markdown("**Team**")
    h_act1.markdown("**Draft Action**")
    h_act2.markdown("**Direct Action**")
    st.divider()
    
    # Player Rows
    for idx, row in df.iterrows():
        c_rank, c_name, c_pos, c_team, c_act1, c_act2 = st.columns([1, 3, 1, 1, 2, 2])
        
        c_rank.write(f"#{row['Rank']}")
        c_name.write(f"**{row['Name']}**")
        c_pos.markdown(f"<span class='badge-{row['Pos'].lower()}'>{row['Pos']}</span>", unsafe_allow_html=True)
        c_team.write(f"{row['Team']}")
        
        if not row['Drafted']:
            if current_pick <= max_picks:
                if c_act1.button(f"Draft → Team {on_the_clock}", key=f"otc_{idx}", use_container_width=True):
                    draft_player(idx, on_the_clock)
                    st.rerun()
                if on_the_clock != st.session_state.user_team_num:
                    if c_act2.button("Draft → MY Team", key=f"my_{idx}", use_container_width=True):
                        draft_player(idx, st.session_state.user_team_num)
                        st.rerun()
        else:
            pick_val = int(row['Pick_Num']) if pd.notnull(row['Pick_Num']) else "?"
            c_act1.write(f"✅ Team {row['Drafted_By']} (Pick #{pick_val})")

# -----------------------------------------------------------------------------
# TAB 2: VISUAL DRAFT BOARD
# -----------------------------------------------------------------------------
with tab_board:
    st.subheader("Interactive Draft Grid")
    
    num_teams = st.session_state.num_teams
    num_rounds = st.session_state.num_rounds
    
    drafted_players = st.session_state.players_df[st.session_state.players_df['Drafted'] == True].copy()
    if not drafted_players.empty:
        drafted_players['Pick_Num'] = drafted_players['Pick_Num'].astype(int)
    
    board_cols = st.columns(num_teams)
    for t_idx, col in enumerate(board_cols, start=1):
        label = f"Team {t_idx}"
        if t_idx == st.session_state.user_team_num:
            label += " (YOU)"
        col.markdown(f"**{label}**")

    for r in range(1, num_rounds + 1):
        r_cols = st.columns(num_teams)
        for t in range(1, num_teams + 1):
            if r % 2 == 1:
                p_num = (r - 1) * num_teams + t
            else:
                p_num = (r - 1) * num_teams + (num_teams - t + 1)
            
            match = drafted_players[drafted_players['Pick_Num'] == p_num]
            
            with r_cols[t-1]:
                if not match.empty:
                    player_data = match.iloc[0]
                    p_name = str(player_data['Name'])
                    p_pos = str(player_data['Pos'])
                    p_team = str(player_data['Team'])
                    pos_class = f"draft-card-{p_pos.lower()}"
                    
                    card_html = f"""
                    <div class="draft-card {pos_class}">
                        <b>{p_name}</b><br/>
                        <small>{p_pos} - {p_team} (#{p_num})</small>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                else:
                    card_html = f'<div class="draft-card draft-card-empty"><small>#{p_num}</small></div>'
                    st.markdown(card_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 3: TEAM ROSTERS & BREAKDOWN
# -----------------------------------------------------------------------------
with tab_rosters:
    st.subheader("Team Rosters & Positional Needs")
    
    selected_team_num = st.selectbox(
        "Select Team",
        options=list(range(1, st.session_state.num_teams + 1)),
        format_func=lambda x: f"Team {x}" + (" (YOU)" if x == st.session_state.user_team_num else "")
    )
    
    team_roster = st.session_state.players_df[
        st.session_state.pl
