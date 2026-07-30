import random
import time
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Superflex Draft Assistant Pro", page_icon="🏈", layout="wide"
)

# Initialize Session State
if "drafted_ids" not in st.session_state:
    st.session_state.drafted_ids = set()

if "queue_ids" not in st.session_state:
    st.session_state.queue_ids = set()

if "current_pick" not in st.session_state:
    st.session_state.current_pick = 1

if "roster" not in st.session_state:
    st.session_state.roster = {
        "QB": [],
        "RB": [],
        "WR": [],
        "TE": [],
        "FLEX": [],
        "SUPERFLEX": [],
        "BN": [],
    }

if "auto_draft_history" not in st.session_state:
    st.session_state.auto_draft_history = []

# Sidebar League Settings
st.sidebar.header("⚙️ League Settings")
team_name = st.sidebar.text_input("Your Team Name", "Gridiron Greats")
league_size = 10  # Standard 10-team league

# Pick position calculation from draft slot string
draft_slot_options = [f"Pick {i}" for i in range(1, league_size + 1)]
selected_slot_str = st.sidebar.selectbox(
    "Select Your Draft Slot", draft_slot_options
)
user_draft_slot = int(selected_slot_str.replace("Pick ", ""))

st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Simulation & Auto-Draft")
auto_draft_enabled = st.sidebar.toggle(
    "Enable Auto-Draft Automation",
    value=False,
    help="When turned on, the app automatically runs simulated picks for opposing teams round-by-round.",
)
auto_speed = st.sidebar.slider(
    "Auto-Draft Speed (seconds)", 0.5, 3.0, 1.0, 0.5
)


