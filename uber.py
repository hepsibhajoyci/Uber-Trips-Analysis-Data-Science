# =====================================
# UBER TRIPS DATA ANALYSIS PROJECT
# =====================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("uber65.csv")

# Combine DATE and TIME
df['DateTime'] = pd.to_datetime(df['DATE'] + " " + df['TIME'])

# Create new columns
df['Hour'] = df['DateTime'].dt.hour
df['Day'] = df['DateTime'].dt.day
df['Month'] = df['DateTime'].dt.month
df['Weekday'] = df['DateTime'].dt.day_name()

# ===============================
# DATA VISUALIZATION
# ===============================

# 1️⃣ Trips by Hour
plt.figure()
sns.countplot(x='Hour', data=df)
plt.title("Trips by Hour")
plt.show()

plt.close()   # <-- important

# 2️⃣ Trips by Month
plt.figure()
sns.countplot(x='Month', data=df)
plt.title("Trips by Month")
plt.show()

plt.close()

# 3️⃣ Trips by Weekday
plt.figure()
sns.countplot(x='Weekday', data=df)
plt.xticks(rotation=45)
plt.title("Trips by Weekday")
plt.show()

plt.close()

# 4️⃣ Heatmap
pivot = df.groupby(['Weekday', 'Hour']).size().unstack()

plt.figure()
sns.heatmap(pivot)
plt.title("Heatmap (Weekday vs Hour)")
plt.show()

plt.close()

print("Analysis Completed Successfully ✅")