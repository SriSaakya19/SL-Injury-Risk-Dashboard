import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="Injury Risk Dashboard", layout="wide")
st.title("🏏 Sports Load & Injury Risk Dashboard")

# 1. Data load
df = pd.read_csv(r"C:\Users\user\Desktop\SL_Injury_Project\data\injury_risk_report.csv")

# 2. Top 10 Risk Players
st.subheader("Top 10 High Risk Players")
st.bar_chart(df.head(10).set_index('player')['Risk_Score'])

# 3. Full Table
st.subheader("Full Risk Report")
st.dataframe(df)

# 4. Player Search WITH PHOTO
st.subheader("Check Specific Player")
player = st.selectbox("Select Player", df['player'].unique())

col1, col2 = st.columns([1, 2])

with col1:
    # LINK PATH EKKADA PASTE CHEYYALI ANTE IKKADA 👇
    photo_path = f"C:\\Users\\user\\Desktop\\SL_Injury_Project\\{player.replace(' ', '_')}.jpg"
    
    if os.path.exists(photo_path):
        image = Image.open(photo_path)
        st.image(image, width=200)
    else:
        st.write("📷 Photo not found")
        st.write(photo_path) # Error vasthe ee path kanipistundi

with col2:
    player_risk = df[df['player']==player]['Risk_Level'].values[0]
    player_score = df[df['player']==player]['Risk_Score'].values[0]
    st.metric(label="Risk Level", value=player_risk)
    st.metric(label="Risk Score", value=f"{player_score:.2f}")
    
    if player_risk == "High Risk":
        st.error("⚠️ Rest Needed!")
    else:
        st.success("✅ Safe to Play")