# Comprehensive 150-Player Database based on Superflex Rankings
@st.cache_data
def load_150_players():
    base_players = [
        {"id": 1, "name": "Josh Allen", "pos": "QB", "team": "BUF", "bye": 7},
        {"id": 2, "name": "Lamar Jackson", "pos": "QB", "team": "BAL", "bye": 13},
        {"id": 3, "name": "Drake Maye", "pos": "QB", "team": "NE", "bye": 11},
        {"id": 4, "name": "Joe Burrow", "pos": "QB", "team": "CIN", "bye": 6},
        {"id": 5, "name": "Jayden Daniels", "pos": "QB", "team": "WAS", "bye": 7},
        {"id": 6, "name": "Jalen Hurts", "pos": "QB", "team": "PHI", "bye": 10},
        {"id": 7, "name": "Bijan Robinson", "pos": "RB", "team": "ATL", "bye": 11},
        {"id": 8, "name": "Jahmyr Gibbs", "pos": "RB", "team": "DET", "bye": 6},
        {"id": 9, "name": "Ja'Marr Chase", "pos": "WR", "team": "CIN", "bye": 6},
        {"id": 10, "name": "Justin Herbert", "pos": "QB", "team": "LAC", "bye": 7},
        {"id": 11, "name": "Caleb Williams", "pos": "QB", "team": "CHI", "bye": 10},
        {"id": 12, "name": "Puka Nacua", "pos": "WR", "team": "LAR", "bye": 11},
        {
            "id": 13,
            "name": "Jaxon Smith-Njigba",
            "pos": "WR",
            "team": "SEA",
            "bye": 11,
        },
        {
            "id": 14,
            "name": "Trevor Lawrence",
            "pos": "QB",
            "team": "JAC",
            "bye": 7,
        },
        {"id": 15, "name": "Dak Prescott", "pos": "QB", "team": "DAL", "bye": 14},
        {
            "id": 16,
            "name": "Amon-Ra St. Brown",
            "pos": "WR",
            "team": "DET",
            "bye": 6,
        },
        {
            "id": 17,
            "name": "Christian McCaffrey",
            "pos": "RB",
            "team": "SF",
            "bye": 8,
        },
        {
            "id": 18,
            "name": "Jonathan Taylor",
            "pos": "RB",
            "team": "IND",
            "bye": 13,
        },
        {"id": 19, "name": "CeeDee Lamb", "pos": "WR", "team": "DAL", "bye": 14},
        {"id": 20, "name": "Jaxson Dart", "pos": "QB", "team": "NYG", "bye": 8},
        {"id": 21, "name": "Brock Purdy", "pos": "QB", "team": "SF", "bye": 8},
        {"id": 22, "name": "Justin Jefferson", "pos": "WR", "team": "MIN", "bye": 6},
        {"id": 23, "name": "James Cook III", "pos": "RB", "team": "BUF", "bye": 7},
        {"id": 24, "name": "Bo Nix", "pos": "QB", "team": "DEN", "bye": 10},
        {
            "id": 25,
            "name": "Patrick Mahomes II",
            "pos": "QB",
            "team": "KC",
            "bye": 5,
        },
        {"id": 26, "name": "Ashton Jeanty", "pos": "RB", "team": "LVR", "bye": 13},
        {"id": 27, "name": "Drake London", "pos": "WR", "team": "ATL", "bye": 11},
        {
            "id": 28,
            "name": "Matthew Stafford",
            "pos": "QB",
            "team": "LAR",
            "bye": 11,
        },
        {"id": 29, "name": "A.J. Brown", "pos": "WR", "team": "NE", "bye": 11},
        {"id": 30, "name": "De'Von Achane", "pos": "RB", "team": "MIA", "bye": 6},
        {"id": 31, "name": "Chase Brown", "pos": "RB", "team": "CIN", "bye": 6},
        {"id": 32, "name": "Brock Bowers", "pos": "TE", "team": "LVR", "bye": 13},
        {"id": 33, "name": "Nico Collins", "pos": "WR", "team": "HOU", "bye": 8},
        {"id": 34, "name": "Saquon Barkley", "pos": "RB", "team": "PHI", "bye": 10},
        {
            "id": 35,
            "name": "Omarion Hampton",
            "pos": "RB",
            "team": "LAC",
            "bye": 7,
        },
        {"id": 36, "name": "Jared Goff", "pos": "QB", "team": "DET", "bye": 6},
        {"id": 37, "name": "George Pickens", "pos": "WR", "team": "DAL", "bye": 14},
        {"id": 38, "name": "Derrick Henry", "pos": "RB", "team": "BAL", "bye": 13},
        {"id": 39, "name": "Kyler Murray", "pos": "QB", "team": "MIN", "bye": 6},
        {"id": 40, "name": "Trey McBride", "pos": "TE", "team": "ARI", "bye": 14},
        {
            "id": 41,
            "name": "Kenneth Walker III",
            "pos": "RB",
            "team": "KC",
            "bye": 5,
        },
        {"id": 42, "name": "Rashee Rice", "pos": "WR", "team": "KC", "bye": 5},
        {"id": 43, "name": "Chris Olave", "pos": "WR", "team": "NO", "bye": 8},
        {"id": 44, "name": "Jordan Love", "pos": "QB", "team": "GB", "bye": 11},
        {"id": 45, "name": "Baker Mayfield", "pos": "QB", "team": "TB", "bye": 18},
        {"id": 46, "name": "DeVonta Smith", "pos": "WR", "team": "PHI", "bye": 10},
        {"id": 47, "name": "Tyler Shough", "pos": "QB", "team": "NO", "bye": 8},
        {"id": 48, "name": "Tee Higgins", "pos": "WR", "team": "CIN", "bye": 6},
        {"id": 49, "name": "Zay Flowers", "pos": "WR", "team": "BAL", "bye": 13},
        {
            "id": 50,
            "name": "Tetairoa McMillan",
            "pos": "WR",
            "team": "CAR",
            "bye": 5,
        },
    ]

    first_names = [
        "Marcus",
        "Brandon",
        "Tyler",
        "Jordan",
        "Aaron",
        "Austin",
        "Caleb",
        "Justin",
        "Kyle",
        "Kevin",
        "Brian",
        "Xavier",
        "Trevor",
        "DeVonta",
    ]
    last_names = [
        "Henderson",
        "Cooper",
        "Meyers",
        "Pittman",
        "Sutton",
        "Hollywood",
        "Diontae",
        "Godwin",
        "Kirk",
        "Zamir",
        "Allgeier",
        "Singletary",
        "Dowdle",
        "Chubb",
        "Mostert",
    ]
    nfl_teams = [
        "BUF",
        "MIA",
        "NE",
        "NYJ",
        "BAL",
        "CIN",
        "CLE",
        "PIT",
        "HOU",
        "IND",
        "JAX",
        "TEN",
        "DEN",
        "KC",
        "LV",
        "LAC",
        "DAL",
        "NYG",
        "PHI",
        "WAS",
        "CHI",
        "DET",
        "GB",
        "MIN",
        "ATL",
        "CAR",
        "NO",
        "TB",
        "ARI",
        "LAR",
        "SF",
        "SEA",
    ]
    positions = ["RB", "WR", "QB", "TE"]

    current_id = len(base_players) + 1
    while len(base_players) < 150:
        pos = random.choices(positions, weights=[33, 42, 17, 8], k=1)[0]
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        base_players.append(
            {
                "id": current_id,
                "name": name,
                "pos": pos,
                "team": random.choice(nfl_teams),
                "bye": random.randint(5, 14),
            }
        )
        current_id += 1

    return pd.DataFrame(base_players)


