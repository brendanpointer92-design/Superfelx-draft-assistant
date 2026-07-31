import streamlit as st
import pandas as pd
import random

# Page Configuration
st.set_page_config(
    page_title="SuperFlex Draft Companion // FF Draft App",
    page_icon="⚡",
    layout="wide"
)

# Custom Styling to match dark mode aesthetics
st.markdown("""
    <style>
    .stApp {
        background-color: #030712;
        color: #f3f4f6;
    }
    .metric-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        padding: 15px;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for League Teams & Draft Slot
if "team_names" not in st.session_state:
    st.session_state.team_names = [
        "My Team", 
        "Team 2", 
        "Team 3", 
        "Team 4", 
        "Team 5", 
        "Team 6", 
        "Team 7", 
        "Team 8", 
        "Team 9", 
        "Team 10"
    ]

if "user_draft_slot" not in st.session_state:
    st.session_state.user_draft_slot = 1  # 1-indexed draft position for "My Team"

if "team_rosters" not in st.session_state:
    st.session_state.team_rosters = {
        name: [
            {"position": "QB", "player": None},
            {"position": "QB", "player": None},
            {"position": "RB", "player": None},
            {"position": "RB", "player": None},
            {"position": "WR", "player": None},
            {"position": "WR", "player": None},
            {"position": "TE", "player": None},
            {"position": "S-FLX", "player": None},
            {"position": "FLEX", "player": None},
            {"position": "BN", "player": None},
            {"position": "BN", "player": None},
            {"position": "BN", "player": None},
            {"position": "BN", "player": None},
            {"position": "BN", "player": None},
            {"position": "BN", "player": None},
            {"position": "BN", "player": None},
        ] for name in st.session_state.team_names
    }

# Initialize Top 150 Player Pool
if "players" not in st.session_state:
    base_players = [
        {"id": 1, "name": "Josh Allen", "pos": "QB", "team": "BUF", "adp": 1.1, "proj": 363.0, "tier": 1, "bye": 7},
        {"id": 2, "name": "Lamar Jackson", "pos": "QB", "team": "BAL", "adp": 2.8, "proj": 328.0, "tier": 1, "bye": 13},
        {"id": 3, "name": "Drake Maye", "pos": "QB", "team": "NE", "adp": 3.2, "proj": 315.0, "tier": 1, "bye": 11},
        {"id": 4, "name": "Joe Burrow", "pos": "QB", "team": "CIN", "adp": 4.8, "proj": 311.0, "tier": 1, "bye": 6},
        {"id": 5, "name": "Jayden Daniels", "pos": "QB", "team": "WAS", "adp": 6.4, "proj": 315.0, "tier": 1, "bye": 7},
        {"id": 6, "name": "Jalen Hurts", "pos": "QB", "team": "PHI", "adp": 7.2, "proj": 313.0, "tier": 2, "bye": 10},
        {"id": 7, "name": "Bijan Robinson", "pos": "RB", "team": "ATL", "adp": 9.2, "proj": 274.0, "tier": 2, "bye": 11},
        {"id": 8, "name": "Jahmyr Gibbs", "pos": "RB", "team": "DET", "adp": 9.3, "proj": 273.0, "tier": 2, "bye": 6},
        {"id": 9, "name": "Ja'Marr Chase", "pos": "WR", "team": "CIN", "adp": 9.4, "proj": 186.0, "tier": 2, "bye": 6},
        {"id": 10, "name": "Justin Herbert", "pos": "QB", "team": "LAC", "adp": 11.4, "proj": 301.0, "tier": 2, "bye": 7},
        {"id": 11, "name": "Caleb Williams", "pos": "QB", "team": "CHI", "adp": 11.6, "proj": 294.0, "tier": 2, "bye": 10},
        {"id": 12, "name": "Puka Nacua", "pos": "WR", "team": "LAR", "adp": 11.9, "proj": 208.0, "tier": 2, "bye": 11},
        {"id": 13, "name": "Jaxon Smith-Njigba", "pos": "WR", "team": "SEA", "adp": 13.4, "proj": 187.0, "tier": 2, "bye": 11},
        {"id": 14, "name": "Trevor Lawrence", "pos": "QB", "team": "JAC", "adp": 15.0, "proj": 300.0, "tier": 2, "bye": 7},
        {"id": 15, "name": "Dak Prescott", "pos": "QB", "team": "DAL", "adp": 15.4, "proj": 290.0, "tier": 2, "bye": 7},
        {"id": 16, "name": "Amon-Ra St. Brown", "pos": "WR", "team": "DET", "adp": 16.3, "proj": 171.0, "tier": 3, "bye": 6},
        {"id": 17, "name": "Christian McCaffrey", "pos": "RB", "team": "SF", "adp": 17.2, "proj": 241.0, "tier": 3, "bye": 8},
        {"id": 18, "name": "Jonathan Taylor", "pos": "RB", "team": "IND", "adp": 20.5, "proj": 260.0, "tier": 3, "bye": 13},
        {"id": 19, "name": "CeeDee Lamb", "pos": "WR", "team": "DAL", "adp": 21.0, "proj": 163.0, "tier": 3, "bye": 14},
        {"id": 20, "name": "Jaxson Dart", "pos": "QB", "team": "NYG", "adp": 21.2, "proj": 275.0, "tier": 3, "bye": 11},
        {"id": 21, "name": "Brock Purdy", "pos": "QB", "team": "SF", "adp": 21.7, "proj": 282.0, "tier": 3, "bye": 8},
        {"id": 22, "name": "Justin Jefferson", "pos": "WR", "team": "MIN", "adp": 21.7, "proj": 154.0, "tier": 3, "bye": 6},
        {"id": 23, "name": "James Cook III", "pos": "RB", "team": "BUF", "adp": 23.4, "proj": 232.0, "tier": 3, "bye": 7},
        {"id": 24, "name": "Bo Nix", "pos": "QB", "team": "DEN", "adp": 26.0, "proj": 270.0, "tier": 3, "bye": 14},
        {"id": 25, "name": "Patrick Mahomes II", "pos": "QB", "team": "KC", "adp": 27.1, "proj": 310.0, "tier": 3, "bye": 10},
        {"id": 26, "name": "Ashton Jeanty", "pos": "RB", "team": "LV", "adp": 27.5, "proj": 220.0, "tier": 3, "bye": 10},
        {"id": 27, "name": "Drake London", "pos": "WR", "team": "ATL", "adp": 28.8, "proj": 155.0, "tier": 4, "bye": 11},
        {"id": 28, "name": "Matthew Stafford", "pos": "QB", "team": "LAR", "adp": 30.4, "proj": 265.0, "tier": 4, "bye": 11},
        {"id": 29, "name": "A.J. Brown", "pos": "WR", "team": "PHI", "adp": 31.6, "proj": 152.0, "tier": 4, "bye": 10},
        {"id": 30, "name": "De'Von Achane", "pos": "RB", "team": "MIA", "adp": 32.7, "proj": 215.0, "tier": 4, "bye": 6},
        {"id": 31, "name": "Chase Brown", "pos": "RB", "team": "CIN", "adp": 33.0, "proj": 205.0, "tier": 4, "bye": 6},
        {"id": 32, "name": "Brock Bowers", "pos": "TE", "team": "LV", "adp": 33.1, "proj": 190.0, "tier": 4, "bye": 10},
        {"id": 33, "name": "Nico Collins", "pos": "WR", "team": "HOU", "adp": 33.2, "proj": 150.0, "tier": 4, "bye": 14},
        {"id": 34, "name": "Saquon Barkley", "pos": "RB", "team": "PHI", "adp": 33.4, "proj": 216.0, "tier": 4, "bye": 10},
        {"id": 35, "name": "Omarion Hampton", "pos": "RB", "team": "LAC", "adp": 35.0, "proj": 195.0, "tier": 4, "bye": 7},
        {"id": 36, "name": "Jared Goff", "pos": "QB", "team": "DET", "adp": 35.5, "proj": 260.0, "tier": 4, "bye": 6},
        {"id": 37, "name": "George Pickens", "pos": "WR", "team": "DAL", "adp": 37.8, "proj": 145.0, "tier": 4, "bye": 7},
        {"id": 38, "name": "Derrick Henry", "pos": "RB", "team": "BAL", "adp": 39.5, "proj": 240.0, "tier": 4, "bye": 13},
        {"id": 39, "name": "Kyler Murray", "pos": "QB", "team": "ARI", "adp": 39.6, "proj": 258.0, "tier": 4, "bye": 11},
        {"id": 40, "name": "Trey McBride", "pos": "TE", "team": "ARI", "adp": 40.2, "proj": 175.0, "tier": 4, "bye": 11},
        {"id": 41, "name": "Kenneth Walker III", "pos": "RB", "team": "SEA", "adp": 41.0, "proj": 190.0, "tier": 4, "bye": 11},
        {"id": 42, "name": "Rashee Rice", "pos": "WR", "team": "KC", "adp": 42.4, "proj": 142.0, "tier": 4, "bye": 10},
        {"id": 43, "name": "Chris Olave", "pos": "WR", "team": "NO", "adp": 44.0, "proj": 140.0, "tier": 5, "bye": 12},
        {"id": 44, "name": "Jordan Love", "pos": "QB", "team": "GB", "adp": 45.7, "proj": 255.0, "tier": 5, "bye": 10},
        {"id": 45, "name": "Baker Mayfield", "pos": "QB", "team": "TB", "adp": 46.6, "proj": 252.0, "tier": 5, "bye": 11},
        {"id": 46, "name": "DeVonta Smith", "pos": "WR", "team": "PHI", "adp": 46.6, "proj": 138.0, "tier": 5, "bye": 10},
        {"id": 47, "name": "Tyler Shough", "pos": "QB", "team": "NO", "adp": 48.7, "proj": 240.0, "tier": 5, "bye": 12},
        {"id": 48, "name": "Tee Higgins", "pos": "WR", "team": "CIN", "adp": 50.8, "proj": 135.0, "tier": 5, "bye": 6},
        {"id": 49, "name": "Zay Flowers", "pos": "WR", "team": "BAL", "adp": 50.8, "proj": 134.0, "tier": 5, "bye": 13},
        {"id": 50, "name": "Tetairoa McMillan", "pos": "WR", "team": "CAR", "adp": 51.2, "proj": 130.0, "tier": 5, "bye": 11},
        {"id": 51, "name": "Jeremiyah Love", "pos": "RB", "team": "ARI", "adp": 52.0, "proj": 175.0, "tier": 5, "bye": 11},
        {"id": 52, "name": "Kyren Williams", "pos": "RB", "team": "LAR", "adp": 52.9, "proj": 185.0, "tier": 5, "bye": 11},
        {"id": 53, "name": "Josh Jacobs", "pos": "RB", "team": "GB", "adp": 54.0, "proj": 180.0, "tier": 5, "bye": 10},
        {"id": 54, "name": "Sam LaPorta", "pos": "TE", "team": "DET", "adp": 56.0, "proj": 160.0, "tier": 5, "bye": 6},
        {"id": 55, "name": "Mark Andrews", "pos": "TE", "team": "BAL", "adp": 58.0, "proj": 155.0, "tier": 5, "bye": 13},
        *[{"id": i, "name": f"Player {i}", "pos": "WR" if i % 3 == 0 else ("RB" if i % 3 == 1 else "QB"), "team": "FA", "adp": float(i), "proj": float(250 - i), "tier": (i // 25) + 1, "bye": 7} for i in range(56, 151)]
    ]
    st.session_state.players = base_players

if "drafted_log" not in st.session_state:
    st.session_state.drafted_log = []

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if "current_pick" not in st.session_state:
    st.session_state.current_pick = 1

# Helper function to compute snake draft order for a given overall pick number (1-indexed)
def get_team_for_pick(pick_num, user_slot, team_names):
    num_teams = len(team_names)
    round_num = (pick_num - 1) // num_teams + 1
    position_in_round = (pick_num - 1) % num_teams
    
    if round_num % 2 == 1:
        # Odd round: 1 to N
        # user_slot 1 maps to index 0
        idx = (user_slot - 1) + position_in_round
    else:
        # Even round: N down to 1 (snake reverse)
        idx = (user_slot - 1) + (num_teams - 1 - position_in_round)
        
    # Wrap around safely if bounds shift, though standard mapping follows absolute slots
    actual_team_index = idx % num_teams
    return team_names[actual_team_index]

current_round = (st.session_state.current_pick - 1) // len(st.session_state.team_names) + 1
active_on_the_clock = get_team_for_pick(st.session_state.current_pick, st.session_state.user_draft_slot, st.session_state.team_names)

# Helper function to execute a draft pick for a specific team
def execute_draft(player, target_team):
    st.session_state.players = [p for p in st.session_state.players if p["id"] != player["id"]]
    st.session_state.watchlist = [p for p in st.session_state.watchlist if p["id"] != player["id"]]
    
    roster = st.session_state.team_rosters[target_team]
    assigned = False
    
    if player["pos"] == "QB":
        for s in roster:
            if s["position"] == "QB" and not s["player"]:
                s["player"] = player
                assigned = True
                break
        if not assigned:
            for s in roster:
                if s["position"] == "S-FLX" and not s["player"]:
                    s["player"] = player
                    assigned = True
                    break
    else:
        for s in roster:
            if s["position"] == player["pos"] and not s["player"]:
                s["player"] = player
                assigned = True
                break
        if not assigned:
            for s in roster:
                if s["position"] in ["FLEX", "S-FLX"] and not s["player"]:
                    s["player"] = player
                    assigned = True
                    break
                    
    if not assigned:
        for s in roster:
            if s["position"] == "BN" and not s["player"]:
                s["player"] = player
                break
                
    st.session_state.drafted_log.insert(0, {"pick": st.session_state.current_pick, "team": target_team, "player": player})
    st.session_state.current_pick += 1

# AI / Auto-Draft Logic for CPU Teams
def run_auto_pick():
    if not st.session_state.players:
        return
    current_team = get_team_for_pick(st.session_state.current_pick, st.session_state.user_draft_slot, st.session_state.team_names)
    
    # Simple intelligent heuristic: CPU looks for highest projection, slightly prioritizing needs if critical
    # For simplicity and speed, pick top available player by projection
    best_player = max(st.session_state.players, key=lambda x: x["proj"])
    execute_dir = best_player
    execute_draft(execute_dir, current_team)

# --- HEADER ---
col_head1, col_head2, col_head3 = st.columns([3, 2, 1])
with col_head1:
    st.title("⚡ SuperFlex Draft App")
    st.caption("Snake Draft Slot Management & Automated AI Simulation")
with col_head2:
    st.markdown(f"**Round {current_round} • Pick {st.session_state.current_pick}**<br>🟢 On The Clock: **{active_on_the_clock}**", unsafe_allow_html=True)
with col_head3:
    if st.button("🔄 Reset Draft", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.divider()

# --- SIDEBAR: TEAM MANAGEMENT & DRAFT SETTINGS ---
with st.sidebar:
    st.header("⚙️ League Settings")
    
    # Draft Slot Selection
    st.subheader("🎯 My Draft Slot")
    new_slot = st.number_input("Choose Draft Position", min_value=1, max_value=len(st.session_state.team_names), value=st.session_state.user_draft_slot, step=1)
    if new_slot != st.session_state.user_draft_slot:
        st.session_state.user_draft_slot = new_slot
        st.rerun()
        
    st.caption(f"Your team ('{st.session_state.team_names[st.session_state.user_draft_slot - 1]}') picks according to snake order.")
    
    st.divider()
    st.subheader("🤖 Auto-Draft Control")
    if active_on_the_clock != st.session_state.team_names[st.session_state.user_draft_slot - 1]:
        if st.button("Simulate AI Pick (On Clock)", use_container_width=True):
            run_auto_pick()
            st.rerun()
        if st.button("Simulate Rest of Round", use_container_width=True):
            target_round = current_round
            while current_round == target_round and st.session_state.players:
                run_auto_pick()
                current_round = (st.session_state.current_pick - 1) // len(st.session_state.team_names) + 1
            st.rerun()
    else:
        st.info("You are currently on the clock! Make your manual selection from the player pool or use the dropdown.")

    st.divider()
    st.subheader("Edit Team Names")
    updated_names = []
    for i, old_name in enumerate(st.session_state.team_names):
        new_name = st.text_input(f"Team {i+1} (Slot {i+1})", value=old_name, key=f"team_input_{i}")
        updated_names.append(new_name)
        
    if updated_names != st.session_state.team_names:
        new_rosters = {}
        for old, new in zip(st.session_state.team_names, updated_names):
            new_rosters[new] = st.session_state.team_rosters.pop(old)
        st.session_state.team_names = updated_names
        st.session_state.team_rosters = new_rosters

    st.divider()
    st.subheader("🛡️ View Team Rosters")
    selected_view_team = st.selectbox("Select Team to Inspect", st.session_state.team_names)
    
    view_container = st.container(height=250)
    with view_container:
        for slot in st.session_state.team_rosters[selected_view_team]:
            p_name = slot["player"]["name"] if slot["player"] else "Empty"
            p_team = f"({slot['player']['team']})" if slot["player"] else ""
            color = "#3b82f6" if slot["player"] else "#64748b"
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 4px 6px; margin-bottom: 3px; background: #0f172a; border: 1px solid #1e293b; border-radius: 4px; font-size: 11px;">
                    <span style="font-weight: bold; color: #94a3b8; width: 35px;">{slot['position']}</span>
                    <span style="color: {color}; flex-grow: 1; text-align: left; padding-left: 8px;">{p_name} {p_team}</span>
                </div>
            """, unsafe_allow_html=True)

