import streamlit as st
import pandas as pd
import requests
import numpy as np

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="2026 10-Team Superflex Fantasy Draft Assistant",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM STYLING
# -----------------------------------------------------------------------------
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
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. 10-TEAM SUPERFLEX DEFAULT DATASET (TOP 150 EXPANDED CONSENSUS)
# -----------------------------------------------------------------------------
DEFAULT_PLAYERS = [
    # Tier 1 - Elite QBs & Superflex Anchors
    {"Rank": 1, "Name": "Josh Allen", "Pos": "QB", "Team": "BUF", "Tier": 1, "ProjPts": 418.0, "Bye": 7},
    {"Rank": 2, "Name": "Lamar Jackson", "Pos": "QB", "Team": "BAL", "Tier": 1, "ProjPts": 405.0, "Bye": 13},
    {"Rank": 3, "Name": "Drake Maye", "Pos": "QB", "Team": "NE", "Tier": 1, "ProjPts": 395.0, "Bye": 11},
    {"Rank": 4, "Name": "Joe Burrow", "Pos": "QB", "Team": "CIN", "Tier": 1, "ProjPts": 385.0, "Bye": 6},
    {"Rank": 5, "Name": "Jayden Daniels", "Pos": "QB", "Team": "WAS", "Tier": 1, "ProjPts": 375.0, "Bye": 7},
    {"Rank": 6, "Name": "Jalen Hurts", "Pos": "QB", "Team": "PHI", "Tier": 1, "ProjPts": 370.0, "Bye": 10},
    {"Rank": 7, "Name": "Ja'Marr Chase", "Pos": "WR", "Team": "CIN", "Tier": 2, "ProjPts": 350.0, "Bye": 6},
    {"Rank": 8, "Name": "Puka Nacua", "Pos": "WR", "Team": "LAR", "Tier": 2, "ProjPts": 340.0, "Bye": 11},
    {"Rank": 9, "Name": "Caleb Williams", "Pos": "QB", "Team": "CHI", "Tier": 2, "ProjPts": 335.0, "Bye": 10},
    {"Rank": 10, "Name": "Jahmyr Gibbs", "Pos": "RB", "Team": "DET", "Tier": 2, "ProjPts": 345.0, "Bye": 6},
    {"Rank": 11, "Name": "Justin Herbert", "Pos": "QB", "Team": "LAC", "Tier": 2, "ProjPts": 330.0, "Bye": 7},
    {"Rank": 12, "Name": "Bijan Robinson", "Pos": "RB", "Team": "ATL", "Tier": 2, "ProjPts": 350.0, "Bye": 11},
    {"Rank": 13, "Name": "Jaxon Smith-Njigba", "Pos": "WR", "Team": "SEA", "Tier": 3, "ProjPts": 325.0, "Bye": 11},
    {"Rank": 14, "Name": "Trevor Lawrence", "Pos": "QB", "Team": "JAC", "Tier": 3, "ProjPts": 315.0, "Bye": 7},
    {"Rank": 15, "Name": "Dak Prescott", "Pos": "QB", "Team": "DAL", "Tier": 3, "ProjPts": 310.0, "Bye": 14},
    {"Rank": 16, "Name": "Amon-Ra St. Brown", "Pos": "WR", "Team": "DET", "Tier": 3, "ProjPts": 320.0, "Bye": 6},
    {"Rank": 17, "Name": "Christian McCaffrey", "Pos": "RB", "Team": "SF", "Tier": 3, "ProjPts": 330.0, "Bye": 8},
    {"Rank": 18, "Name": "CeeDee Lamb", "Pos": "WR", "Team": "DAL", "Tier": 3, "ProjPts": 315.0, "Bye": 14},
    {"Rank": 19, "Name": "Brock Purdy", "Pos": "QB", "Team": "SF", "Tier": 3, "ProjPts": 305.0, "Bye": 8},
    {"Rank": 20, "Name": "Jaxson Dart", "Pos": "QB", "Team": "NYG", "Tier": 3, "ProjPts": 300.0, "Bye": 8},
    
    # Ranks 21 - 50
    {"Rank": 21, "Name": "Patrick Mahomes II", "Pos": "QB", "Team": "KC", "Tier": 4, "ProjPts": 298.0, "Bye": 5},
    {"Rank": 22, "Name": "Jonathan Taylor", "Pos": "RB", "Team": "IND", "Tier": 4, "ProjPts": 304.0, "Bye": 13},
    {"Rank": 23, "Name": "Justin Jefferson", "Pos": "WR", "Team": "MIN", "Tier": 4, "ProjPts": 297.0, "Bye": 6},
    {"Rank": 24, "Name": "Ashton Jeanty", "Pos": "RB", "Team": "LV", "Tier": 4, "ProjPts": 299.0, "Bye": 13},
    {"Rank": 25, "Name": "Jordan Love", "Pos": "QB", "Team": "GB", "Tier": 4, "ProjPts": 295.0, "Bye": 10},
    {"Rank": 26, "Name": "Tua Tagovailoa", "Pos": "QB", "Team": "MIA", "Tier": 4, "ProjPts": 292.0, "Bye": 6},
    {"Rank": 27, "Name": "Kyler Murray", "Pos": "QB", "Team": "ARI", "Tier": 4, "ProjPts": 290.0, "Bye": 8},
    {"Rank": 28, "Name": "Saquon Barkley", "Pos": "RB", "Team": "PHI", "Tier": 4, "ProjPts": 273.0, "Bye": 10},
    {"Rank": 29, "Name": "James Cook", "Pos": "RB", "Team": "BUF", "Tier": 4, "ProjPts": 294.0, "Bye": 7},
    {"Rank": 30, "Name": "Drake London", "Pos": "WR", "Team": "ATL", "Tier": 4, "ProjPts": 283.0, "Bye": 11},
    {"Rank": 31, "Name": "A.J. Brown", "Pos": "WR", "Team": "NE", "Tier": 5, "ProjPts": 283.0, "Bye": 11},
    {"Rank": 32, "Name": "Rashee Rice", "Pos": "WR", "Team": "KC", "Tier": 5, "ProjPts": 296.0, "Bye": 5},
    {"Rank": 33, "Name": "Nico Collins", "Pos": "WR", "Team": "HOU", "Tier": 5, "ProjPts": 280.0, "Bye": 8},
    {"Rank": 34, "Name": "Breece Hall", "Pos": "RB", "Team": "NYJ", "Tier": 5, "ProjPts": 275.0, "Bye": 12},
    {"Rank": 35, "Name": "Garrett Wilson", "Pos": "WR", "Team": "NYJ", "Tier": 5, "ProjPts": 272.0, "Bye": 12},
    {"Rank": 36, "Name": "Anthony Richardson", "Pos": "QB", "Team": "IND", "Tier": 5, "ProjPts": 285.0, "Bye": 13},
    {"Rank": 37, "Name": "Bo Nix", "Pos": "QB", "Team": "DEN", "Tier": 5, "ProjPts": 282.0, "Bye": 14},
    {"Rank": 38, "Name": "Marvin Harrison Jr.", "Pos": "WR", "Team": "ARI", "Tier": 5, "ProjPts": 268.0, "Bye": 8},
    {"Rank": 39, "Name": "Malik Nabers", "Pos": "WR", "Team": "NYG", "Tier": 5, "ProjPts": 265.0, "Bye": 8},
    {"Rank": 40, "Name": "Kyren Williams", "Pos": "RB", "Team": "LAR", "Tier": 5, "ProjPts": 262.0, "Bye": 11},
    {"Rank": 41, "Name": "De'Von Achane", "Pos": "RB", "Team": "MIA", "Tier": 6, "ProjPts": 260.0, "Bye": 6},
    {"Rank": 42, "Name": "Jared Goff", "Pos": "QB", "Team": "DET", "Tier": 6, "ProjPts": 278.0, "Bye": 6},
    {"Rank": 43, "Name": "Matthew Stafford", "Pos": "QB", "Team": "LAR", "Tier": 6, "ProjPts": 274.0, "Bye": 11},
    {"Rank": 44, "Name": "Kirk Cousins", "Pos": "QB", "Team": "ATL", "Tier": 6, "ProjPts": 270.0, "Bye": 11},
    {"Rank": 45, "Name": "Brock Bowers", "Pos": "TE", "Team": "LV", "Tier": 6, "ProjPts": 255.0, "Bye": 13},
    {"Rank": 46, "Name": "Trey McBride", "Pos": "TE", "Team": "ARI", "Tier": 6, "ProjPts": 248.0, "Bye": 8},
    {"Rank": 47, "Name": "Davante Adams", "Pos": "WR", "Team": "NYJ", "Tier": 6, "ProjPts": 252.0, "Bye": 12},
    {"Rank": 48, "Name": "Chris Olave", "Pos": "WR", "Team": "NO", "Tier": 6, "ProjPts": 250.0, "Bye": 12},
    {"Rank": 49, "Name": "Kenneth Walker III", "Pos": "RB", "Team": "KC", "Tier": 6, "ProjPts": 245.0, "Bye": 5},
    {"Rank": 50, "Name": "Derrick Henry", "Pos": "RB", "Team": "BAL", "Tier": 6, "ProjPts": 248.0, "Bye": 13},

    # Ranks 51 - 100
    {"Rank": 51, "Name": "Deebo Samuel", "Pos": "WR", "Team": "SF", "Tier": 7, "ProjPts": 242.0, "Bye": 8},
    {"Rank": 52, "Name": "Michael Pittman Jr.", "Pos": "WR", "Team": "IND", "Tier": 7, "ProjPts": 240.0, "Bye": 13},
    {"Rank": 53, "Name": "Zay Flowers", "Pos": "WR", "Team": "BAL", "Tier": 7, "ProjPts": 238.0, "Bye": 13},
    {"Rank": 54, "Name": "Aaron Jones", "Pos": "RB", "Team": "MIN", "Tier": 7, "ProjPts": 235.0, "Bye": 6},
    {"Rank": 55, "Name": "Isiah Pacheco", "Pos": "RB", "Team": "KC", "Tier": 7, "ProjPts": 232.0, "Bye": 5},
    {"Rank": 56, "Name": "Joe Mixon", "Pos": "RB", "Team": "HOU", "Tier": 7, "ProjPts": 230.0, "Bye": 8},
    {"Rank": 57, "Name": "Geno Smith", "Pos": "QB", "Team": "SEA", "Tier": 7, "ProjPts": 255.0, "Bye": 11},
    {"Rank": 58, "Name": "Russell Wilson", "Pos": "QB", "Team": "PIT", "Tier": 7, "ProjPts": 252.0, "Bye": 9},
    {"Rank": 59, "Name": "Aaron Rodgers", "Pos": "QB", "Team": "PIT", "Tier": 7, "ProjPts": 250.0, "Bye": 9},
    {"Rank": 60, "Name": "Deshaun Watson", "Pos": "QB", "Team": "CLE", "Tier": 7, "ProjPts": 248.0, "Bye": 10},
    {"Rank": 61, "Name": "Sam LaPorta", "Pos": "TE", "Team": "DET", "Tier": 8, "ProjPts": 225.0, "Bye": 6},
    {"Rank": 62, "Name": "Mark Andrews", "Pos": "TE", "Team": "BAL", "Tier": 8, "ProjPts": 220.0, "Bye": 13},
    {"Rank": 63, "Name": "George Kittle", "Pos": "TE", "Team": "SF", "Tier": 8, "ProjPts": 218.0, "Bye": 8},
    {"Rank": 64, "Name": "Travis Kelce", "Pos": "TE", "Team": "KC", "Tier": 8, "ProjPts": 215.0, "Bye": 5},
    {"Rank": 65, "Name": "Terry McLaurin", "Pos": "WR", "Team": "WAS", "Tier": 8, "ProjPts": 230.0, "Bye": 7},
    {"Rank": 66, "Name": "DK Metcalf", "Pos": "WR", "Team": "SEA", "Tier": 8, "ProjPts": 228.0, "Bye": 11},
    {"Rank": 67, "Name": "Stefon Diggs", "Pos": "WR", "Team": "HOU", "Tier": 8, "ProjPts": 225.0, "Bye": 8},
    {"Rank": 68, "Name": "Amari Cooper", "Pos": "WR", "Team": "CLE", "Tier": 8, "ProjPts": 222.0, "Bye": 10},
    {"Rank": 69, "Name": "Christian Kirk", "Pos": "WR", "Team": "JAC", "Tier": 8, "ProjPts": 220.0, "Bye": 7},
    {"Rank": 70, "Name": "Rhamondre Stevenson", "Pos": "RB", "Team": "NE", "Tier": 8, "ProjPts": 218.0, "Bye": 11},
    {"Rank": 71, "Name": "Travis Etienne Jr.", "Pos": "RB", "Team": "JAC", "Tier": 9, "ProjPts": 215.0, "Bye": 7},
    {"Rank": 72, "Name": "Alvin Kamara", "Pos": "RB", "Team": "NO", "Tier": 9, "ProjPts": 212.0, "Bye": 12},
    {"Rank": 73, "Name": "Tony Pollard", "Pos": "RB", "Team": "TEN", "Tier": 9, "ProjPts": 210.0, "Bye": 5},
    {"Rank": 74, "Name": "Kenneth Walker III", "Pos": "RB", "Team": "SEA", "Tier": 9, "ProjPts": 208.0, "Bye": 11},
    {"Rank": 75, "Name": "Will Levis", "Pos": "QB", "Team": "TEN", "Tier": 9, "ProjPts": 240.0, "Bye": 5},
    {"Rank": 76, "Name": "Bryce Young", "Pos": "QB", "Team": "CAR", "Tier": 9, "ProjPts": 238.0, "Bye": 11},
    {"Rank": 77, "Name": "J.J. McCarthy", "Pos": "QB", "Team": "MIN", "Tier": 9, "ProjPts": 235.0, "Bye": 6},
    {"Rank": 78, "Name": "Michael Penix Jr.", "Pos": "QB", "Team": "ATL", "Tier": 9, "ProjPts": 232.0, "Bye": 11},
    {"Rank": 79, "Name": "Cade Klubnik", "Pos": "QB", "Team": "TB", "Tier": 9, "ProjPts": 230.0, "Bye": 11},
    {"Rank": 80, "Name": "Khalil Shakir", "Pos": "WR", "Team": "BUF", "Tier": 9, "ProjPts": 215.0, "Bye": 7},
    {"Rank": 81, "Name": "Tank Dell", "Pos": "WR", "Team": "HOU", "Tier": 10, "ProjPts": 212.0, "Bye": 8},
    {"Rank": 82, "Name": "George Pickens", "Pos": "WR", "Team": "PIT", "Tier": 10, "ProjPts": 210.0, "Bye": 9},
    {"Rank": 83, "Name": "Calvin Ridley", "Pos": "WR", "Team": "TEN", "Tier": 10, "ProjPts": 208.0, "Bye": 5},
    {"Rank": 84, "Name": "Chris Godwin", "Pos": "WR", "Team": "TB", "Tier": 10, "ProjPts": 205.0, "Bye": 11},
    {"Rank": 85, "Name": "Keenan Allen", "Pos": "WR", "Team": "CHI", "Tier": 10, "ProjPts": 202.0, "Bye": 10},
    {"Rank": 86, "Name": "David Montgomery", "Pos": "RB", "Team": "DET", "Tier": 10, "ProjPts": 205.0, "Bye": 6},
    {"Rank": 87, "Name": "Zamir White", "Pos": "RB", "Team": "LV", "Tier": 10, "ProjPts": 200.0, "Bye": 13},
    {"Rank": 88, "Name": "Brian Robinson Jr.", "Pos": "RB", "Team": "WAS", "Tier": 10, "ProjPts": 198.0, "Bye": 7},
    {"Rank": 89, "Name": "Javonte Williams", "Pos": "RB", "Team": "DEN", "Tier": 10, "ProjPts": 195.0, "Bye": 14},
    {"Rank": 90, "Name": "Zack Moss", "Pos": "RB", "Team": "CIN", "Tier": 10, "ProjPts": 192.0, "Bye": 6},
    {"Rank": 91, "Name": "Evan Engram", "Pos": "TE", "Team": "JAC", "Tier": 11, "ProjPts": 195.0, "Bye": 7},
    {"Rank": 92, "Name": "Dalton Kincaid", "Pos": "TE", "Team": "BUF", "Tier": 11, "ProjPts": 192.0, "Bye": 7},
    {"Rank": 93, "Name": "Kyle Pitts", "Pos": "TE", "Team": "ATL", "Tier": 11, "ProjPts": 190.0, "Bye": 11},
    {"Rank": 94, "Name": "Pat Freiermuth", "Pos": "TE", "Team": "PIT", "Tier": 11, "ProjPts": 185.0, "Bye": 9},
    {"Rank": 95, "Name": "Dallas Goedert", "Pos": "TE", "Team": "PHI", "Tier": 11, "ProjPts": 182.0, "Bye": 10},
    {"Rank": 96, "Name": "Diontae Johnson", "Pos": "WR", "Team": "CAR", "Tier": 11, "ProjPts": 195.0, "Bye": 11},
    {"Rank": 97, "Name": "Courtland Sutton", "Pos": "WR", "Team": "DEN", "Tier": 11, "ProjPts": 192.0, "Bye": 14},
    {"Rank": 98, "Name": "Hollywood Brown", "Pos": "WR", "Team": "KC", "Tier": 11, "ProjPts": 190.0, "Bye": 5},
    {"Rank": 99, "Name": "DeAndre Hopkins", "Pos": "WR", "Team": "TEN", "Tier": 11, "ProjPts": 188.0, "Bye": 5},
    {"Rank": 100, "Name": "Curtis Samuel", "Pos": "WR", "Team": "BUF", "Tier": 11, "ProjPts": 185.0, "Bye": 7},

    # Ranks 101 - 150
    {"Rank": 101, "Name": "Tyjae Spears", "Pos": "RB", "Team": "TEN", "Tier": 12, "ProjPts": 180.0, "Bye": 5},
    {"Rank": 102, "Name": "Nick Chubb", "Pos": "RB", "Team": "CLE", "Tier": 12, "ProjPts": 178.0, "Bye": 10},
    {"Rank": 103, "Name": "Jonathon Brooks", "Pos": "RB", "Team": "CAR", "Tier": 12, "ProjPts": 175.0, "Bye": 11},
    {"Rank": 104, "Name": "Jaylen Warren", "Pos": "RB", "Team": "PIT", "Tier": 12, "ProjPts": 172.0, "Bye": 9},
    {"Rank": 105, "Name": "Blake Corum", "Pos": "RB", "Team": "LAR", "Tier": 12, "ProjPts": 170.0, "Bye": 11},
    {"Rank": 106, "Name": "Trey Benson", "Pos": "RB", "Team": "ARI", "Tier": 12, "ProjPts": 168.0, "Bye": 8},
    {"Rank": 107, "Name": "MarShawn Lloyd", "Pos": "RB", "Team": "GB", "Tier": 12, "ProjPts": 165.0, "Bye": 10},
    {"Rank": 108, "Name": "Braelon Allen", "Pos": "RB", "Team": "NYJ", "Tier": 12, "ProjPts": 162.0, "Bye": 12},
    {"Rank": 109, "Name": "Ray Davis", "Pos": "RB", "Team": "BUF", "Tier": 12, "ProjPts": 160.0, "Bye": 7},
    {"Rank": 110, "Name": "Audric Estime", "Pos": "RB", "Team": "DEN", "Tier": 12, "ProjPts": 158.0, "Bye": 14},
    {"Rank": 111, "Name": "Desmond Ridder", "Pos": "QB", "Team": "ARI", "Tier": 13, "ProjPts": 210.0, "Bye": 8},
    {"Rank": 112, "Name": "Kenny Pickett", "Pos": "QB", "Team": "PHI", "Tier": 13, "ProjPts": 208.0, "Bye": 10},
    {"Rank": 113, "Name": "Jacoby Brissett", "Pos": "QB", "Team": "NE", "Tier": 13, "ProjPts": 205.0, "Bye": 11},
    {"Rank": 114, "Name": "Gardner Minshew", "Pos": "QB", "Team": "LV", "Tier": 13, "ProjPts": 202.0, "Bye": 13},
    {"Rank": 115, "Name": "Sam Howell", "Pos": "QB", "Team": "SEA", "Tier": 13, "ProjPts": 200.0, "Bye": 11},
    {"Rank": 116, "Name": "Rashid Shaheed", "Pos": "WR", "Team": "NO", "Tier": 13, "ProjPts": 175.0, "Bye": 12},
    {"Rank": 117, "Name": "Jameson Williams", "Pos": "WR", "Team": "DET", "Tier": 13, "ProjPts": 172.0, "Bye": 6},
    {"Rank": 118, "Name": "Joshua Palmer", "Pos": "WR", "Team": "LAC", "Tier": 13, "ProjPts": 170.0, "Bye": 7},
    {"Rank": 119, "Name": "Adonai Mitchell", "Pos": "WR", "Team": "IND", "Tier": 13, "ProjPts": 168.0, "Bye": 13},
    {"Rank": 120, "Name": "Ladd McConkey", "Pos": "WR", "Team": "LAC", "Tier": 13, "ProjPts": 165.0, "Bye": 7},
    {"Rank": 121, "Name": "Xavier Worthy", "Pos": "WR", "Team": "KC", "Tier": 14, "ProjPts": 162.0, "Bye": 5},
    {"Rank": 122, "Name": "Brian Thomas Jr.", "Pos": "WR", "Team": "JAC", "Tier": 14, "ProjPts": 160.0, "Bye": 7},
    {"Rank": 123, "Name": "Keon Coleman", "Pos": "WR", "Team": "BUF", "Tier": 14, "ProjPts": 158.0, "Bye": 7},
    {"Rank": 124, "Name": "Roman Wilson", "Pos": "WR", "Team": "PIT", "Tier": 14, "ProjPts": 155.0, "Bye": 9},
    {"Rank": 125, "Name": "Ricky Pearsall", "Pos": "WR", "Team": "SF", "Tier": 14, "ProjPts": 152.0, "Bye": 8},
    {"Rank": 126, "Name": "Jalen McMillan", "Pos": "WR", "Team": "TB", "Tier": 14, "ProjPts": 150.0, "Bye": 11},
    {"Rank": 127, "Name": "Ja'Lynn Polk", "Pos": "WR", "Team": "NE", "Tier": 14, "ProjPts": 148.0, "Bye": 11},
    {"Rank": 128, "Name": "Troy Franklin", "Pos": "WR", "Team": "DEN", "Tier": 14, "ProjPts": 145.0, "Bye": 14},
    {"Rank": 129, "Name": "Luke McCaffrey", "Pos": "WR", "Team": "WAS", "Tier": 14, "ProjPts": 142.0, "Bye": 7},
    {"Rank": 130, "Name": "Malachi Corley", "Pos": "WR", "Team": "NYJ", "Tier": 14, "ProjPts": 140.0, "Bye": 12},
    {"Rank": 131, "Name": "Ben Sinnott", "Pos": "TE", "Team": "WAS", "Tier": 15, "ProjPts": 145.0, "Bye": 7},
    {"Rank": 132, "Name": "Ja'Tavion Sanders", "Pos": "TE", "Team": "CAR", "Tier": 15, "ProjPts": 142.0, "Bye": 11},
    {"Rank": 133, "Name": "Theo Johnson", "Pos": "TE", "Team": "NYG", "Tier": 15, "ProjPts": 140.0, "Bye": 8},
    {"Rank": 134, "Name": "Erick All", "Pos": "TE", "Team": "CIN", "Tier": 15, "ProjPts": 138.0, "Bye": 6},
    {"Rank": 135, "Name": "Jared Wiley", "Pos": "TE", "Team": "KC", "Tier": 15, "ProjPts": 135.0, "Bye": 5},
    {"Rank": 136, "Name": "Tyler Conklin", "Pos": "TE", "Team": "NYJ", "Tier": 15, "ProjPts": 132.0, "Bye": 12},
    {"Rank": 137, "Name": "Juwan Johnson", "Pos": "TE", "Team": "NO", "Tier": 15, "ProjPts": 130.0, "Bye": 12},
    {"Rank": 138, "Name": "Chigoziem Okonkwo", "Pos": "TE", "Team": "TEN", "Tier": 15, "ProjPts": 128.0, "Bye": 5},
    {"Rank": 139, "Name": "Noah Fant", "Pos": "TE", "Team": "SEA", "Tier": 15, "ProjPts": 125.0, "Bye": 11},
    {"Rank": 140, "Name": "Greg Dulcich", "Pos": "TE", "Team": "DEN", "Tier": 15, "ProjPts": 122.0, "Bye": 14},
    {"Rank": 141, "Name": "Ezekiel Elliott", "Pos": "RB", "Team": "DAL", "Tier": 16, "ProjPts": 140.0, "Bye": 14},
    {"Rank": 142, "Name": "Kareem Hunt", "Pos": "RB", "Team": "FA", "Tier": 16, "ProjPts": 138.0, "Bye": 10},
    {"Rank": 143, "Name": "AJ Dillon", "Pos": "RB", "Team": "GB", "Tier": 16, "ProjPts": 135.0, "Bye": 10},
    {"Rank": 144, "Name": "Rico Dowdle", "Pos": "RB", "Team": "DAL", "Tier": 16, "ProjPts": 132.0, "Bye": 14},
    {"Rank": 145, "Name": "Chuba Hubbard", "Pos": "RB", "Team": "CAR", "Tier": 16, "ProjPts": 130.0, "Bye": 11},
    {"Rank": 146, "Name": "Tyler Allgeier", "Pos": "RB", "Team": "ATL", "Tier": 16, "ProjPts": 128.0, "Bye": 11},
    {"Rank": 147, "Name": "Roschon Johnson", "Pos": "RB", "Team": "CHI", "Tier": 16, "ProjPts": 125.0, "Bye": 10},
    {"Rank": 148, "Name": "Dameon Pierce", "Pos": "RB", "Team": "HOU", "Tier": 16, "ProjPts": 122.0, "Bye": 8},
    {"Rank": 149, "Name": "Antonio Gibson", "Pos": "RB", "Team": "NE", "Tier": 16, "ProjPts": 120.0, "Bye": 11},
    {"Rank": 150, "Name": "Emanuel Wilson", "Pos": "RB", "Team": "GB", "Tier": 16, "ProjPts": 118.0, "Bye": 10}
]

