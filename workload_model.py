import pandas as pd
import os

# Iddaru kalipi
BASE_PATH = r"C:\Users\user\Desktop\SL_Injury_Project"

matches = pd.read_csv(os.path.join(BASE_PATH, 'data', 'matches.csv'))
deliveries = pd.read_csv(os.path.join(BASE_PATH, 'data', 'deliveries.csv'))

df = deliveries.merge(matches[['id', 'date', 'season']], left_on='match_id', right_on='id')
df['date'] = pd.to_datetime(df['date'])

bowler_workload = df.groupby('bowler').agg(Total_Balls_Bowled = ('ball', 'count')).reset_index()
batsman_workload = df.groupby('batter').agg(Total_Balls_Faced = ('ball', 'count')).reset_index()

player_workload = pd.concat([
    bowler_workload.rename(columns={'bowler':'player', 'Total_Balls_Bowled':'Total_Balls'}),
    batsman_workload.rename(columns={'batter':'player', 'Total_Balls_Faced':'Total_Balls'})
])

player_workload.to_csv(os.path.join(BASE_PATH, 'data', 'player_workload.csv'), index=False)

print("✅ Files saved successfully!")