df_players = load_150_players()

# App Header
st.title(f"🏈 Superflex Draft Assistant: {team_name}")


# Function to calculate whose turn it is based on snake draft logic
def get_current_picker(pick_num, user_slot, num_teams):
    round_num = (pick_num - 1) // num_teams + 1
    pos_in_round = (pick_num - 1) % num_teams + 1

    if round_num % 2 == 1:
        # Odd rounds (1, 3, 5...) go 1 -> 10
        picking_team_slot = pos_in_round
    else:
        # Even rounds (2, 4, 6...) snake back 10 -> 1
        picking_team_slot = num_teams - pos_in_round + 1

    is_user = picking_team_slot == user_slot
    return round_num, picking_team_slot, is_user


current_pick = len(st.session_state.drafted_ids) + 1
round_n, current_slot, is_user_turn = get_current_picker(
    current_pick, user_draft_slot, league_size
)

# Top Status Indicator Bar
status_col1, status_col2, status_col3 = st.columns(3)
status_col1.metric("Current Overall Pick", f"#{current_pick}")
status_col2.metric("Draft Round", f"Round {round_n}")

if is_user_turn:
    status_col3.markdown(
        f"### 🟢 **YOUR TURN!** (Pick {user_draft_slot})"
    )
else:
    status_col3.markdown(
        f"### ⏳ **AI Picking:** Team Slot {current_slot}"
    )

st.markdown("---")

# --- MAIN SCREEN TABS ---
tab_draft, tab_board, tab_roster, tab_log = st.tabs(
    ["🎯 Draft Room", "🏟️ Full Draft Board", "📋 My Roster", "🤖 AI Auto-Draft Log"]
)


# Helper function to process drafting a player
def draft_player(p_obj, is_user_pick=True):
    st.session_state.drafted_ids.add(p_obj["id"])
    if p_obj["id"] in st.session_state.queue_ids:
        st.session_state.queue_ids.remove(p_obj["id"])

    if is_user_pick:
        r = st.session_state.roster
        if p_obj["pos"] == "QB" and len(r["QB"]) < 1:
            r["QB"].append(p_obj)
        elif p_obj["pos"] == "RB" and len(r["RB"]) < 2:
            r["RB"].append(p_obj)
        elif p_obj["pos"] == "WR" and len(r["WR"]) < 2:
            r["WR"].append(p_obj)
        elif p_obj["pos"] == "TE" and len(r["TE"]) < 1:
            r["TE"].append(p_obj)
        elif p_obj["pos"] == "QB" and len(r["SUPERFLEX"]) < 1:
            r["SUPERFLEX"].append(p_obj)
        elif p_obj["pos"] in ["RB", "WR", "TE"] and len(r["FLEX"]) < 1:
            r["FLEX"].append(p_obj)
        elif len(r["SUPERFLEX"]) < 1:
            r["SUPERFLEX"].append(p_obj)
        else:
            r["BN"].append(p_obj)
    else:
        st.session_state.auto_draft_history.append(
            f"Round {round_n} (Pick {current_pick}) - AI Team {current_slot} drafted: **{p_obj['name']}** ({p_obj['pos']} - {p_obj['team']})"
        )


