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

# Initialize Session State
if "players" not in st.session_state:
    st.session_state.players = [
        {"id": 1, "name": "Josh Allen", "pos": "QB", "team": "BUF", "adp": 1.2, "proj": 395.4, "tier": 1, "bye": 12},
        {"id": 2, "name": "Patrick Mahomes", "pos": "QB", "team": "KC", "adp": 2.1, "proj": 382.1, "tier": 1, "bye": 6},
        {"id": 3, "name": "Lamar Jackson", "pos": "QB", "team": "BAL", "adp": 3.4, "proj": 375.0, "tier": 1, "bye": 14},
        {"id": 4, "name": "Jalen Hurts", "pos": "QB", "team": "PHI", "adp": 4.0, "proj": 368.5, "tier": 1, "bye": 5},
        {"id": 5, "name": "C.J. Stroud", "pos": "QB", "team": "HOU", "adp": 5.2, "proj": 345.2, "tier": 2, "bye": 14},
        {"id": 6, "name": "Christian McCaffrey", "pos": "RB", "team": "SF", "adp": 5.8, "proj": 330.0, "tier": 1, "bye": 9},
        {"id": 7, "name": "Anthony Richardson", "pos": "QB", "team": "IND", "adp": 6.5, "proj": 340.0, "tier": 2, "bye": 14},
        {"id": 8, "name": "Joe Burrow", "pos": "QB", "team": "CIN", "adp": 7.1, "proj": 338.4, "tier": 2, "bye": 12},
        {"id": 9, "name": "Ceedee Lamb", "pos": "WR", "team": "DAL", "adp": 8.0, "proj": 325.6, "tier": 1, "bye": 7},
        {"id": 10, "name": "Tyreek Hill", "pos": "WR", "team": "MIA", "adp": 9.2, "proj": 318.0, "tier": 1, "bye": 6},
        {"id": 11, "name": "Ja'Marr Chase", "pos": "WR", "team": "CIN", "adp": 10.5, "proj": 312.4, "tier": 1, "bye": 12},
        {"id": 12, "name": "Kyler Murray", "pos": "QB", "team": "ARI", "adp": 12.0, "proj": 315.0, "tier": 2, "bye": 11},
        {"id": 13, "name": "Bijan Robinson", "pos": "RB", "team": "ATL", "adp": 13.1, "proj": 290.2, "tier": 1, "bye": 12},
        {"id": 14, "name": "Breece Hall", "pos": "RB", "team": "NYJ", "adp": 14.2, "proj": 285.5, "tier": 1, "bye": 12},
        {"id": 15, "name": "Dak Prescott", "pos": "QB", "team": "DAL", "adp": 16.0, "proj": 308.1, "tier": 3, "bye": 7},
        {"id": 16, "name": "Amon-Ra St. Brown", "pos": "WR", "team": "DET", "adp": 17.5, "proj": 295.0, "tier": 2, "bye": 5},
        {"id": 17, "name": "Jordan Love", "pos": "QB", "team": "GB", "adp": 19.0, "proj": 299.8, "tier": 3, "bye": 10},
        {"id": 18, "name": "Brock Bowers", "pos": "TE", "team": "LV", "adp": 22.0, "proj": 210.0, "tier": 1, "bye": 10},
        {"id": 19, "name": "Trevor Lawrence", "pos": "QB", "team": "JAX", "adp": 24.5, "proj": 288.0, "tier": 3, "bye": 12},
        {"id": 20, "name": "Sam LaPorta", "pos": "TE", "team": "DET", "adp": 26.0, "proj": 215.4, "tier": 1, "bye": 5}
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
    st.caption("Live Mock & Draft Companion Engine (SF Edition)")
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
                        # Draft logic trigger
                        player = w_player
                        st.session_state.players = [p for p in st.session_state.players if p["id"] != player["id"]]
                        st.session_state.watchlist = [p for p in st.session_state.watchlist if p["id"] != player["id"]]
                        
                        # Assign roster slot
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
    st.subheader("📋 Available Player Pool")
    
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        search_query = st.text_input("Search Player", placeholder="Name or Team...")
    with col_f2:
        selected_pos = st.selectbox("Filter Position", ["ALL", "QB", "RB", "WR", "TE"])

    # Filter logic
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
                        
                        # Assign roster slot
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
        advice = "In Superflex, secure your QB1 early. Elite tier signal-callers provide unmatched positional advantage over starting WRs/RBs."
    elif qb_count == 1 and current_round <= 6:
        advice = "You need a second starter for your Superflex slot. Target Tier 2/3 QBs before the run dries up."
    else:
        advice = "QBs are scarce. Look for elite WR/RB value drops or stash high-upside dual-threat backup QBs."
        
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
                
