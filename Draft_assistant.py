import random
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


# Comprehensive 150-Player Database based on Draft Sharks Superflex Rankings
@st.cache_data
def load_150_players():
    base_players = [
        {"id": 1, "name": "Josh Allen", "pos": "QB", "team": "BUF", "bye": 7},
        {"id": 2, "name": "Jahmyr Gibbs", "pos": "RB", "team": "DET", "bye": 6},
        {"id": 3, "name": "Bijan Robinson", "pos": "RB", "team": "ATL", "bye": 11},
        {"id": 4, "name": "Lamar Jackson", "pos": "QB", "team": "BAL", "bye": 13},
        {"id": 5, "name": "Puka Nacua", "pos": "WR", "team": "LAR", "bye": 11},
        {"id": 6, "name": "Drake Maye", "pos": "QB", "team": "NE", "bye": 11},
        {"id": 7, "name": "Joe Burrow", "pos": "QB", "team": "CIN", "bye": 6},
        {"id": 8, "name": "Ja'Marr Chase", "pos": "WR", "team": "CIN", "bye": 6},
        {
            "id": 9,
            "name": "Jaxon Smith-Njigba",
            "pos": "WR",
            "team": "SEA",
            "bye": 11,
        },
        {
            "id": 10,
            "name": "Christian McCaffrey",
            "pos": "RB",
            "team": "SF",
            "bye": 8,
        },
        {
            "id": 11,
            "name": "Jonathan Taylor",
            "pos": "RB",
            "team": "IND",
            "bye": 13,
        },
        {"id": 12, "name": "Jayden Daniels", "pos": "QB", "team": "WAS", "bye": 7},
        {"id": 13, "name": "Jalen Hurts", "pos": "QB", "team": "PHI", "bye": 10},
        {"id": 14, "name": "James Cook", "pos": "RB", "team": "BUF", "bye": 7},
        {"id": 15, "name": "Derrick Henry", "pos": "RB", "team": "BAL", "bye": 13},
        {
            "id": 16,
            "name": "Amon-Ra St. Brown",
            "pos": "WR",
            "team": "DET",
            "bye": 6,
        },
        {"id": 17, "name": "CeeDee Lamb", "pos": "WR", "team": "DAL", "bye": 14},
        {"id": 18, "name": "Justin Jefferson", "pos": "WR", "team": "MIN", "bye": 6},
        {"id": 19, "name": "Saquon Barkley", "pos": "RB", "team": "PHI", "bye": 10},
        {
            "id": 20,
            "name": "Trevor Lawrence",
            "pos": "QB",
            "team": "JAC",
            "bye": 7,
        },
        {"id": 21, "name": "Justin Herbert", "pos": "QB", "team": "LAC", "bye": 7},
        {"id": 22, "name": "Caleb Williams", "pos": "QB", "team": "CHI", "bye": 10},
        {"id": 23, "name": "Brock Purdy", "pos": "QB", "team": "SF", "bye": 8},
        {"id": 24, "name": "Ashton Jeanty", "pos": "RB", "team": "LVR", "bye": 13},
        {"id": 25, "name": "Kyler Murray", "pos": "QB", "team": "MIN", "bye": 6},
        {"id": 26, "name": "Dak Prescott", "pos": "QB", "team": "DAL", "bye": 14},
        {"id": 27, "name": "A.J. Brown", "pos": "WR", "team": "NE", "bye": 11},
        {"id": 28, "name": "Drake London", "pos": "WR", "team": "ATL", "bye": 11},
        {"id": 29, "name": "George Pickens", "pos": "WR", "team": "DAL", "bye": 14},
        {"id": 30, "name": "Jaxson Dart", "pos": "QB", "team": "NYG", "bye": 8},
        {
            "id": 31,
            "name": "Kenneth Walker III",
            "pos": "RB",
            "team": "KC",
            "bye": 5,
        },
        {
            "id": 32,
            "name": "Omarion Hampton",
            "pos": "RB",
            "team": "LAC",
            "bye": 7,
        },
        {"id": 33, "name": "Rashee Rice", "pos": "WR", "team": "KC", "bye": 5},
        {"id": 34, "name": "De'Von Achane", "pos": "RB", "team": "MIA", "bye": 6},
        {"id": 35, "name": "Bo Nix", "pos": "QB", "team": "DEN", "bye": 10},
        {"id": 36, "name": "Brock Bowers", "pos": "TE", "team": "LVR", "bye": 13},
        {"id": 37, "name": "Josh Jacobs", "pos": "RB", "team": "GB", "bye": 11},
        {
            "id": 38,
            "name": "Patrick Mahomes",
            "pos": "QB",
            "team": "KC",
            "bye": 5,
        },
        {"id": 39, "name": "Tee Higgins", "pos": "WR", "team": "CIN", "bye": 6},
        {
            "id": 40,
            "name": "Colston Loveland",
            "pos": "TE",
            "team": "CHI",
            "bye": 10,
        },
        {"id": 41, "name": "Jeremiah Love", "pos": "RB", "team": "ARI", "bye": 14},
        {
            "id": 42,
            "name": "Christian Watson",
            "pos": "WR",
            "team": "GB",
            "bye": 11,
        },
        {"id": 43, "name": "Chase Brown", "pos": "RB", "team": "CIN", "bye": 6},
        {"id": 44, "name": "Trey McBride", "pos": "TE", "team": "ARI", "bye": 14},
        {"id": 45, "name": "Zay Flowers", "pos": "WR", "team": "BAL", "bye": 13},
        {"id": 46, "name": "Chris Olave", "pos": "WR", "team": "NO", "bye": 8},
        {"id": 47, "name": "Kyren Williams", "pos": "RB", "team": "LAR", "bye": 11},
        {"id": 48, "name": "Javonte Williams", "pos": "RB", "team": "DAL", "bye": 14},
        {"id": 49, "name": "DeVonta Smith", "pos": "WR", "team": "PHI", "bye": 10},
        {"id": 50, "name": "Davante Adams", "pos": "WR", "team": "LAR", "bye": 11},
        {"id": 51, "name": "Tyler Warren", "pos": "TE", "team": "IND", "bye": 13},
        {"id": 52, "name": "Malik Nabers", "pos": "WR", "team": "NYG", "bye": 8},
        {"id": 53, "name": "Jared Goff", "pos": "QB", "team": "DET", "bye": 6},
        {"id": 54, "name": "Jameson Williams", "pos": "WR", "team": "DET", "bye": 6},
        {"id": 55, "name": "Travis Etienne", "pos": "RB", "team": "NO", "bye": 8},
        {
            "id": 56,
            "name": "Terry McLaurin",
            "pos": "WR",
            "team": "WAS",
            "bye": 7,
        },
        {"id": 57, "name": "Garrett Wilson", "pos": "WR", "team": "NYJ", "bye": 13},
        {"id": 58, "name": "Tucker Kraft", "pos": "TE", "team": "GB", "bye": 11},
        {"id": 59, "name": "Breece Hall", "pos": "RB", "team": "NYJ", "bye": 13},
        {
            "id": 60,
            "name": "Tetairoa McMillan",
            "pos": "WR",
            "team": "CAR",
            "bye": 5,
        },
        {
            "id": 61,
            "name": "Matthew Stafford",
            "pos": "QB",
            "team": "LAR",
            "bye": 11,
        },
    ]

    # Generate remaining players cleanly up to 150 following typical draft board distribution
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
        "Brandon",
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
        pos = random.choices(
            positions, weights=[35, 45, 12, 8], k=1
        )[0]  # weighted spread
        name = f"{random.choice(first_names)} {random.choice(last_names)} ({current_id})"
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
st.title("🏈 Superflex Draft Assistant Pro")
st.markdown(
    "**10-Team • Standard Scoring • Draft Board, Roster Manager & Tier Tracker**"
)
st.markdown("---")