# --- MAIN LAYOUT SETUP ---
main_col, ai_col = st.columns([7, 3])

# --- CENTER COLUMN: PLAYER POOL & CONTROLS ---
with main_col:
    st.subheader("📋 Available Player Pool (Top 150)")
    
    col_f1, col_f2, col_f3 = st.columns([2, 1.5, 1.5])
    with col_f1:
        search_query = st.text_input("Search Player", placeholder="Name or Team...")
    with col_f2:
        selected_pos = st.selectbox("Filter Position", ["ALL", "QB", "RB", "WR", "TE"])
    with col_f3:
        # Default draft target matches whoever is currently on the clock
        active_draft_team = st.selectbox("Draft Pick To Team:", st.session_state.team_names, index=st.session_state.team_names.index(active_on_the_clock) if active_on_the_clock in st.session_state.team_names else 0)

    filtered_players = st.session_state.players
    if selected_pos != "ALL":
        filtered_players = [p for p in filtered_players if p["pos"] == selected_pos]
    if search_query:
        filtered_players = [p for p in filtered_players if search_query.lower() in p["name"].lower() or search_query.lower() in p["team"].lower()]

    pool_container = st.container(height=520)
    with pool_container:
        for player in filtered_players:
            c1, c2, c3, c4, c5, c6 = st.columns([2, 1, 1, 1, 1, 1])
            with c1:
                st.markdown(f"**{player['name']}** <br><span style='font-size:10px; color:#64748b;'>Tier {player['tier']} • Bye {player['bye']}</span>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"`{player['pos']}`")
            with c3:
                st.markdown(f"{player['team']}")
            with c4:
                st.markdown(f"ADP: {player['adp']}")
            with c5:
                st.markdown(f"**{player['proj']}**")
            with c6:
                col_act1, col_act2 = st.columns(2)
                with col_act1:
                    is_watched = any(w["id"] == player["id"] for w in st.session_state.watchlist)
                    if st.button("⭐" if not is_watched else "❌", key=f"star_{player['id']}"):
                        if is_watched:
                            st.session_state.watchlist = [w for w in st.session_state.watchlist if w["id"] != player["id"]]
                        else:
                            st.session_state.watchlist.append(player)
                        st.rerun()
                with col_act2:
                    if st.button("Draft", key=f"draft_{player['id']}"):
                        execute_draft(player, active_draft_team)
                        st.rerun()
            st.divider()

# --- RIGHT COLUMN: AI ADVISOR & DRAFT LOG ---
with ai_col:
    st.subheader("🧠 SuperFlex AI Advisor")
    
    my_team_name = st.session_state.team_names[st.session_state.user_draft_slot - 1]
    user_roster = st.session_state.team_rosters[my_team_name]
    qb_count = sum(1 for s in user_roster if s["position"] == "QB" and s["player"] is not None)
    
    if qb_count == 0 and current_round <= 3:
        advice = f"[{my_team_name}] Early quarterback optimization is vital in Superflex. Secure a tier-1 signal caller now."
    elif qb_count == 1 and current_round <= 6:
        advice = f"[{my_team_name}] Lock down your second starter for the Superflex slot before the quarterback pool thins out."
    else:
        advice = f"[{my_team_name}] Target value drops across running back and wide receiver slots or secure high-upside backups."
        
    st.info(advice)
    
    st.subheader("🕒 Recent Draft Log")
    log_container = st.container(height=330)
    with log_container:
        if not st.session_state.drafted_log:
            st.text("Draft picks will show here.")
        else:
            for log in st.session_state.drafted_log:
                p = log["player"]
                st.markdown(f"**P{log['pick']} ({log['team']})**: {p['name']} ({p['pos']})")
                
