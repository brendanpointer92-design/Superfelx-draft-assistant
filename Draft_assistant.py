import random
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# --- FANTASYPROS SUPERFLEX 150 PLAYER DATA (Standard Scoring) ---
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
    ("Jaylen Warren", "PIN", "RB"),
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


class DraftApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Superflex Draft Assistant (10-Man Standard)")
    self.root.geometry("1400850")
    self.root.configure(bg="#1e1e1e")

    # League Settings
    self.num_teams = 10
    self.total_rounds = 15
    self.user_team_idx = 0  # Default User is Team 1
    self.current_pick = 1

    # Initialize Teams & Names
    self.team_names = [f"Team {i+1}" for i in range(self.num_teams)]
    self.team_names[0] = "My Team"
    self.rosters = {i: [] for i in range(self.num_teams)}

    # Initialize Player Pool
    self.players = []
    for idx, (name, team, pos) in enumerate(RAW_PLAYERS[:150]):
      self.players.append(
          {
              "id": idx + 1,
              "name": name,
              "team": team,
              "pos": pos,
              "drafted": False,
              "drafted_by": None,
          }
      )

    self.setup_styles()
    self.create_widgets()
    self.update_display()

  def setup_styles(self):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#2d2d2d",
        foreground="white",
        fieldbackground="#2d2d2d",
        rowheight=24,
    )
    style.map("Treeview", background=[("selected", "#007acc")])

  def create_widgets(self):
    # Top Control Bar
    top_frame = tk.Frame(self.root, bg="#252526", height=60)
    top_frame.pack(fill="x", side="top")

    self.status_label = tk.Label(
        top_frame,
        text="",
        font=("Arial", 14, "bold"),
        bg="#252526",
        fg="#4ec9b0",
    )
    self.status_label.pack(side="left", padx=20, pady=15)

    btn_config = {
        "font": ("Arial", 10, "bold"),
        "bg": "#007acc",
        "fg": "white",
        "bd": 0,
        "padx": 10,
        "pady": 5,
    }

    tk.Button(
        top_frame,
        text="Draft Selected",
        command=self.user_draft_player,
        **btn_config,
    ).pack(side="left", padx=10)
    tk.Button(
        top_frame,
        text="Auto-Draft Pick",
        command=self.simulate_single_pick,
        bg="#68217a",
        **btn_config,
    ).pack(side="left", padx=5)
    tk.Button(
        top_frame,
        text="Auto-Draft to My Turn",
        command=self.auto_draft_to_user,
        bg="#b5cea8",
        fg="black",
        **btn_config,
    ).pack(side="left", padx=5)
    tk.Button(
        top_frame,
        text="Rename Teams",
        command=self.rename_teams_dialog,
        bg="#333333",
        **btn_config,
    ).pack(side="right", padx=20)

    # Main Content Panes (Left: Available Players, Right: Tabs for Draft Board & Rosters)
    main_paned = tk.PanedWindow(
        self.root, orient=tk.HORIZONTAL, bg="#1e1e1e", sashwidth=6
    )
    main_paned.pack(fill="both", expand=True, padx=10, pady=10)

    # Left Frame: Available Players
    left_frame = tk.Frame(main_paned, bg="#2d2d2d")
    main_paned.add(left_frame, width=550)

    tk.Label(
        left_frame,
        text="Available Players (FantasyPros Superflex)",
        font=("Arial", 12, "bold"),
        bg="#2d2d2d",
        fg="white",
    ).pack(anchor="w", padx=10, pady=10)

    # Player Treeview
    columns = ("rk", "name", "pos", "team")
    self.player_tree = ttk.Treeview(
        left_frame, columns=columns, show="headings", selectmode="browse"
    )
    self.player_tree.heading("rk", text="Rk")
    self.player_tree.heading("name", text="Player Name")
    self.player_tree.heading("pos", text="Pos")
    self.player_tree.heading("team", text="Team")

    self.player_tree.column("rk", width=40, anchor="center")
    self.player_tree.column("name", width=220, anchor="w")
    self.player_tree.column("pos", width=60, anchor="center")
    self.player_tree.column("team", width=60, anchor="center")

    scrollbar = ttk.Scrollbar(
        left_frame, orient="vertical", command=self.player_tree.yview
    )
    self.player_tree.configure(yscrollcommand=scrollbar.set)

    self.player_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    scrollbar.pack(side="right", fill="y", pady=5)

    # Right Frame: Notebook (Draft Board & Rosters)
    right_frame = tk.Frame(main_paned, bg="#1e1e1e")
    main_paned.add(right_frame, width=800)

    self.notebook = ttk.Notebook(right_frame)
    self.notebook.pack(fill="both", expand=True)

    # Tab 1: Draft Board Grid
    self.board_frame = tk.Frame(self.notebook, bg="#2d2d2d")
    self.notebook.add(self.board_frame, text="Visual Draft Board")

    self.board_canvas = tk.Canvas(self.board_frame, bg="#2d2d2d", highlightthickness=0)
    board_scroll = ttk.Scrollbar(
        self.board_frame, orient="vertical", command=self.board_canvas.yview
    )
    board_xscroll = ttk.Scrollbar(
        self.board_frame, orient="horizontal", command=self.board_canvas.xview
    )
    self.board_canvas.configure(
        yscrollcommand=board_scroll.set, xscrollcommand=board_xscroll.set
    )

    board_scroll.pack(side="right", fill="y")
    board_xscroll.pack(side="bottom", fill="x")
    self.board_canvas.pack(side="left", fill="both", expand=True)

    self.board_inner_frame = tk.Frame(self.board_canvas, bg="#2d2d2d")
    self.board_canvas.create_window(
        (0, 0), window=self.board_inner_frame, anchor="nw"
    )
    self.board_inner_frame.bind(
        "<Configure>",
        lambda e: self.board_canvas.configure(
            scrollregion=self.board_canvas.bbox("all")
        ),
    )

    # Tab 2: Roster View
    self.roster_frame = tk.Frame(self.notebook, bg="#2d2d2d")
    self.notebook.add(self.roster_frame, text="Team Rosters")

    self.roster_tree = ttk.Treeview(
        self.roster_frame, columns=("team", "pos_roster"), show="headings"
    )
    self.roster_tree.heading("team", text="Team")
    self.roster_tree.heading("pos_roster", text="Drafted Roster")
    self.roster_tree.column("team", width=150, anchor="w")
    self.roster_tree.column("pos_roster", width=600, anchor="w")
    self.roster_tree.pack(fill="both", expand=True, padx=10, pady=10)

  def get_current_turn_info(self):
    if self.current_pick > self.num_teams * self.total_rounds:
      return None, None, None

    round_num = (self.current_pick - 1) // self.num_teams + 1
    index_in_round = (self.current_pick - 1) % self.num_teams

    # Snake draft logic
    if round_num % 2 == 1:
      team_idx = index_in_round
    else:
      team_idx = self.num_teams - 1 - index_in_round

    return round_num, index_in_round + 1, team_idx

  def update_display(self):
    # Update Player Tree
    for row in self.player_tree.get_children():
      self.player_tree.delete(row)

    for p in self.players:
      if not p["drafted"]:
        self.player_tree.insert(
            "",
            "end",
            iid=str(p["id"]),
            values=(p["id"], p["name"], p["pos"], p["team"]),
        )

    # Update Status Banner
    round_num, pick_in_round, team_idx = self.get_current_turn_info()
    if round_num is None:
      self.status_label.config(text="DRAFT COMPLETED!", fg="#ce9178")
    else:
      active_team = self.team_names[team_idx]
      turn_text = (
          f"Round {round_num}, Pick {pick_in_round} (Overall {self.current_pick})"
          f" — On the Clock: {active_team}"
      )
      self.status_label.config(
          text=turn_text, fg="#4ec9b0" if team_idx == self.user_team_idx else "white"
      )

    self.draw_draft_board()
    self.update_roster_view()

  def draw_draft_board(self):
    for widget in self.board_inner_frame.winfo_children():
      widget.destroy()

    # Headers (Teams)
    for t_idx in range(self.num_teams):
      lbl = tk.Label(
          self.board_inner_frame,
          text=self.team_names[t_idx],
          font=("Arial", 9, "bold"),
          bg="#333333",
          fg="white",
          width=16,
          relief="ridge",
          padx=2,
          pady=4,
      )
      lbl.grid(row=0, column=t_idx, padx=1, pady=1)

    # Grid Cells (Rounds)
    for r in range(1, self.total_rounds + 1):
      # Round Label
      r_lbl = tk.Label(
          self.board_inner_frame,
          text=f"R{r}",
          font=("Arial", 8),
          bg="#252526",
          fg="#aaaaaa",
          width=4,
      )
      r_lbl.grid(row=r, column=self.num_teams, padx=2, pady=1)

      for t in range(self.num_teams):
        # Determine pick number for this grid slot
        if r % 2 == 1:
          pick_num = (r - 1) * self.num_teams + t + 1
        else:
          pick_num = (r - 1) * self.num_teams + (self.num_teams - t)

        # Find player drafted here
        player_name = ""
        bg_col = "#3c3c3c"
        for p in self.players:
          if p["drafted_by"] == t and p.get("pick_num") == pick_num:
            player_name = f"{p['name']} ({p['pos'])"
            if p["pos"] == "QB":
              bg_col = "#264f78"
            elif p["pos"] == "RB":
              bg_col = "#2d5a27"
            elif p["pos"] == "WR":
              bg_col = "#5a4a27"
            elif p["pos"] == "TE":
              bg_col = "#5a274e"
            break

        cell = tk.Label(
            self.board_inner_frame,
            text=player_name,
            font=("Arial", 8),
            bg=bg_col,
            fg="white",
            width=16,
            height=2,
            relief="sunken",
            wraplength=100,
        )
        cell.grid(row=r, column=t, padx=1, pady=1)

  def update_roster_view(self):
    for row in self.roster_tree.get_children():
      self.roster_tree.delete(row)

    for t_idx in range(self.num_teams):
      roster_str = ", ".join(
          [f"{p['name']} ({p['pos']})" for p in self.rosters[t_idx]]
      )
      self.roster_tree.insert(
          "", "end", values=(self.team_names[t_idx], roster_str)
      )

  def draft_player_action(self, player_id, team_idx):
    for p in self.players:
      if p["id"] == player_id and not p["drafted"]:
        p["drafted"] = True
        p["drafted_by"] = team_idx
        p["pick_num"] = self.current_pick
        self.rosters[team_idx].append(p)
        self.current_pick += 1
        return True
    return False

  def user_draft_player(self):
    round_num, _, team_idx = self.get_current_turn_info()
    if round_num is None:
      messagebox.showinfo("Draft Over", "The draft has concluded!")
      return

    if team_idx != self.user_team_idx:
      if (
          not messagebox.askyesno(
              "Out of Turn",
              f"It is currently {self.team_names[team_idx]}'s turn. Draft"
              " anyway for your team?",
          )
          == True
      ):
        return

    selected = self.player_tree.selection()
    if not selected:
      messagebox.showwarning(
          "Selection Error", "Please select an available player from the list."
      )
      return

    player_id = int(selected[0])
    self.draft_player_action(player_id, self.user_team_idx)
    self.update_display()

  def simulate_single_pick(self):
    round_num, _, team_idx = self.get_current_turn_info()
    if round_num is None:
      return

    # AI Logic: Pick highest available player based on positional needs/value
    available = [p for p in self.players if not p["drafted"]]
    if not available:
      return

    # Simple smart heuristic for CPU: favor QBs early in Superflex, else best available ranking
    chosen_player = available[0]
    if round_num <= 3:
      qbs = [p for p in available if p["pos"] == "QB"]
      if qbs and random.random() < 0.7:
        chosen_player = qbs[0]

    self.draft_player_action(chosen_player["id"], team_idx)
    self.update_display()

  def auto_draft_to_user(self):
    round_num, _, team_idx = self.get_current_turn_info()
    if round_num is None:
      return

    # Simulate picks until it hits user turn or draft ends
    while team_idx is not None and team_idx != self.user_team_idx:
      self.simulate_single_pick()
      round_num, _, team_idx = self.get_current_turn_info()

    self.update_display()

  def rename_teams_dialog(self):
    popup = tk.Toplevel(self.root)
    popup.title("Rename Teams")
    popup.geometry("350-450")
    popup.configure(bg="#2d2d2d")

    tk.Label(
        popup,
        text="Customize Franchise Names",
        font=("Arial", 11, "bold"),
        bg="#2d2d2d",
        fg="white",
    ).pack(pady=10)

    entries = []
    for i in range(self.num_teams):
      f = tk.Frame(popup, bg="#2d2d2d")
      f.pack(fill="x", padx=20, pady=2)
      tk.Label(
          f, text=f"Team {i+1}:", width=10, anchor="w", bg="#2d2d2d", fg="white"
      ).pack(side="left")
      ent = tk.Entry(f, width=20)
      ent.insert(0, self.team_names[i])
      ent.pack(side="right")
      entries.append(ent)

    def save_names():
      for i, ent in enumerate(entries):
        val = ent.get().strip()
        if val:
          self.team_names[i] = val
      popup.destroy()
      self.update_display()

    tk.Button(
        popup,
        text="Save Names",
        command=save_names,
        bg="#007acc",
        fg="white",
        font=("Arial", 10, "bold"),
    ).pack(pady=15)


if __name__ == "__main__":
  root = tk.Tk()
  app = DraftApp(root)
  root.mainloop()
      