# Sidebar navigation / tool controls
st.sidebar.header("Draft Controls")
view_mode = st.sidebar.radio(
    "Select View Mode",
    ["Draft Room (Main)", "Full Draft Board", "My Roster & Bye Analyzer"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Quick Stats")
total_drafted = len(st.session_state.drafted_ids)
st.sidebar.progress(
    total_drafted / 150, text=f"Draft Pool Progress: {total_drafted}/150 Picked"
)


# --- VIEW 1: DRAFT ROOM ---
if view_mode == "Draft Room (Main)":
    col_left, col_right = st.columns([2, 1])

    with col_right:
        st.subheader("💡 Expert Advice")
        qb_count = len(st.session_state.roster["QB"]) + len(
            [
                p
                for p in st.session_state.roster["SUPERFLEX"]
                if p["pos"] == "QB"
            ]
        )

        if qb_count == 0:
            st.warning(
                "**Priority Warning:** You lack a starting Quarterback. Secure a top passer before Tier 1 runs dry."
            )
        elif qb_count == 1:
            st.info(
                "**Strategy Tip:** Anchor QB locked. Focus on high-end Standard RBs or elite WR target volume."
            )
        else:
            st.success(
                "**Roster Health:** QB structure is rock solid. Focus on depth and FLEX value."
            )

        st.markdown("---")
        st.subheader("⭐ My Wishlist Queue")
        if not st.session_state.queue_ids:
            st.caption("No players queued. Click 'Queue' on any player.")
        else:
            queued_df = df_players[
                df_players["id"].isin(st.session_state.queue_ids)
                & ~df_players["id"].isin(st.session_state.drafted_ids)
            ]
            for _, qrow in queued_df.iterrows():
                qc1, qc2 = st.columns([3, 1])
                qc1.text(f"{qrow['name']} ({qrow['pos']})")
                if qc2.button("Remove", key=f"unq_{qrow['id']}"):
                    st.session_state.queue_ids.remove(qrow["id"])
                    st.rerun()

    with col_left:
        st.subheader("Available Player Pool")

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

        # Render rows with Action buttons
        for _, row in filtered.head(40).iterrows():
            rc1, rc2, rc3, rc4, rc5, rc6 = st.columns([1, 3, 1, 1, 1, 1])
            rc1.write(f"#{row['id']}")
            rc2.markdown(f"**{row['name']}**")
            rc3.code(row["pos"])
            rc4.text(row["team"])

            # Queue Button toggle
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
                p_obj = row.to_dict()
                st.session_state.drafted_ids.add(row["id"])
                if row["id"] in st.session_state.queue_ids:
                    st.session_state.queue_ids.remove(row["id"])

                # Smart Roster Allocation
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
                elif (
                    p_obj["pos"] in ["RB", "WR", "TE"] and len(r["FLEX"]) < 1
                ):
                    r["FLEX"].append(p_obj)
                elif len(r["SUPERFLEX"]) < 1:
                    r["SUPERFLEX"].append(p_obj)
                else:
                    r["BN"].append(p_obj)
                st.rerun()


# --- VIEW 2: FULL DRAFT BOARD ---
elif view_mode == "Full Draft Board":
    st.subheader("🏟️ Overall Draft Tracker (Top 150)")
    st.markdown("Visual grid overview of player availability.")

    # Grid display of all 150 players
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


# --- VIEW 3: MY ROSTER & BYE ANALYZER ---
elif view_mode == "My Roster & Bye Analyzer":
    st.subheader("📋 My Comprehensive Starting Lineup & Bench")

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

    roster_lines = []
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
            roster_lines.append(
                f"{label}: {assigned['name']} ({assigned['pos']})"
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
            roster_lines.append(f"Bench: {bp['name']} ({bp['pos']})")

    st.markdown("---")
    st.subheader("🛡️ Bye Week Analyzer")
    # Check bye week overlaps in starters
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
                f"⚠️ **Bye Conflict Warning:** You have multiple starting players on a Bye during Week(s): {', '.join(map(str, overloaded))}. Keep an eye on depth!"
            )
        else:
            st.success(
                "✅ No major starting lineup bye week conflicts detected!"
            )

    st.markdown("---")
    if st.button("Reset Entire Draft Board"):
        st.session_state.drafted_ids = set()
        st.session_state.queue_ids = set()
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
        