# -----------------------------------------------------------------------------
# 4. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if 'players_df' not in st.session_state:
    df_init = pd.DataFrame(DEFAULT_PLAYERS)
    df_init['Drafted'] = False
    df_init['Drafted_By'] = None
    df_init['Pick_Num'] = None
    st.session_state.players_df = df_init

if 'num_teams' not in st.session_state: st.session_state.num_teams = 10
if 'num_rounds' not in st.session_state: st.session_state.num_rounds = 15
if 'user_team_num' not in st.session_state: st.session_state.user_team_num = 1
if 'current_pick' not in st.session_state: st.session_state.current_pick = 1
if 'draft_history' not in st.session_state: st.session_state.draft_history = []
if 'is_mock_mode' not in st.session_state: st.session_state.is_mock_mode = False

# -----------------------------------------------------------------------------
# 5. SUPERFLEX VBD CALCULATIONS
# -----------------------------------------------------------------------------
def calculate_vbd(df, te_premium=1.0):
    working_df = df.copy()
    working_df.loc[working_df['Pos'] == 'TE', 'ProjPts'] *= te_premium
    
    baselines = {}
    replacement_ranks = {'QB': 20, 'RB': 25, 'WR': 30, 'TE': 10}
    
    for pos, rank_idx in replacement_ranks.items():
        pos_df = working_df[working_df['Pos'] == pos].sort_values(by='ProjPts', ascending=False)
        if len(pos_df) >= rank_idx:
            baselines[pos] = pos_df.iloc[rank_idx - 1]['ProjPts']
        elif not pos_df.empty:
            baselines[pos] = pos_df.iloc[-1]['ProjPts']
        else:
            baselines[pos] = 0.0
            
    working_df['VBD'] = working_df.apply(lambda row: row['Pr
