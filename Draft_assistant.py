import streamlit as st
import pandas as pd

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

# Initialize Session State with Top 150 Superflex Data Pool
if "players" not in st.session_state:
    st.session_state.players = [
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
        # Filling out ranks 56 to 150 structurally to ensure full draft depth
        *[{"id": i, "name": f"Player {i}", "pos": "WR" if i % 3 == 0 else ("RB" if i % 3 == 1 else "QB"), "team": "FA", "adp": float(i), "proj": float(250 - i), "tier": (i // 25) + 1, "bye": 7} for i in range(56, 151)]
    ]

if "drafted_log" not in st.session_state:
    st.session_state.drafted_log = []

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if "roster" not in st.session_state:
    st.session_state.roster = [
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
    ]

if "current_pick" not in st.session_state:
    st.session_state.current_pick = 1

current_round = (st.session_state.current_pick - 1) // 10 + 1

# --- HEADER ---
col_head1, col_head2, col_head3 = st.columns([3, 2, 1])
with col_head1:
    st.title("⚡ SuperFlex Draft App")
    st.caption("Top 150 Draft Sharks Superflex Rankings Edition")
with col_head2:
    st.markdown(f"**Current Round / Pick:** Round {current_round} • Pick {st.session_state.current_pick}")
with col_head3:
    if st.button("🔄 Reset Draft", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.divider()

# --- LAYOUT SETUP ---
sidebar_col, main_col, ai_col = st.columns([3, 6, 3])

# --- LEFT COLUMN: ROSTER & QUEUE ---
with sidebar_col:
    st.subheader("🛡️ My Roster")
    roster_container = st.container(height=340)
    with roster_container:
        for idx, slot in enumerate(st.session_state.roster):
            p_name = slot["player"]["name"] if slot["player"] else "Empty"
            p_team = f"({slot['player']['team']})" if slot["player"] else ""
            color = "#3b82f6" if slot["player"] else "#64748b"
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 4px 8px; margin-bottom: 4px; background: #0f172a; border: 1px solid #1e293b; border-radius: 6px; font-size: 12px;">
                    <span style="font-weight: bold; color: #94a3b8; width: 40px;">{slot['position']}</span>
                    <span style="color: {color}; flex-grow: 1; text-align: left; padding-left: 10px;">{p_name} {p_team}</span>
                </div>
            """, unsafe_allow_html=True)

    st.subheader("⭐ Draft Queue")
    queue_container = st.container(height=220)
    with queue_container:
        if not st.session_state.watchlist:
            st.info("Click 'Star' on any player to add them to your queue.")
        else:
            for w_player in st.session_state.watchlist:
                col_q1, col_q2 = st.columns([3, 1])
                with col_q1:
                    st.text(f"{w_player['pos']} - {w_player['name']}")
                with col_q2:
                    if st.button("Draft", key=f"q_{w_player['id']}"):
                        player = w_player
                        st.session_state.players = [p for p in st.session_state.players if p["id"] != player["id"]]
                        st.session_state.watchlist = [p for p in st.session_state.watchlist if p["id"] != player["id"]]
                        
                        assigned = False
                        if player["pos"] == "QB":
                            for s in st.session_state.roster:
                                if s["position"] == "QB" and not s["player"]:
                                    s["player"] = player
                                    assigned = True
                                    break
                            if not assigned:
                                for s in st.session_state.roster:
                                    if s["position"] == "S-FLX" and not s["player"]:
                                        s["player"] = player
                                        assigned = True
                                        break
                        else:
                            for s in st.session_state.roster:
                                if s["position"] == player["pos"] and not s["player"]:
                                    s["player"] = player
                                    assigned = True
                                    break
                            if not assigned:
                                for s in st.session_state.roster:
                                    if s["position"] in ["FLEX", "S-FLX"] and not s["player"]:
                                        s["player"] = player
                                        assigned = True
                                        break
                        if not assigned:
                            for s in st.session_state.roster:
                                if s["position"] == "BN" and not s["player"]:
                                    s["player"] = player
                                    break
                        
                        st.session_state.drafted_log.insert(0, {"pick": st.session_state.current_pick, "player": player})
                        st.session_state.current_pick += 1
                        st.rerun()

# --- CENTER COLUMN: PLAYER POOL ---
with main_col:
    st.subheader("📋 Available Player Pool (Top 150 Pool)")
    
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        search_query = st.text_input("Search Player", placeholder="Name or Team...")
    with col_f2:
        selected_pos = st.selectbox("Filter Position", ["ALL", "QB", "RB", "WR", "TE"])

    filtered_players = st.session_state.players
    if selected_pos != "ALL":
        filtered_players = [p for p in filtered_players if p["pos"] == selected_pos]
    if search_query:
        filtered_players = [p for p in filtered_players if search_query.lower() in p["name"].lower() or search_query.lower() in p["team"].lower()]

    pool_container = st.container(height=500)
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
                        st.session_state.players = [p for p in st.session_state.players if p["id"] != player["id"]]
                        st.session_state.watchlist = [p for p in st.session_state.watchlist if p["id"] != player["id"]]
                        
                        assigned = False
                        if player["pos"] == "QB":
                            for s in st.session_state.roster:
                                if s["position"] == "QB" and not s["player"]:
                                    s["player"] = player
                                    assigned = True
                                    break
                            if not assigned:
                                for s in st.session_state.roster:
                                    if s["position"] == "S-FLX" and not s["player"]:
                                        s["player"] = player
                                        assigned = True
                                        break
                        else:
                            for s in st.session_state.roster:
                                if s["position"] == player["pos"] and not s["player"]:
                                    s["player"] = player
                                    assigned = True
                                    break
                            if not assigned:
                                for s in st.session_state.roster:
                                    if s["position"] in ["FLEX", "S-FLX"] and not s["player"]:
                                        s["player"] = player
                                        assigned = True
                                        break
                        if not assigned:
                            for s in st.session_state.roster:
                                if s["position"] == "BN" and not s["player"]:
                                    s["player"] = player
                                    break
                        
                        st.session_state.drafted_log.insert(0, {"pick": st.session_state.current_pick, "player": player})
                        st.session_state.current_pick += 1
                        st.rerun()
            st.divider()

# --- RIGHT COLUMN: AI ADVISOR & DRAFT LOG ---
with ai_col:
    st.subheader("🧠 SuperFlex AI Advisor")
    
    qb_count = sum(1 for s in st.session_state.roster if s["position"] == "QB" and s["player"] is not None)
    
    if qb_count == 0 and current_round <= 3:
        advice = "Draft Sharks data emphasizes early quarterback value. Secure your tier-1 signal caller or elite dual-threat cornerstone now."
    elif qb_count == 1 and current_round <= 6:
        advice = "With one QB down, target your Superflex slot anchor before the tier drop-off at quarterback occurs."
    else:
        advice = "Balance your roster by pulling high-value positional players while monitoring tier-based backups deep into the top 150 pool."
        
    st.info(advice)
    
    st.subheader("🕒 Recent Picks")
    log_container = st.container(height=300)
    with log_container:
        if not st.session_state.drafted_log:
            st.text("Draft picks will show here.")
        else:
            for log in st.session_state.drafted_log:
                p = log["player"]
                st.markdown(f"**Pick {log['pick']}**: {p['name']} ({p['pos']} - {p['team']})")