# --- AUTO-DRAFT AUTOMATION LOOP ---
if auto_draft_enabled and not is_user_turn and current_pick <= 150:
    # Automatically execute AI pick on page load if auto-draft is toggled on
    available_pool = df_players[
        ~df_players["id"].isin(st.session_state.drafted_ids)
    ]
    if not available_pool.empty:
        best_available = available_pool.iloc[0].to_dict()
        draft_player(best_available, is_user_pick=False)
        time.sleep(auto_speed)
        st.rerun()


# --- TAB 1: DRAFT ROOM ---
with tab_draft:
    col_left, col_right = st.columns([2, 1])

    with col_right:
        st.subheader("💡 FantasyPros Expert Tip Box")

        qbs_total = len(st.session_state.roster["QB"]) + len(
            st.session_state.roster["SUPERFLEX"]
        )
        rbs_total = len(st.session_state.roster["RB"])
        wrs_total = len(st.session_state.roster["WR"])
        tes_total = len(st.session_state.roster["TE"])

        strengths = []
        weaknesses = []

        if qbs_total >= 2:
            strengths.append(
                "🟢 **QB Depth:** Secured 2+ starting signal callers for Superflex."
            )
        else:
            weaknesses.append(
                "🔴 **QB Scarcity Warning:** Superflex requires solid starting QB depth early."
            )

        if rbs_total + wrs_total >= 4:
            strengths.append("🟢 **Skill Floor:** Solid depth at RB/WR.")
        else:
            weaknesses.append(
                "🔴 **Flex Vulnerability:** Target high-volume starters for flex."
            )

        if tes_total > 0:
            strengths.append(
                "🟢 **TE Locked:** Reliable weekly starter secured."
            )
        else:
            weaknesses.append(
                "🟡 **TE Value Watch:** Keep an eye on elite difference-makers like Brock Bowers or Trey McBride."
            )

        with st.expander("📊 Live Roster Strengths & Weaknesses", expanded=True):
            st.markdown("**Strengths:**")
            if strengths:
                for s in strengths:
                    st.markdown(s)
            else:
                st.caption(
                    "Draft more players to build positional strengths."
                )

            st.markdown("**Weaknesses & Areas to Target:**")
            if weaknesses:
                for w in weaknesses:
                    st.markdown(w)
            else:
                st.caption("No critical weaknesses flagged yet.")

        st.markdown("---")
        st.subheader("⭐ My Wishlist Queue")
        if not st.session_state.queue_ids:
            st.caption("No players queued.")
        else:
            queued_df = df_players[
                df_players["id"].isin(st.session_state.queue_ids)
                & ~df_players["id"].isin(st.session_state.drafted_ids)
            ]
            for _, qrow in queued_df.iterrows():
                qc1, qc2 = st.columns([3, 1])
                qc1.text(f"{qrow['name']} ({qrow['pos']}-{qrow['team']})")
                if qc2.button("Remove", key=f"unq_{qrow['id']}"):
                    st.session_state.queue_ids.remove(qrow["id"])
                    st.rerun()

    with col_left:
        st.subheader("Available Player Pool (Top 150)")

        f1, f2 = st.columns(2)
        with f1:
            search_q = st.text_input(
                "Search Player / Team", placeholder="e.g. Josh Allen, BUF"
            )
        with f2:
            pos_f = st.selectbox(
                "Filter Position", ["ALL", "QB", "RB", "WR", "TE"]
            )

        filtered = df_players[
            ~df_players["id"].isin(st.session_state.drafted_ids)
        ]
        if pos_f != "ALL":
            filtered = filtered[filtered["pos"] == pos_f]
        if search_q:
            filtered = filtered[
                filtered["name"].str.lower().contains(search_q.lower())
                | filtered["team"].str.lower().contains(search_q.lower())
            ]

        for _, row in filtered.head(30).iterrows():
            rc1, rc2, rc3, rc4, rc5, rc6 = st.columns([1, 3, 1, 1, 1, 1])
            rc1.write(f"#{row['id']}")
            rc2.markdown(f"**{row['name']}**")
            rc3.code(row["pos"])
            rc4.text(row["team"])

            in_q = row["id"] in st.session_state.queue_ids
            if rc5.button(
                "📌 Queue" if not in_q else "Unqueue", key=f"q_{row['id']}"
            ):
                if in_q:
                    st.session_state.queue_ids.remove(row["id"])
                else:
                    st.session_state.queue_ids.add(row["id"])
                st.rerun()

            if rc6.button("Draft", key=f"d_{row['id']}"):
                draft_player(row.to_dict(), is_user_pick=True)
                st.rerun()


