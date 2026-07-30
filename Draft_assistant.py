import random
import time
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Superflex Draft Assistant Pro", page_icon="🏈", layout="wide"
)

# Custom CSS for Position Color Coding & Visual Polish
st.markdown(
    """
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b;
        border-radius: 6px;
        color: #f8fafc;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }
    
    /* Position Badge Styles */
    .badge-qb { background-color: #1e3a8a; color: #93c5fd; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; border: 1px solid #3b82f6; }
    .badge-rb { background-color: #064e3b; color: #6ee7b7; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; border: 1px solid #10b981; }
    .badge-wr { background-color: #78350f; color: #fde68a; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; border: 1px solid #f59e0b; }
    .badge-te { background-color: #581c87; color: #d8b4fe; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; border: 1px solid #a855f7; }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session State
if "drafted_ids" not in st.session_state:
    st.session_state.drafted_ids = set()

if "queue_ids" not in st.session_state:
    st.session_state.queue_ids = set()

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


# Helper for badge rendering
def get_position_badge(pos):
    if pos == "QB":
        return '<span class="badge-qb">QB</span>'
    elif pos == "RB":
        return '<span class="badge-rb">RB</span>'
    elif pos == "WR":
        return '<span class="badge-wr">WR</span>'
    elif pos == "TE":
        return '<span class="badge-te">TE</span>'
    return f"<span>{pos}</span>"


# Enhanced 150-Player Database with Draft Sharks metrics (Tier, ADP, Proj Points, 3D Value)
@st.cache_data
def load_150_players():
    base_players = [
        {
            "id": 1,
            "name": "Josh Allen",
            "pos": "QB",
            "team": "BUF",
            "bye": 7,
            "tier": "Tier 1",
            "adp": "1.01",
            "proj_pts": 363,
            "val_3d": 100,
        },
        {
            "id": 2,
            "name": "Jahmyr Gibbs",
            "pos": "RB",
            "team": "DET",
            "bye": 6,
            "tier": "Tier 1",
            "adp": "1.04",
            "proj_pts": 273,
            "val_3d": 75,
        },
        {
            "id": 3,
            "name": "Bijan Robinson",
            "pos": "RB",
            "team": "ATL",
            "bye": 11,
            "tier": "Tier 1",
            "adp": "1.02",
            "proj_pts": 274,
            "val_3d": 73,
        },
        {
            "id": 4,
            "name": "Lamar Jackson",
            "pos": "QB",
            "team": "BAL",
            "bye": 13,
            "tier": "Tier 1",
            "adp": "1.11",
            "proj_pts": 328,
            "val_3d": 72,
        },
        {
            "id": 5,
            "name": "Puka Nacua",
            "pos": "WR",
            "team": "LAR",
            "bye": 11,
            "tier": "Tier 1",
            "adp": "1.06",
            "proj_pts": 208,
            "val_3d": 70,
        },
        {
            "id": 6,
            "name": "Drake Maye",
            "pos": "QB",
            "team": "NE",
            "bye": 11,
            "tier": "Tier 1",
            "adp": "1.03",
            "proj_pts": 315,
            "val_3d": 68,
        },
        {
            "id": 7,
            "name": "Joe Burrow",
            "pos": "QB",
            "team": "CIN",
            "bye": 6,
            "tier": "Tier 1",
            "adp": "1.10",
            "proj_pts": 311,
            "val_3d": 67,
        },
        {
            "id": 8,
            "name": "Ja'Marr Chase",
            "pos": "WR",
            "team": "CIN",
            "bye": 6,
            "tier": "Tier 1",
            "adp": "1.05",
            "proj_pts": 186,
            "val_3d": 66,
        },
        {
            "id": 9,
            "name": "Jaxon Smith-Njigba",
            "pos": "WR",
            "team": "SEA",
            "bye": 11,
            "tier": "Tier 1",
            "adp": "1.07",
            "proj_pts": 187,
            "val_3d": 64,
        },
        {
            "id": 10,
            "name": "Christian McCaffrey",
            "pos": "RB",
            "team": "SF",
            "bye": 8,
            "tier": "Tier 2",
            "adp": "1.09",
            "proj_pts": 241,
            "val_3d": 63,
        },
        {
            "id": 11,
            "name": "Jonathan Taylor",
            "pos": "RB",
            "team": "IND",
            "bye": 13,
            "tier": "Tier 2",
            "adp": "1.12",
            "proj_pts": 260,
            "val_3d": 62,
        },
        {
            "id": 12,
            "name": "Jayden Daniels",
            "pos": "QB",
            "team": "WAS",
            "bye": 7,
            "tier": "Tier 2",
            "adp": "1.08",
            "proj_pts": 315,
            "val_3d": 62,
        },
        {
            "id": 13,
            "name": "Jalen Hurts",
            "pos": "QB",
            "team": "PHI",
            "bye": 10,
            "tier": "Tier 2",
            "adp": "3.01",
            "proj_pts": 313,
            "val_3d": 61,
        },
        {
            "id": 14,
            "name": "James Cook III",
            "pos": "RB",
            "team": "BUF",
            "bye": 7,
            "tier": "Tier 2",
            "adp": "2.01",
            "proj_pts": 232,
            "val_3d": 61,
        },
        {
            "id": 15,
            "name": "Justin Herbert",
            "pos": "QB",
            "team": "LAC",
            "bye": 7,
            "tier": "Tier 2",
            "adp": "2.03",
            "proj_pts": 298,
            "val_3d": 59,
        },
        {
            "id": 16,
            "name": "Caleb Williams",
            "pos": "QB",
            "team": "CHI",
            "bye": 10,
            "tier": "Tier 2",
            "adp": "2.04",
            "proj_pts": 295,
            "val_3d": 58,
        },
        {
            "id": 17,
            "name": "Amon-Ra St. Brown",
            "pos": "WR",
            "team": "DET",
            "bye": 6,
            "tier": "Tier 2",
            "adp": "2.02",
            "proj_pts": 182,
            "val_3d": 57,
        },
        {
            "id": 18,
            "name": "Trevor Lawrence",
            "pos": "QB",
            "team": "JAC",
            "bye": 7,
            "tier": "Tier 2",
            "adp": "2.05",
            "proj_pts": 290,
            "val_3d": 56,
        },
        {
            "id": 19,
            "name": "Dak Prescott",
            "pos": "QB",
            "team": "DAL",
            "bye": 14,
            "tier": "Tier 2",
            "adp": "2.06",
            "proj_pts": 288,
            "val_3d": 55,
        },
        {
            "id": 20,
            "name": "CeeDee Lamb",
            "pos": "WR",
            "team": "DAL",
            "bye": 14,
            "tier": "Tier 2",
            "adp": "2.07",
            "proj_pts": 179,
            "val_3d": 54,
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
        rnd = random.randint(3, 15)
        pick = random.randint(1, 10)
        base_players.append(
            {
                "id": current_id,
                "name": name,
                "pos": pos,
                "team": random.choice(nfl_teams),
                "bye": random.randint(5, 14),
                "tier": f"Tier {random.randint(3, 5)}",
                "adp": f"{rnd}.{pick:02d}",
                "proj_pts": random.randint(130, 240),
                "val_3d": max(10, 55 - (current_id // 3)),
            }
        )
        current_id += 1

    return pd.DataFrame(base_players)


df_players = load_150_players()

# App Header
st.title(f"🏈 Superflex Draft Assistant: {team_name}")


# Snake draft calculation
def get_current_picker(pick_num, user_slot, num_teams):
    round_num = (pick_num - 1) // num_teams + 1
    pos_in_round = (pick_num - 1) % num_teams + 1

    if round_num % 2 == 1:
        picking_team_slot = pos_in_round
    else:
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
                "🟡 **TE Value Watch:** Keep an eye on elite difference-makers."
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
                pos_badge = get_position_badge(qrow["pos"])
                qc1.markdown(
                    f"{pos_badge} **{qrow['name']}** ({qrow['team']})<br><small style='color:#94a3b8;'>{qrow['tier']} | Proj: {qrow['proj_pts']} pts</small>",
                    unsafe_allow_html=True,
                )
                if qc2.button("Remove", key=f"unq_{qrow['id']}"):
                    st.session_state.queue_ids.remove(qrow["id"])
                    st.rerun()

    with col_left:
        st.subheader("Available Player Pool (Draft Sharks Metrics)")

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

        for _, row in filtered.head(25).iterrows():
            with st.container():
                rc1, rc2, rc3, rc4, rc5, rc6 = st.columns(
                    [1, 2.5, 1, 2.2, 1.2, 1.2]
                )
                rc1.markdown(
                    f"<span style='color: #94a3b8; font-weight:600;'>#{row['id']}</span>",
                    unsafe_allow_html=True,
                )
                rc2.markdown(
                    f"**{row['name']}**<br><small style='color: #cbd5e1;'>{row['team']} • Bye {row['bye']}</small>",
                    unsafe_allow_html=True,
                )
                rc3.markdown(
                    get_position_badge(row["pos"]), unsafe_allow_html=True
                )

                # Draft Sharks Info Display
                rc4.markdown(
                    f"<small><b>{row['tier']}</b> | ADP: {row['adp']}<br>Proj: <b>{row['proj_pts']} pts</b> | 3D Val: <b>{row['val_3d']}</b></small>",
                    unsafe_allow_html=True,
                )

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
                st.markdown(
                    "<hr style='margin: 4px 0px; border-color: #1e293b;'>",
                    unsafe_allow_html=True,
                )


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

                if is_drafted:
                    card_style = "background-color: #0f172a; color: #475569; border: 1px solid #1e293b;"
                    status_text = "❌ DRAFTED"
                else:
                    if p["pos"] == "QB":
                        card_style = "background-color: #0f172a; border: 1px solid #1e3a8a; color: #f8fafc;"
                    elif p["pos"] == "RB":
                        card_style = "background-color: #0f172a; border: 1px solid #064e3b; color: #f8fafc;"
                    elif p["pos"] == "WR":
                        card_style = "background-color: #0f172a; border: 1px solid #78350f; color: #f8fafc;"
                    else:
                        card_style = "background-color: #0f172a; border: 1px solid #581c87; color:
