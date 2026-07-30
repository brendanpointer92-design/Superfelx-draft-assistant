import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Fantasy Football Draft Assistant (Superflex)",
    page_icon="🏈",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 1. EXPANDED DEFAULT DATASET (PLAYERS 1 TO 150)
# -----------------------------------------------------------------------------
DEFAULT_PLAYERS = [
    {"Rank": 1, "Name": "Josh Allen", "Pos": "QB", "Team": "BUF", "Tier": 1, "ProjPts": 395.0, "Bye": 12},
    {"Rank": 2, "Name": "Lamar Jackson", "Pos": "QB", "Team": "BAL", "Tier": 1, "ProjPts": 380.0, "Bye": 14},
    {"Rank": 3, "Name": "Drake Maye", "Pos": "QB", "Team": "NE", "Tier": 1, "ProjPts": 345.0, "Bye": 11},
    {"Rank": 4, "Name": "Joe Burrow", "Pos": "QB", "Team": "CIN", "Tier": 1, "ProjPts": 350.0, "Bye": 12},
    {"Rank": 5, "Name": "Jayden Daniels", "Pos": "QB", "Team": "WAS", "Tier": 2, "ProjPts": 340.0, "Bye": 14},
    {"Rank": 6, "Name": "Jalen Hurts", "Pos": "QB", "Team": "PHI", "Tier": 2, "ProjPts": 355.0, "Bye": 5},
    {"Rank": 7, "Name": "Jahmyr Gibbs", "Pos": "RB", "Team": "DET", "Tier": 2, "ProjPts": 310.0, "Bye": 5},
    {"Rank": 8, "Name": "Bijan Robinson", "Pos": "RB", "Team": "ATL", "Tier": 2, "ProjPts": 320.0, "Bye": 12},
    {"Rank": 9, "Name": "Ja'Marr Chase", "Pos": "WR", "Team": "CIN", "Tier": 2, "ProjPts": 330.0, "Bye": 12},
    {"Rank": 10, "Name": "Caleb Williams", "Pos": "QB", "Team": "CHI", "Tier": 2, "ProjPts": 315.0, "Bye": 7},
    {"Rank": 11, "Name": "Justin Herbert", "Pos": "QB", "Team": "LAC", "Tier": 2, "ProjPts": 305.0, "Bye": 5},
    {"Rank": 12, "Name": "Puka Nacua", "Pos": "WR", "Team": "LAR", "Tier": 2, "ProjPts": 310.0, "Bye": 6},
    {"Rank": 13, "Name": "Dak Prescott", "Pos": "QB", "Team": "DAL", "Tier": 3, "ProjPts": 300.0, "Bye": 7},
    {"Rank": 14, "Name": "Trevor Lawrence", "Pos": "QB", "Team": "JAC", "Tier": 3, "ProjPts": 290.0, "Bye": 12},
    {"Rank": 15, "Name": "Jaxon Smith-Njigba", "Pos": "WR", "Team": "SEA", "Tier": 3, "ProjPts": 285.0, "Bye": 10},
    {"Rank": 16, "Name": "Amon-Ra St. Brown", "Pos": "WR", "Team": "DET", "Tier": 3, "ProjPts": 305.0, "Bye": 5},
    {"Rank": 17, "Name": "Jonathan Taylor", "Pos": "RB", "Team": "IND", "Tier": 3, "ProjPts": 275.0, "Bye": 14},
    {"Rank": 18, "Name": "Brock Purdy", "Pos": "QB", "Team": "SF", "Tier": 3, "ProjPts": 295.0, "Bye": 9},
    {"Rank": 19, "Name": "Christian McCaffrey", "Pos": "RB", "Team": "SF", "Tier": 3, "ProjPts": 290.0, "Bye": 9},
    {"Rank": 20, "Name": "Jaxson Dart", "Pos": "QB", "Team": "NYG", "Tier": 3, "ProjPts": 280.0, "Bye": 11},
    {"Rank": 21, "Name": "CeeDee Lamb", "Pos": "WR", "Team": "DAL", "Tier": 4, "ProjPts": 315.0, "Bye": 7},
    {"Rank": 22, "Name": "Justin Jefferson", "Pos": "WR", "Team": "MIN", "Tier": 4, "ProjPts": 320.0, "Bye": 6},
    {"Rank": 23, "Name": "Saquon Barkley", "Pos": "RB", "Team": "PHI", "Tier": 4, "ProjPts": 285.0, "Bye": 5},
    {"Rank": 24, "Name": "James Cook", "Pos": "RB", "Team": "BUF", "Tier": 4, "ProjPts": 250.0, "Bye": 12},
    {"Rank": 25, "Name": "Derrick Henry", "Pos": "RB", "Team": "BAL", "Tier": 4, "ProjPts": 260.0, "Bye": 14},
    {"Rank": 26, "Name": "Malik Nabers", "Pos": "WR", "Team": "NYG", "Tier": 4, "ProjPts": 275.0, "Bye": 11},
    {"Rank": 27, "Name": "Nico Collins", "Pos": "WR", "Team": "HOU", "Tier": 4, "ProjPts": 270.0, "Bye": 14},
    {"Rank": 28, "Name": "Brian Thomas Jr.", "Pos": "WR", "Team": "JAC", "Tier": 4, "ProjPts": 260.0, "Bye": 12},
    {"Rank": 29, "Name": "Patrick Mahomes II", "Pos": "QB", "Team": "KC", "Tier": 4, "ProjPts": 325.0, "Bye": 6},
    {"Rank": 30, "Name": "Brock Bowers", "Pos": "TE", "Team": "LV", "Tier": 5, "ProjPts": 240.0, "Bye": 10},
    {"Rank": 31, "Name": "Trey McBride", "Pos": "TE", "Team": "ARI", "Tier": 5, "ProjPts": 230.0, "Bye": 11},
    {"Rank": 32, "Name": "Bo Nix", "Pos": "QB", "Team": "DEN", "Tier": 5, "ProjPts": 270.0, "Bye": 14},
    {"Rank": 33, "Name": "Kyler Murray", "Pos": "QB", "Team": "MIN", "Tier": 5, "ProjPts": 285.0, "Bye": 6},
    {"Rank": 34, "Name": "Bucky Irving", "Pos": "RB", "Team": "TB", "Tier": 5, "ProjPts": 225.0, "Bye": 11},
    {"Rank": 35, "Name": "De'Von Achane", "Pos": "RB", "Team": "MIA", "Tier": 5, "ProjPts": 240.0, "Bye": 6},
    {"Rank": 36, "Name": "Ashton Jeanty", "Pos": "RB", "Team": "LV", "Tier": 5, "ProjPts": 235.0, "Bye": 10},
    {"Rank": 37, "Name": "Jordan Love", "Pos": "QB", "Team": "GB", "Tier": 5, "ProjPts": 290.0, "Bye": 10},
    {"Rank": 38, "Name": "A.J. Brown", "Pos": "WR", "Team": "NE", "Tier": 5, "ProjPts": 265.0, "Bye": 11},
    {"Rank": 39, "Name": "Drake London", "Pos": "WR", "Team": "ATL", "Tier": 5, "ProjPts": 255.0, "Bye": 12},
    {"Rank": 40, "Name": "George Kittle", "Pos": "TE", "Team": "SF", "Tier": 6, "ProjPts": 200.0, "Bye": 9},
    {"Rank": 41, "Name": "Breece Hall", "Pos": "RB", "Team": "NYJ", "Tier": 6, "ProjPts": 245.0, "Bye": 12},
    {"Rank": 42, "Name": "Kyren Williams", "Pos": "RB", "Team": "LAR", "Tier": 6, "ProjPts": 240.0, "Bye": 6},
    {"Rank": 43, "Name": "Travis Etienne Jr.", "Pos": "RB", "Team": "JAC", "Tier": 6, "ProjPts": 230.0, "Bye": 12},
    {"Rank": 44, "Name": "Kenneth Walker III", "Pos": "RB", "Team": "SEA", "Tier": 6, "ProjPts": 235.0, "Bye": 10},
    {"Rank": 45, "Name": "Garrett Wilson", "Pos": "WR", "Team": "NYJ", "Tier": 6, "ProjPts": 250.0, "Bye": 12},
    {"Rank": 46, "Name": "Marvin Harrison Jr.", "Pos": "WR", "Team": "ARI", "Tier": 6, "ProjPts": 245.0, "Bye": 11},
    {"Rank": 47, "Name": "Deebo Samuel Sr.", "Pos": "WR", "Team": "WAS", "Tier": 6, "ProjPts": 235.0, "Bye": 14},
    {"Rank": 48, "Name": "Davante Adams", "Pos": "WR", "Team": "LV", "Tier": 6, "ProjPts": 225.0, "Bye": 10},
    {"Rank": 49, "Name": "Tyreek Hill", "Pos": "WR", "Team": "MIA", "Tier": 6, "ProjPts": 260.0, "Bye": 6},
    {"Rank": 50, "Name": "Cooper Kupp", "Pos": "WR", "Team": "LAR", "Tier": 6, "ProjPts": 215.0, "Bye": 6},
    {"Rank": 51, "Name": "Mark Andrews", "Pos": "TE", "Team": "BAL", "Tier": 7, "ProjPts": 190.0, "Bye": 14},
    {"Rank": 52, "Name": "Sam LaPorta", "Pos": "TE", "Team": "DET", "Tier": 7, "ProjPts": 205.0, "Bye": 5},
    {"Rank": 53, "Name": "T.J. Hockenson", "Pos": "TE", "Team": "MIN", "Tier": 7, "ProjPts": 195.0, "Bye": 6},
    {"Rank": 54, "Name": "Kyle Pitts", "Pos": "TE", "Team": "ATL", "Tier": 7, "ProjPts": 175.0, "Bye": 12},
    {"Rank": 55, "Name": "Aaron Jones", "Pos": "RB", "Team": "MIN", "Tier": 7, "ProjPts": 210.0, "Bye": 6},
    {"Rank": 56, "Name": "Rachaad White", "Pos": "RB", "Team": "TB", "Tier": 7, "ProjPts": 215.0, "Bye": 11},
    {"Rank": 57, "Name": "Isiah Pacheco", "Pos": "RB", "Team": "KC", "Tier": 7, "ProjPts": 220.0, "Bye": 6},
    {"Rank": 58, "Name": "Josh Jacobs", "Pos": "RB", "Team": "GB", "Tier": 7, "ProjPts": 225.0, "Bye": 10},
    {"Rank": 59, "Name": "Alvin Kamara", "Pos": "RB", "Team": "NO", "Tier": 7, "ProjPts": 218.0, "Bye": 12},
    {"Rank": 60, "Name": "Joe Mixon", "Pos": "RB", "Team": "HOU", "Tier": 7, "ProjPts": 222.0, "Bye": 14},
    {"Rank": 61, "Name": "DK Metcalf", "Pos": "WR", "Team": "SEA", "Tier": 8, "ProjPts": 230.0, "Bye": 10},
    {"Rank": 62, "Name": "Chris Olave", "Pos": "WR", "Team": "NO", "Tier": 8, "ProjPts": 232.0, "Bye": 12},
    {"Rank": 63, "Name": "Michael Pittman Jr.", "Pos": "WR", "Team": "IND", "Tier": 8, "ProjPts": 210.0, "Bye": 14},
    {"Rank": 64, "Name": "Zay Flowers", "Pos": "WR", "Team": "BAL", "Tier": 8, "ProjPts": 208.0, "Bye": 14},
    {"Rank": 65, "Name": "Tank Dell", "Pos": "WR", "Team": "HOU", "Tier": 8, "ProjPts": 195.0, "Bye": 14},
    {"Rank": 66, "Name": "Rashee Rice", "Pos": "WR", "Team": "KC", "Tier": 8, "ProjPts": 240.0, "Bye": 6},
    {"Rank": 67, "Name": "Stefon Diggs", "Pos": "WR", "Team": "HOU", "Tier": 8, "ProjPts": 212.0, "Bye": 14},
    {"Rank": 68, "Name": "Amari Cooper", "Pos": "WR", "Team": "BUF", "Tier": 8, "ProjPts": 205.0, "Bye": 12},
    {"Rank": 69, "Name": "Tee Higgins", "Pos": "WR", "Team": "CIN", "Tier": 8, "ProjPts": 200.0, "Bye": 12},
    {"Rank": 70, "Name": "DeVonta Smith", "Pos": "WR", "Team": "PHI", "Tier": 8, "ProjPts": 215.0, "Bye": 5},
    {"Rank": 71, "Name": "Matthew Stafford", "Pos": "QB", "Team": "LAR", "Tier": 9, "ProjPts": 265.0, "Bye": 6},
    {"Rank": 72, "Name": "Aaron Rodgers", "Pos": "QB", "Team": "NYJ", "Tier": 9, "ProjPts": 255.0, "Bye": 12},
    {"Rank": 73, "Name": "Tua Tagovailoa", "Pos": "QB", "Team": "MIA", "Tier": 9, "ProjPts": 260.0, "Bye": 6},
    {"Rank": 74, "Name": "Kirk Cousins", "Pos": "QB", "Team": "ATL", "Tier": 9, "ProjPts": 250.0, "Bye": 12},
    {"Rank": 75, "Name": "Anthony Richardson", "Pos": "QB", "Team": "IND", "Tier": 9, "ProjPts": 275.0, "Bye": 14},
    {"Rank": 76, "Name": "Deshaun Watson", "Pos": "QB", "Team": "CLE", "Tier": 9, "ProjPts": 240.0, "Bye": 10},
    {"Rank": 77, "Name": "Will Levis", "Pos": "QB", "Team": "TEN", "Tier": 9, "ProjPts": 220.0, "Bye": 5},
    {"Rank": 78, "Name": "C.J. Stroud", "Pos": "QB", "Team": "HOU", "Tier": 9, "ProjPts": 290.0, "Bye": 14},
    {"Rank": 79, "Name": "J.K. Dobbins", "Pos": "RB", "Team": "LAC", "Tier": 9, "ProjPts": 185.0, "Bye": 5},
    {"Rank": 80, "Name": "Tony Pollard", "Pos": "RB", "Team": "TEN", "Tier": 9, "ProjPts": 190.0, "Bye": 5},
    {"Rank": 81, "Name": "Najee Harris", "Pos": "RB", "Team": "PIT", "Tier": 10, "ProjPts": 195.0, "Bye": 9},
    {"Rank": 82, "Name": "Jaylen Warren", "Pos": "RB", "Team": "PIT", "Tier": 10, "ProjPts": 180.0, "Bye": 9},
    {"Rank": 83, "Name": "David Montgomery", "Pos": "RB", "Team": "DET", "Tier": 10, "ProjPts": 200.0, "Bye": 5},
    {"Rank": 84, "Name": "Zamir White", "Pos": "RB", "Team": "LV", "Tier": 10, "ProjPts": 170.0, "Bye": 10},
    {"Rank": 85, "Name": "Ezekiel Elliott", "Pos": "RB", "Team": "DAL", "Tier": 10, "ProjPts": 150.0, "Bye": 7},
    {"Rank": 86, "Name": "Rhamondre Stevenson", "Pos": "RB", "Team": "NE", "Tier": 10, "ProjPts": 190.0, "Bye": 11},
    {"Rank": 87, "Name": "Brian Robinson Jr.", "Pos": "RB", "Team": "WAS", "Tier": 10, "ProjPts": 192.0, "Bye": 14},
    {"Rank": 88, "Name": "Chuba Hubbard", "Pos": "RB", "Team": "CAR", "Tier": 10, "ProjPts": 175.0, "Bye": 11},
    {"Rank": 89, "Name": "Khalil Herbert", "Pos": "RB", "Team": "CIN", "Tier": 10, "ProjPts": 140.0, "Bye": 12},
    {"Rank": 90, "Name": "Tyler Allgeier", "Pos": "RB", "Team": "ATL", "Tier": 10, "ProjPts": 135.0, "Bye": 12},
    {"Rank": 91, "Name": "Jerome Ford", "Pos": "RB", "Team": "CLE", "Tier": 11, "ProjPts": 165.0, "Bye": 10},
    {"Rank": 92, "Name": "Gus Edwards", "Pos": "RB", "Team": "LAC", "Tier": 11, "ProjPts": 145.0, "Bye": 5},
    {"Rank": 93, "Name": "Tyjae Spears", "Pos": "RB", "Team": "TEN", "Tier": 11, "ProjPts": 155.0, "Bye": 5},
    {"Rank": 94, "Name": "Zach Charbonnet", "Pos": "RB", "Team": "SEA", "Tier": 11, "ProjPts": 150.0, "Bye": 10},
    {"Rank": 95, "Name": "Blake Corum", "Pos": "RB", "Team": "LAR", "Tier": 11, "ProjPts": 130.0, "Bye": 6},
    {"Rank": 96, "Name": "MarShawn Lloyd", "Pos": "RB", "Team": "GB", "Tier": 11, "ProjPts": 125.0, "Bye": 10},
    {"Rank": 97, "Name": "Ray Davis", "Pos": "RB", "Team": "BUF", "Tier": 11, "ProjPts": 120.0, "Bye": 12},
    {"Rank": 98, "Name": "Trey Benson", "Pos": "RB", "Team": "ARI", "Tier": 11, "ProjPts": 135.0, "Bye": 11},
    {"Rank": 99, "Name": "Courtland Sutton", "Pos": "WR", "Team": "DEN", "Tier": 11, "ProjPts": 185.0, "Bye": 14},
    {"Rank": 100, "Name": "Christian Kirk", "Pos": "WR", "Team": "JAC", "Tier": 11, "ProjPts": 180.0, "Bye": 12},
    {"Rank": 101, "Name": "Calvin Ridley", "Pos": "WR", "Team": "TEN", "Tier": 12, "ProjPts": 190.0, "Bye": 5},
    {"Rank": 102, "Name": "Terry McLaurin", "Pos": "WR", "Team": "WAS", "Tier": 12, "ProjPts": 195.0, "Bye": 14},
    {"Rank": 103, "Name": "Diontae Johnson", "Pos": "WR", "Team": "BAL", "Tier": 12, "ProjPts": 182.0, "Bye": 14},
    {"Rank": 104, "Name": "Keenan Allen", "Pos": "WR", "Team": "CHI", "Tier": 12, "ProjPts": 188.0, "Bye": 7},
    {"Rank": 105, "Name": "Chris Godwin", "Pos": "WR", "Team": "TB", "Tier": 12, "ProjPts": 198.0, "Bye": 11},
    {"Rank": 106, "Name": "Mike Evans", "Pos": "WR", "Team": "TB", "Tier": 12, "ProjPts": 210.0, "Bye": 11},
    {"Rank": 107, "Name": "Hollywood Brown", "Pos": "WR", "Team": "KC", "Tier": 12, "ProjPts": 175.0, "Bye": 6},
    {"Rank": 108, "Name": "Jahan Dotson", "Pos": "WR", "Team": "PHI", "Tier": 12, "ProjPts": 140.0, "Bye": 5},
    {"Rank": 109, "Name": "Jordan Addison", "Pos": "WR", "Team": "MIN", "Tier": 12, "ProjPts": 178.0, "Bye": 6},
    {"Rank": 110, "Name": "Xavier Worthy", "Pos": "WR", "Team": "KC", "Tier": 12, "ProjPts": 170.0, "Bye": 6},
    {"Rank": 111, "Name": "Ladd McConkey", "Pos": "WR", "Team": "LAC", "Tier": 13, "ProjPts": 165.0, "Bye": 5},
    {"Rank": 112, "Name": "Keon Coleman", "Pos": "WR", "Team": "BUF", "Tier": 13, "ProjPts": 160.0, "Bye": 12},
    {"Rank": 113, "Name": "Rome Odunze", "Pos": "WR", "Team": "CHI", "Tier": 13, "ProjPts": 172.0, "Bye": 7},
    {"Rank": 114, "Name": "Adonai Mitchell", "Pos": "WR", "Team": "IND", "Tier": 13, "ProjPts": 135.0, "Bye": 14},
    {"Rank": 115, "Name": "Ja'Lynn Polk", "Pos": "WR", "Team": "NE", "Tier": 13, "ProjPts": 130.0, "Bye": 11},
    {"Rank": 116, "Name": "Ricky Pearsall", "Pos": "WR", "Team": "SF", "Tier": 13, "ProjPts": 125.0, "Bye": 9},
    {"Rank": 117, "Name": "Dallas Goedert", "Pos": "TE", "Team": "PHI", "Tier": 13, "ProjPts": 150.0, "Bye": 5},
    {"Rank": 118, "Name": "Evan Engram", "Pos": "TE", "Team": "JAC", "Tier": 13, "ProjPts": 168.0, "Bye": 12},
    {"Rank": 119, "Name": "Pat Freiermuth", "Pos": "TE", "Team": "PIT", "Tier": 13, "ProjPts": 140.0, "Bye": 9},
    {"Rank": 120, "Name": "David Njoku", "Pos": "TE", "Team": "CLE", "Tier": 13, "ProjPts": 160.0, "Bye": 10},
    {"Rank": 121, "Name": "Jake Ferguson", "Pos": "TE", "Team": "DAL", "Tier": 14, "ProjPts": 155.0, "Bye": 7},
    {"Rank": 122, "Name": "Dalton Kincaid", "Pos": "TE", "Team": "BUF", "Tier": 14, "ProjPts": 162.0, "Bye": 12},
    {"Rank": 123, "Name": "Taysom Hill", "Pos": "TE", "Team": "NO", "Tier": 14, "ProjPts": 130.0, "Bye": 12},
    {"Rank": 124, "Name": "Cole Kmet", "Pos": "TE", "Team": "CHI", "Tier": 14, "ProjPts": 145.0, "Bye": 7},
    {"Rank": 125, "Name": "Russell Wilson", "Pos": "QB", "Team": "PIT", "Tier": 14, "ProjPts": 230.0, "Bye": 9},
    {"Rank": 126, "Name": "Geno Smith", "Pos": "QB", "Team": "SEA", "Tier": 14, "ProjPts": 235.0, "Bye": 10},
    {"Rank": 127, "Name": "Derek Carr", "Pos": "QB", "Team": "NO", "Tier": 14, "ProjPts": 225.0, "Bye": 12},
    {"Rank": 128, "Name": "Bryce Young", "Pos": "QB", "Team": "CAR", "Tier": 14, "ProjPts": 210.0, "Bye": 11},
    {"Rank": 129, "Name": "Justin Fields", "Pos": "QB", "Team": "PIT", "Tier": 14, "ProjPts": 220.0, "Bye": 9},
    {"Rank": 130, "Name": "Baker Mayfield", "Pos": "QB", "Team": "TB", "Tier": 14, "ProjPts": 245.0, "Bye": 11},
    {"Rank": 131, "Name": "Sam Darnold", "Pos": "QB", "Team": "MIN", "Tier": 15, "ProjPts": 215.0, "Bye": 6},
    {"Rank": 132, "Name": "Joe Flacco", "Pos": "QB", "Team": "IND", "Tier": 15, "ProjPts": 190.0, "Bye": 14},
    {"Rank": 133, "Name": "Khalil Shakir", "Pos": "WR", "Team": "BUF", "Tier": 15, "ProjPts": 120.0, "Bye": 12},
    {"Rank": 134, "Name": "Demarcus Robinson", "Pos": "WR", "Team": "LAR", "Tier": 15, "ProjPts": 115.0, "Bye": 6},
    {"Rank": 135, "Name": "Rashod Bateman", "Pos": "WR", "Team": "BAL", "Tier": 15, "ProjPts": 118.0, "Bye": 14},
    {"Rank": 136, "Name": "Curtis Samuel", "Pos": "WR", "Team": "BUF", "Tier": 15, "ProjPts": 122.0, "Bye": 12},
    {"Rank": 137, "Name": "Tyler Boyd", "Pos": "WR", "Team": "TEN", "Tier": 15, "ProjPts": 110.0, "Bye": 5},
    {"Rank": 138, "Name": "Josh Downs", "Pos": "WR", "Team": "IND", "Tier": 15, "ProjPts": 125.0, "Bye": 14},
    {"Rank": 139, "Name": "Wan'Dale Robinson", "Pos": "WR", "Team": "NYG", "Tier": 15, "ProjPts": 115.0, "Bye": 11},
    {"Rank": 140, "Name": "Kendrick Bourne", "Pos": "WR", "Team": "NE", "Tier": 15, "ProjPts": 105.0, "Bye": 11},
    {"Rank": 141, "Name": "Luke Musgrave", "Pos": "TE", "Team": "GB", "Tier": 16, "ProjPts": 110.0, "Bye": 10},
    {"Rank": 142, "Name": "Michael Mayer", "Pos": "TE", "Team": "LV", "Tier": 16, "ProjPts": 105.0, "Bye": 10},
    {"Rank": 143, "Name": "Noah Fant", "Pos": "TE", "Team": "SEA", "Tier": 16, "ProjPts": 100.0, "Bye": 10},
    {"Rank": 144, "Name": "Juwan Johnson", "Pos": "TE", "Team": "NO", "Tier": 16, "ProjPts": 102.0, "Bye": 12},
    {"Rank": 145, "Name": "Emanuel Wilson", "Pos": "RB", "Team": "GB", "Tier": 16, "ProjPts": 95.0, "Bye": 10},
    {"Rank": 146, "Name": "Antonio Gibson", "Pos": "RB", "Team": "NE", "Tier": 16, "ProjPts": 112.0, "Bye": 11},
    {"Rank": 147, "Name": "Dameon Pierce", "Pos": "RB", "Team": "HOU", "Tier": 16, "ProjPts": 90.0, "Bye": 14},
    {"Rank": 148, "Name": "Clyde Edwards-Helaire", "Pos": "RB", "Team": "KC", "Tier": 16, "ProjPts": 88.0, "Bye": 6},
    {"Rank": 149, "Name": "Gardner Minshew II", "Pos": "QB", "Team": "LV", "Tier": 16, "ProjPts": 180.0, "Bye": 10},
    {"Rank": 150, "Name": "Jacoby Brissett", "Pos": "QB", "Team": "NE", "Tier": 16, "ProjPts": 170.0, "Bye": 11}
]

