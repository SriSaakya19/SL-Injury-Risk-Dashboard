import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="SL Injury Risk Dashboard", layout="wide")

st.title("🏏 Sri Lanka Cricket - Injury Risk Dashboard")
st.markdown("---")

# CSV load cheyyadam - Streamlit Cloud kosam 'data/' tho start
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/player_workload.csv')
        return df
    except FileNotFoundError:
        st.error("Error: 'data/player_workload.csv' file dorakaledu. GitHub lo 'data' folder unda check cheyyi.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # Sidebar filters
    st.sidebar.header("Filters")
    players = st.sidebar.multiselect("Player select cheyyi", df['Player'].unique(), default=df['Player'].unique()[:3])
    
    filtered_df = df[df['Player'].isin(players)]
    
    # Main dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Player Workload Data")
        st.dataframe(filtered_df, use_container_width=True)
    
    with col2:
        st.subheader("📈 Workload Trend")
        if 'Date' in df.columns and 'Workload' in df.columns:
            for player in players:
                player_data = filtered_df[filtered_df['Player'] == player]
                st.line_chart(player_data.set_index('Date')['Workload'])
        else:
            st.write("Columns: Date, Player, Workload undali CSV lo")
    
    # Risk indicator
    st.subheader("⚠️ Injury Risk Alert")
    if 'Workload' in df.columns:
        high_risk = filtered_df[filtered_df['Workload'] > 100]  # example threshold
        if not high_risk.empty:
            st.warning(f"{len(high_risk)} records lo high workload kanipinchindi")
        else:
            st.success("All players are in safe workload zone")

else:
    st.stop()

st.markdown("---")
st.caption("Built with Streamlit for SL Cricket Team")