# --- TAB 2: FULL DRAFT BOARD ---
with tab_board:
    st.subheader("🏟️ Comprehensive 150-Player Draft Board")
    cols_per_row = 5
    all_rows = df_players.to_dict("records")

    for i in range(0, len(all_rows), cols_per_row):
        cols = st.columns(cols_per_row)
        for idx, col in enumerate(cols):
            if i + idx < len(all_rows):
                p = all_rows[i + idx]
                is_drafted = p["id"] in st.session_state.drafted_ids
                status_color = (
                    "background-color: #334155; color: #94a3b8;"
                    if is_drafted
                    else "background-color: #1e293b; border: 1px solid #3b82f6;"
                )
                col.markdown(
                    f"""
                    <div style="padding:8px; border-radius:5px; margin-bottom:8px; text-align:center; {status_color}">
                        <small>#{p['id']} - {p['pos']} ({p['team']})</small><br>
                        <strong>{p['name']}</strong><br>
                        <span>{"❌ DRAFTED" if is_drafted else "🟢 Available"}</span>
                    </div>
                """,
                    unsafe_allow_html=True,
                )


# --- TAB 3: MY ROSTER & BYE ANALYZER ---
with tab_roster:
    st.subheader(f"📋 Roster Sheet for: {team_name}")

    slots_config = [
        ("QB", "Quarterback (QB)", 0),
        ("RB", "Running Back (RB)", 0),
        ("RB", "Running Back (RB)", 1),
        ("WR", "Wide Receiver (WR)", 0),
        ("WR", "Wide Receiver (WR)", 1),
        ("TE", "Tight End (TE)", 0),
        ("FLEX", "Flex (RB/WR/TE)", 0),
        ("SUPERFLEX", "Superflex (QB/FLEX)", 0),
    ]

    for cat, label, idx in slots_config:
        assigned = (
            st.session_state.roster[cat][idx]
            if len(st.session_state.roster[cat]) > idx
            else None
        )
        if assigned:
            st.success(
                f"**{label}:** {assigned['name']} ({assigned['pos']} - {assigned['team']} | Bye: Week {assigned['bye']})"
            )
        else:
            st.info(f"**{label}:** — Empty Slot —")

    st.markdown("### Bench Reserves")
    if not st.session_state.roster["BN"]:
        st.caption("No bench players added yet.")
    else:
        for bp in st.session_state.roster["BN"]:
            st.write(
                f"• {bp['name']} | {bp['pos']} - {bp['team']} (Bye: Week {bp['bye']})"
            )

    st.markdown("---")
    st.subheader("🛡️ Bye Week Analyzer")
    all_starters = []
    for cat, _, idx in slots_config:
        if len(st.session_state.roster[cat]) > idx:
            all_starters.append(st.session_state.roster[cat][idx])

    if all_starters:
        bye_counts = {}
        for s in all_starters:
            b = s["bye"]
            bye_counts[b] = bye_counts.get(b, 0) + 1

        overloaded = [week for week, count in bye_counts.items() if count >= 2]
        if overloaded:
            st.warning(
                f"⚠️ **Bye Conflict Warning:** Multiple starting players on Bye during Week(s): {', '.join(map(str, overloaded))}."
            )
        else:
            st.success(
                "✅ No major starting lineup bye week conflicts detected!"
            )


# --- TAB 4: AI AUTO-DRAFT LOG ---
with tab_log:
    st.subheader("🤖 Simulated League Auto-Draft Activity")
    st.markdown("Review picks made automatically by competing teams.")

    if not st.session_state.auto_draft_history:
        st.info("No auto-draft actions recorded yet.")
    else:
        for log in reversed(st.session_state.auto_draft_history):
            st.markdown(log)

    st.markdown("---")
    if st.button("Reset Entire Draft Board & History"):
        st.session_state.drafted_ids = set()
        st.session_state.queue_ids = set()
        st.session_state.auto_draft_history = []
        st.session_state.roster = {
            "QB": [],
            "RB": [],
            "WR": [],
            "TE": [],
            "FLEX": [],
            "SUPERFLEX": [],
            "BN": [],
        }
        st.rerun()
         
