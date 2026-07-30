import streamlit as st
import requests

# ==========================================
# 1. SLEEPER API HELPER FUNCTIONS
# ==========================================

@st.cache_data(ttl=86400)
def fetch_sleeper_players():
    """Fetch and cache all NFL players from Sleeper (refreshes once a day)."""
    url = "https://api.sleeper.app/v1/players/nfl"
    response = requests.get(url)
    if response.status_code == 200:
        players = response.json()
        # Map player_id -> Full Name & Metadata
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
    """Fetch user profile by username."""
    url = f"https://api.sleeper.app/v1/user/{username}"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else None

def get_user_leagues(user_id, season="2026"):
    """Fetch user leagues for a given NFL season."""
    url = f"https://api.sleeper.app/v1/user/{user_id}/leagues/nfl/{season}"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else []

def get_league_drafts(league_id):
    """Fetch drafts associated with a league."""
    url = f"https://api.sleeper.app/v1/league/{league_id}/drafts"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else []

def get_draft_picks(draft_id):
    """Fetch all picks made so far in a draft."""
    url = f"https://api.sleeper.app/v1/draft/{draft_id}/picks"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else []

# ==========================================
# 2. STREAMLIT SIDEBAR / SYNC UI
# ==========================================

def render_sleeper_sidebar():
    st.sidebar.header("🏈 Sleeper League Sync")

    # Store picked players in session state
    if "drafted_players" not in st.session_state:
        st.session_state.drafted_players = []

    # Username Input
    username = st.sidebar.text_input("Sleeper Username", value="", placeholder="e.g. SleeperUser")
    season = st.sidebar.text_input("Season", value="2026")

    if username:
        user_data = get_sleeper_user(username)
        if user_data and "user_id" in user_data:
            user_id = user_data["user_id"]
            leagues = get_user_leagues(user_id, season)

            if leagues:
                league_options = {l["name"]: l["league_id"] for l in leagues}
                selected_league_name = st.sidebar.selectbox("Select League", list(league_options.keys()))
                league_id = league_options[selected_league_name]

                # Get Drafts for League
                drafts = get_league_drafts(league_id)
                if drafts:
                    draft_map = {f"Draft {d['draft_id']} ({d['status']})": d["draft_id"] for d in drafts}
                    selected_draft_label = st.sidebar.selectbox("Select Draft Board", list(draft_map.keys()))
                    draft_id = draft_map[selected_draft_label]

                    # Manual Refresh / Sync Button
                    if st.sidebar.button("🔄 Sync Draft Picks Now"):
                        sync_sleeper_draft(draft_id)
                else:
                    st.sidebar.warning("No drafts found for this league.")
            else:
                st.sidebar.warning(f"No leagues found for '{username}' in {season}.")
        else:
            st.sidebar.error("Sleeper user not found.")

def sync_sleeper_draft(draft_id):
    """Fetch live picks from Sleeper and update session state."""
    with st.spinner("Fetching live Sleeper picks..."):
        all_players = fetch_sleeper_players()
        picks = get_draft_picks(draft_id)

        drafted = []
        for p in picks:
            pid = p.get("player_id")
            player_info = all_players.get(pid, {})
            player_name = player_info.get("name", f"Unknown Player ({pid})")
            
            drafted.append({
                "round": p.get("round"),
                "pick_no": p.get("pick_no"),
                "player_id": pid,
                "player_name": player_name,
                "position": player_info.get("position"),
                "team": player_info.get("team"),
                "picked_by": p.get("picked_by")
            })

        st.session_state.drafted_players = drafted
        st.sidebar.success(f"Synced {len(drafted)} picks!")

# ==========================================
# 3. MAIN DASHBOARD DISPLAY EXAMPLE
# ==========================================

# Render Sidebar Component
render_sleeper_sidebar()

st.title("Draft Assistant with Live Sleeper Sync")

# Display Drafted Players Table
if st.session_state.drafted_players:
    st.subheader("Drafted Players")
    st.dataframe(st.session_state.drafted_players, use_container_width=True)
else:
    st.info("Enter your Sleeper username in the sidebar and hit **Sync Draft Picks Now** to load live picks.")
    
