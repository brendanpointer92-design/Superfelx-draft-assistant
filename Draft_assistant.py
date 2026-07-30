import random
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Superflex Draft Assistant",
    page_layout="wide",
)

# --- CUSTOM CSS FOR STYLING ---
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        font-weight: 600;
    }
    .metric-card {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #374151;
        text-align: center;
    }
    .draft-cell {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 6px;
        padding: 8px;
        font-size: 11px;
        text-align: center;
        min-height: 65px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- FANTASYPROS SUPERFLEX 150 PLAYER DATA (STANDARD SCORING) ---
RAW_PLAYERS = [
    ("Josh Allen", "BUF", "QB"),
    ("Lamar Jackson", "BAL", "QB"),
    ("Drake Maye", "NE", "QB"),
    ("Joe Burrow", "CIN", "QB"),
    ("Jayden Daniels", "WAS", "QB"),
    ("Jalen Hurts", "PHI", "QB"),
    ("Bijan Robinson", "ATL", "RB"),
    ("Jahmyr Gibbs", "DET", "RB"),
    ("Ja'Marr Chase", "CIN", "WR"),
    ("Justin Herbert", "LAC", "QB"),
    ("Caleb Williams", "CHI", "QB"),
    ("Puka Nacua", "LAR", "WR"),
    ("Jaxon Smith-Njigba", "SEA", "WR"),
    ("Trevor Lawrence", "JAC", "QB"),
    ("Dak Prescott", "DAL", "QB"),
    ("Amon-Ra St. Brown", "DET", "WR"),
    ("Christian McCaffrey", "SF", "RB"),
    ("Jonathan Taylor", "IND", "RB"),
    ("CeeDee Lamb", "DAL", "WR"),
    ("Jaxson Dart", "NYG", "QB"),
    ("Brock Purdy", "SF", "QB"),
    ("Justin Jefferson", "MIN", "WR"),
    ("James Cook III", "BUF", "RB"),
    ("Bo Nix", "DEN", "QB"),
    ("Patrick Mahomes II", "KC", "QB"),
    ("Ashton Jeanty", "LV", "RB"),
    ("Drake London", "ATL", "WR"),
    ("Matthew Stafford", "LAR", "QB"),
    ("A.J. Brown", "PHI", "WR"),
    ("De'Von Achane", "MIA", "RB"),
    ("Chase Brown", "CIN", "RB"),
    ("Brock Bowers", "LV", "TE"),
    ("Nico Collins", "HOU", "WR"),
    ("Saquon Barkley", "PHI", "RB"),
    ("Omarion Hampton", "LAC", "RB"),
    ("Jared Goff", "DET", "QB"),
    ("George Pickens", "DAL", "WR"),
    ("Derrick Henry", "BAL", "RB"),
    ("Kyler Murray", "ARI", "QB"),
    ("Trey McBride", "ARI", "TE"),
    ("Kenneth Walker III", "SEA", "RB"),
    ("Rashee Rice", "KC", "WR"),
    ("Chris Olave", "NO", "WR"),
    ("Jordan Love", "GB", "QB"),
    ("Baker Mayfield", "TB", "QB"),
    ("DeVonta Smith", "PHI", "WR"),
    ("Tyler Shough", "NO", "QB"),
    ("Tee Higgins", "CIN", "WR"),
    ("Zay Flowers", "BAL", "WR"),
    ("Tetairoa McMillan", "CAR", "WR"),
    ("Jeremiyah Love", "ARI", "RB"),
    ("Kyren Williams", "LAR", "RB"),
    ("Josh Jacobs", "GB", "RB"),
    ("Malik Nabers", "NYG", "WR"),
    ("Brian Thomas Jr.", "JAC", "WR"),
    ("Rome Odunze", "CHI", "WR"),
    ("Sam LaPorta", "DET", "TE"),
    ("Mark Andrews", "BAL", "TE"),
    ("George Kittle", "SF", "TE"),
    ("Travis Kelce", "KC", "TE"),
    ("Kyle Pitts", "ATL", "TE"),
    ("TJ Hockenson", "MIN", "TE"),
    ("Dalton Kincaid", "BUF", "TE"),
    ("Evan Engram", "JAC", "TE"),
    ("Jake Ferguson", "DAL", "TE"),
    ("Deshaun Watson", "CLE", "QB"),
    ("Aaron Rodgers", "NYJ", "QB"),
    ("Geno Smith", "SEA", "QB"),
    ("Russell Wilson", "PIT", "QB"),
    ("Kirk Cousins", "ATL", "QB"),
    ("Will Levis", "TEN", "QB"),
    ("Anthony Richardson", "IND", "QB"),
    ("Bryce Young", "CAR", "QB"),
    ("J.J. McCarthy", "MIN", "QB"),
    ("Tua Tagovailoa", "MIA", "QB"),
    ("Tony Pollard", "TEN", "RB"),
    ("Rhamondre Stevenson", "NE", "RB"),
    ("Alvin Kamara", "NO", "RB"),
    ("Joe Mixon", "HOU", "RB"),
    ("Rachaad White", "TB", "RB"),
    ("Kenneth Gainwell", "PHI", "RB"),
    ("Zack Moss", "CIN", "RB"),
    ("Nick Chubb", "CLE", "RB"),
    ("Austin Ekeler", "WAS", "RB"),
    ("Najee Harris", "PIT", "RB"),
    ("Jaylen Warren", "PIT", "RB"),
    ("David Montgomery", "DET", "RB"),
    ("Travis Etienne Jr.", "JAC", "RB"),
    ("Braelon Allen", "NYJ", "RB"),
    ("Blake Corum", "LAR", "RB"),
    ("Marvin Harrison Jr.", "ARI", "WR"),
    ("Brandon Aiyuk", "SF", "WR"),
    ("Michael Pittman Jr.", "IND", "WR"),
    ("Deebo Samuel", "SF", "WR"),
    ("DK Metcalf", "SEA", "WR"),
    ("Terry McLaurin", "WAS", "WR"),
    ("Cooper Kupp", "LAR", "WR"),
    ("Davante Adams", "NYJ", "WR"),
    ("Stefon Diggs", "HOU", "WR"),
    ("Chris Godwin", "TB", "WR"),
    ("Tank Dell", "HOU", "WR"),
    ("Christian Kirk", "JAC", "WR"),
    ("Calvin Ridley", "TEN", "WR"),
    ("Amari Cooper", "BUF", "WR"),
    ("Diontae Johnson", "BAL", "WR"),
    ("Keenan Allen", "CHI", "WR"),
    ("Khalil Shakir", "BUF", "WR"),
    ("Jameson Williams", "DET", "WR"),
    ("Jordan Addison", "MIN", "WR"),
    ("Xavier Worthy", "KC", "WR"),
    ("Brian Robinson Jr.", "WAS", "RB"),
    ("Javonte Williams", "DEN", "RB"),
    ("Zamir White", "LV", "RB"),
    ("Tyjae Spears", "TEN", "RB"),
    ("Jonathon Brooks", "CAR", "RB"),
    ("TreVeyon Henderson", "OSU", "RB"),
    ("Quinshon Judkins", "OSU", "RB"),
    ("Emeka Egbuka", "OSU", "WR"),
    ("Luther Burden III", "MOC", "WR"),
    ("Isaiah Bond", "TEX", "WR"),
    ("Colston Loveland", "MICH", "TE"),
    ("Dallas Goedert", "PHI", "TE"),
    ("Pat Freiermuth", "PIT", "TE"),
    ("David Njoku", "CLE", "TE"),
    ("Hunter Henry", "NE", "TE"),
    ("Tucker Kraft", "GB", "TE"),
    ("Ben Sinnott", "WAS", "TE"),
    ("Luke Musgrave", "GB", "TE"),
    ("Michael Mayer", "LV", "TE"),
    ("Noah Fant", "SEA", "TE"),
    ("Erick All", "CIN", "TE"),
    ("Ty Chandler", "MIN", "RB"),
    ("Ray Davis", "BUF", "RB"),
    ("Bucky Irving", "TB", "RB"),
    ("Kimani Vidal", "LAC", "RB"),
    ("Audric Estme", "DEN", "RB"),
    ("Will Shipley", "PHI", "RB"),
    ("Rasheen Ali", "BAL", "RB"),
    ("Isaac Guerendo", "SF", "RB"),
    ("Dylan Laube", "LV", "RB"),
    ("Frank Gore Jr.", "BUF", "RB"),
    ("Cody Schrader", "LAR", "RB"),
    ("Jase McClellan", "ATL", "RB"),
    ("Emani Bailey", "KC", "RB"),
    ("Carson Steele", "KC", "RB"),
    ("Keaton Mitchell", "BAL", "RB"),
    ("Kendre Miller", "NO", "RB"),
    ("Sean Tucker", "TB", "RB"),
    ("Eric Gray", "NYG", "RB"),
    ("Chris Rodriguez Jr.", "WAS", "RB"),
    ("Deneric Prince", "KC", "RB"),
]

# --- INITIALIZE SESSION STATE ---
NUM_TEAMS = 10
TOTAL_ROUNDS = 15

if "initialized" not in st.session_state:
  st.session_state.initialized = True
  st.session_state.current_pick = 1
  st.session_state.user_team_idx = 0
  st.session_state.team_names = [f"Team {i+1}" for i in range(NUM_TEAMS)]
  st.session_state.team_names[0] = "My Team"
  st.session_state.rosters = {i: [] for i in range(NUM_TEAMS)}

  st.session_state.players = []
  for idx, (name, team, pos) in enumerate(RAW_PLAYERS[:150]):
    st.session_state.players.append({
        "id": idx + 1,
        "name": name,
        "team": team,
        "pos": pos,
        "drafted": False,
        "drafted_by": None,
        "pick_num": None,
    })


def get_current_turn():
  if st.session_state.current_pick > NUM_TEAMS * TOTAL_ROUNDS:
    return None, None, None
  round_num = (st.session_state.current_pick - 1) // NUM_TEAMS + 1
  index_in_round = (st.session_state.current_pick - 1) % NUM_TEAMS
  if round_num % 2 == 1:
    team_idx = index_in_round
  else:
    team_idx = NUM_TEAMS - 1 - index_in_round
  return round_num, index_in_round + 1, team_idx


def draft_player(player_id, team_idx):
  for p in st.session_state.players:
    if p["id"] == player_id and not p["drafted"]:
      p["drafted"] = True
      p["drafted_by"] = team_idx
      p["pick_num"] = st.session_state.current_pick
      st.session_state.rosters[team_idx].append(p)
      st.session_state.current_pick += 1
      return True
  return False


def simulate_pick():
  round_num, _, team_idx = get_current_turn()
  if round_num is None:
    return
  available = [p for p in st.session_state.players if not p["drafted"]]
  if not available:
    return

  chosen = available[0]
  if round_num <= 3:
    qbs = [p for p in available if p["pos"] == "QB"]
    if qbs and random.random() < 0.75:
      chosen = qbs[0]

  draft_player(chosen["id"], team_idx)


# --- SIDEBAR: LEAGUE CONFIG & TEAM MANAGEMENT ---
st.sidebar.header("🏈 Draft Settings")
user_slot = st.sidebar.selectbox(
    "Your Draft Slot",
    options=list(range(1, NUM_TEAMS + 1)),
    index=st.session_state.user_team_idx,
)
st.session_state.user_team_idx = user_slot - 1

st.sidebar.markdown("---")
st.sidebar.header("✏️ Rename Teams")
for i in range(NUM_TEAMS):
  current_name = st.session_state.team_names[i]
  new_name = st.sidebar.text_input(f"Team {i+1} Name", current_name, key=f"rename_{i}")
  st.session_state.team_names[i] = new_name

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Reset Draft", type="primary"):
  for key in list(st.session_state.keys()):
    del st.session_state[key]
  st.rerun()

# --- MAIN DASHBOARD BANNER ---
round_num, pick_in_round, active_team_idx = get_current_turn()

st.title("⚡ Superflex Draft Assistant (10-Man Standard)")

if round_num is None:
  st.balloons()
  st.success("🎉 Draft Completed! Check out the final team rosters below.")
else:
  active_team_name = st.session_state.team_names[active_team_idx]
  is_user_turn = active_team_idx == st.session_state.user_team_idx

  col_b1, col_b2 = st.columns([3, 1])
  with col_b1:
    if is_user_turn:
      st.markdown(
          f"### 🟢 <span style='color:#22c55e;'>YOUR TURN!</span> (Round"
          f" {round_num}, Pick {pick_in_round} | Overall"
          f" {st.session_state.current_pick})",
          unsafe_allow_html=True,
      )
    else:
      st.markdown(
          f"### ⏳ On the Clock: **{active_team_name}** (Round {round_num},"
          f" Pick {pick_in_round} | Overall {st.session_state.current_pick})"
      )
  with col_b2:
    if not is_user_turn:
      if st.button("⏩ Simulate Pick"):
        simulate_pick()
        st.rerun()
      if st.button("⚡ Sim to My Turn"):
        while True:
          r, _, t_idx = get_current_turn()
          if r is None or t_idx == st.session_state.user_team_idx:
            break
          simulate_pick()
        st.rerun()

st.markdown("---")

# --- MAIN TABS ---
tab_avail, tab_board, tab_rosters = st.tabs(
    ["📋 Available Rankings (150)", "📊 Visual Draft Board", "👥 Team Rosters"]
)

with tab_avail:
  st.subheader("FantasyPros Superflex Top 150 - Live Pool")

  f_col1, f_col2 = st.columns(2)
  with f_col1:
    pos_filter = st.selectbox(
        "Filter Position", ["ALL", "QB", "RB", "WR", "TE"]
    )
  with f_col2:
    search_query = st.text_input("Search Player Name", "")

  available_players = [
      p for p in st.session_state.players if not p["drafted"]
  ]
  if pos_filter != "ALL":
    available_players = [p for p in available_players if p["pos"] == pos_filter]
  if search_query:
    available_players = [
        p
        for p in available_players
        if search_query.lower() in p["name"].lower()
    ]

  # Table header
  h1, h2, h3, h4 = st.columns([1, 4, 1, 2])
  h1.markdown("**Rank**")
  h2.markdown("**Player (Pos - Team)**")
  h3.markdown("**Action**")
  h4.markdown("---")

  for p in available_players[:40]:  # Paginate/limit view for maximum performance
    cp1, cp2, cp3, cp4 = st.columns([1, 4, 1, 2])
    cp1.markdown(f"`#{p['id']}`")
    cp2.markdown(f"**{p['name']}** `({p['pos']} - {p['team']})`")
    with cp3:
      if st.button("Draft", key=f"draft_btn_{p['id']}"):
        draft_player(p["id"], st.session_state.user_team_idx)
        st.rerun()
    cp4.markdown("---")

with tab_board:
  st.subheader("Visual Draft Board Grid (Snake Draft)")

  for r in range(1, TOTAL_ROUNDS + 1):
    st.markdown(f"**Round {r}**")
    row_cols = st.columns(NUM_TEAMS)
    for t_idx in range(NUM_TEAMS):
      if r % 2 == 1:
        pick_num = (r - 1) * NUM_TEAMS + t_idx + 1
      else:
        pick_num = (r - 1) * NUM_TEAMS + (NUM_TEAMS - t_idx)

      cell_player_name = "-"
      cell_pos = ""
      for p in st.session_state.players:
        if p["drafted_by"] == t_idx and p.get("pick_num") == pick_num:
          cell_player_name = p["name"]
          cell_pos = p["pos"]
          break

      team_short_name = st.session_state.team_names[t_idx][:10]
      with row_cols[t_idx]:
        if cell_player_name != "-":
          st.markdown(
              f"<div"
              " style='background-color:#1e293b;border:1px solid"
              " #3b82f6;border-radius:6px;padding:6px;text-align:center;font-size:11px;min-height:60px;'><span"
              f" style='color:#94a3b8;'>{pick_num}.</span><br><b>{cell_player_name}</b><br><span"
              f" style='color:#38bdf8;'>{cell_pos}</span></div>",
              unsafe_allow_html=True,
          )
        else:
          st.markdown(
              f"<div"
              " style='background-color:#0f172a;border:1px solid"
              " #1e293b;border-radius:6px;padding:6px;text-align:center;font-size:11px;min-height:60px;'><span"
              f" style='color:#475569;'>{pick_num}.</span><br><span"
              f" style='color:#64748b;'>{team_short_name}</span></div>",
              unsafe_allow_html=True,
          )
    st.markdown("")

with tab_rosters:
  st.subheader("League Rosters Overview")
  cols = st.columns(2)
  for t_idx in range(NUM_TEAMS):
    col_idx = t_idx % 2
    with cols[col_idx]:
      team_label = st.session_state.team_names[t_idx]
      roster_list = st.session_state.rosters[t_idx]
      st.markdown(f"### {team_label}")
      if roster_list:
        roster_display = " | ".join(
            [f"{p['name']} ({p['pos']})" for p in roster_list]
        )
        st.info(roster_display)
      else:
        st.markdown(
            "<span style='color:#64748b;'>Empty Roster</span>",
            unsafe_allow_html=True,
        )
      st.markdown("---")
          