# -----------------------------------------------------------------------------
# 2. SESSION STATE SETUP
# -----------------------------------------------------------------------------
if 'players_df' not in st.session_state:
    df = pd.DataFrame(DEFAULT_PLAYERS)
    df['Drafted'] = False
    df['DraftedBy'] = None
    st.session_state['players_df'] = df

if 'my_roster' not in st.session_state:
    st.session_state['my_roster'] = []

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & LEAGUE SETTINGS
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ League Settings")
league_type = st.sidebar.selectbox("League Format", ["Superflex (10-Team)", "1QB PPR (10-Team)"])
scoring_system = st.sidebar.selectbox("Scoring System", ["PPR", "Half-PPR", "Standard"])

st.sidebar.markdown("---")
st.sidebar.header("🛠️ Draft Controls")
search_query = st.sidebar.text_input("Search Player")
pos_filter = st.sidebar.multiselect("Filter Position", ["QB", "RB", "WR", "TE"], default=["QB", "RB", "WR", "TE"])

if st.sidebar.button("🔄 Reset Draft Board"):
    st.session_state['players_df']['Drafted'] = False
    st.session_state['players_df']['DraftedBy'] = None
    st.session_state['my_roster'] = []
    st.rerun()

# -----------------------------------------------------------------------------
# 4. MAIN INTERFACE & VBD CALCULATIONS
# -----------------------------------------------------------------------------
st.title("🏈 Fantasy Football Draft Assistant")
st.markdown("Live 150-Player Board optimized for competitive Superflex formats.")

