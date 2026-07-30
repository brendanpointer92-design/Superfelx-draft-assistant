import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Superflex Draft Assistant", page_icon="🏈", layout="wide"
)

st.title("🏈 Superflex Draft Assistant")
st.markdown(
    "Manage your draft board, track player tiers, and filter rankings effortlessly."
)

# Sidebar for controls and file upload
st.sidebar.header("Configuration & Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload custom rankings (.csv)", type=["csv"]
)

# Default embedded fallback data (so the app works instantly even without uploading)
DEFAULT_DATA = """Rank,Name,Pos,Team,ProjPts
1,J. Allen,QB,BUF,427.8
2,L. Jackson,QB,BAL,425.6
3,D. Maye,QB,NE,423.4
4,J. Burrow,QB,CIN,421.2
5,J. Daniels,QB,WAS,419.0
6,J. Hurts,QB,PHI,416.8
7,J. Gibbs,RB,DET,414.6
8,B. Robinson,RB,ATL,412.4
9,J. Chase,WR,CIN,410.2
10,C. Williams,QB,CHI,408.0
11,J. Herbert,QB,LAC,405.8
12,P. Nacua,WR,LAR,403.6
13,T. Lawrence,QB,JAC,401.4
14,J. Smith-Njigba,WR,SEA,399.2
15,D. Prescott,QB,DAL,397.0
16,A. St. Brown,WR,DET,394.8
17,J. Taylor,RB,IND,392.6
18,B. Purdy,QB,SF,390.4
19,C. McCaffrey,RB,SF,388.2
20,K. Murray,QB,ARI,386.0"""

# Load data logic
@st.cache_data
def load_data(file):
    if file is not None:
        try:
            return pd.read_csv(file)
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")
    # Fallback to default string stream if no file uploaded
    from io import StringIO

    return pd.read_csv(StringIO(DEFAULT_DATA))


df = load_data(uploaded_file)

# Ensure columns exist and format correctly
required_columns = ["Rank", "Name", "Pos", "Team", "ProjPts"]
if not all(col in df.columns for col in required_columns):
    st.error(
        f"Your CSV is missing required columns. Ensure columns are: {required_columns}"
    )
else:
    # Sidebar Filters
    st.sidebar.subheader("Filters")
    positions = ["All"] + sorted(df["Pos"].dropna().unique().tolist())
    selected_pos = st.sidebar.selectbox("Filter by Position", positions)

    search_query = st.sidebar.text_input("Search Player Name", "")

    # Apply filters
    filtered_df = df.copy()
    if selected_pos != "All":
        filtered_df = filtered_df[filtered_df["Pos"] == selected_pos]
    if search_query:
        filtered_df = filtered_df[
            filtered_df["Name"]
            .str.contains(search_query, case=False, na=False)
        ]

    # Main dashboard metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Players Available", len(df))
    col2.metric("Filtered Players", len(filtered_df))
    col3.metric("Top Projected Player", df.iloc[0]["Name"] if not df.empty else "N/A")

    st.markdown("---")

    # Display interactive dataframe
    st.subheader("📋 Draft Board Rankings")
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )
    
