import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("uber65.csv")

# Combine DATE and TIME
df['DateTime'] = pd.to_datetime(df['DATE'] + " " + df['TIME'])

# Create new columns
df['Hour'] = df['DateTime'].dt.hour
df['Month'] = df['DateTime'].dt.month
df['Weekday'] = df['DateTime'].dt.day_name()

# Dashboard layout
plt.figure(figsize=(18,12))

# 1️⃣ Bar Chart – Trips by Hour
plt.subplot(3,3,1)
sns.countplot(x='Hour', data=df)
plt.title("Bar Chart - Trips by Hour")

# 2️⃣ Line Chart – Trips by Hour
plt.subplot(3,3,2)
df['Hour'].value_counts().sort_index().plot()
plt.title("Line Chart - Trips by Hour")

# 3️⃣ Area Chart – Trips by Hour
plt.subplot(3,3,3)
df['Hour'].value_counts().sort_index().plot.area()
plt.title("Area Chart")

# 4️⃣ Pie Chart – Trips by Month
plt.subplot(3,3,4)
df['Month'].value_counts().plot.pie(autopct='%1.1f%%')
plt.ylabel("")
plt.title("Pie Chart - Month")

# 5️⃣ Donut Chart – Trips by Month
plt.subplot(3,3,5)
month_counts = df['Month'].value_counts()
plt.pie(month_counts, labels=month_counts.index,
        wedgeprops=dict(width=0.4), autopct='%1.1f%%')
plt.title("Donut Chart")

# 6️⃣ Scatter Plot – Hour vs Month
plt.subplot(3,3,6)
plt.scatter(df['Hour'], df['Month'])
plt.title("Scatter Plot")

# 7️⃣ Heatmap – Weekday vs Hour
plt.subplot(3,3,7)
pivot = df.groupby(['Weekday','Hour']).size().unstack()
sns.heatmap(pivot, cmap="coolwarm")
plt.title("Heatmap")

# 8️⃣ Histogram – Distribution of Hours
plt.subplot(3,3,8)
plt.hist(df['Hour'], bins=24)
plt.title("Histogram")

# 9️⃣ KPI Card – Total Trips
plt.subplot(3,3,9)
plt.text(0.5, 0.5, f"Total Trips\n{len(df)}",
         fontsize=18, ha='center')
plt.axis('off')

plt.tight_layout()
plt.show()