df = st.session_state['players_df']

# Simple VBD Calculation Baseline
# Baseline replacement scores (approximate baseline for top 10-team leagues)
baselines = {'QB': 180.0, 'RB': 120.0, 'WR': 130.0, 'TE': 100.0}
df['VBD'] = df.apply(lambda row: max(0.0, row['ProjPts'] - baselines.get(row['Pos'], 100.0)), axis=1)

# Apply filters
filtered_df = df[df['Pos'].isin(pos_filter)]
if search_query:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(search_query, case=False)]

# Tabs for layout structure
tab1, tab2, tab3 = st.tabs(["📋 Draft Board", "👤 My Roster", "📊 Tier Breakdown"])

with tab1:
    st.subheader("Available Player Rankings (Top 150)")
    
    # Display table with interactive selection
    available_players = filtered_df[~filtered_df['Drafted']]
    
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        st.dataframe(
            available_players[['Rank', 'Name', 'Pos', 'Team', 'Tier', 'ProjPts', 'VBD', 'Bye']],
            use_container_width=True,
            hide_index=True
        )
    
    with col_right:
        st.markdown("### Draft Player")
        player_to_draft = st.selectbox("Select Player to Draft", available_players['Name'].tolist())
        
        col_btn1, col_btn2 = st.columns
