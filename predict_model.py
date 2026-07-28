import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. INJURY RISK REPORT file ni chaduvudam - idi important
df = pd.read_csv(r"C:\Users\user\Desktop\SL_Injury_Project\data\injury_risk_report.csv")

# 2. Target column create cheddam: Risk > 20 ante High Risk = 1
df['High_Risk'] = (df['Risk_Score'] > 20).astype(int)

# 3. Features and Target separate cheddam
X = df[['Total_Balls']] # ippudu Total_Balls matrame undi
y = df['High_Risk']

# 4. Train and Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Model train cheyyi
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Predict and Accuracy check
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model Accuracy: {accuracy*100:.2f}%")
print("\nModel is ready to predict High Risk players!")

# 7. BONUS: Nithish Kumar Reddy risk entha chuddam
nithish_data = df[df['player'].str.contains('Nithish', case=False)]
if not nithish_data.empty:
    nithish_pred = model.predict(nithish_data[['Total_Balls']])
    print(f"\nNithish Kumar Reddy Prediction: {'High Risk' if nithish_pred[0]==1 else 'Low Risk'}")
    # Nuvvu evarini check cheyyalo ikkada name pettu
player_name = "Nithish Kumar Reddy" 
player_data = df[df['player'].str.contains(player_name, case=False)]

if not player_data.empty:
    player_pred = model.predict(player_data[['Total_Balls']])
    print(f"\n{player_name} Prediction: {'High Risk' if player_pred[0]==1 else 'Low Risk'}")
else:
    print(f"\n{player_name} data not found")