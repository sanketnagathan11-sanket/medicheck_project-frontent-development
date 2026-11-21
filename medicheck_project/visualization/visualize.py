"""
MediCheck — Data Visualization (Assignment 5, 24CsDscU3002)
Reads bookings_data.csv, displays its content, then plots a
Line Chart, Bar Chart, and Pie Chart using Pandas + Matplotlib.
"""
import pandas as pd
import matplotlib.pyplot as plt

# ---- 1. Load and display the CSV content -------------------------
df = pd.read_csv("bookings_data.csv")

print("First 10 rows:")
print(df.head(10))
print("\nShape:", df.shape)
print("\nSummary stats:")
print(df.describe(include="all"))

# ---- 2. LINE CHART: monthly revenue trend -------------------------
monthly_revenue = df.groupby("Month")["Revenue"].sum()

plt.figure(figsize=(8, 5))
plt.plot(monthly_revenue.index, monthly_revenue.values,
         marker="o", color="#1F4D42", linewidth=2)
plt.title("MediCheck: Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (Rs.)")
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("charts_line_revenue_trend.png", dpi=150)
plt.close()

# ---- 3. BAR CHART: bookings by test category -----------------------
category_bookings = df.groupby("Category")["Bookings"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
plt.bar(category_bookings.index, category_bookings.values, color="#4C8B6F")
plt.title("MediCheck: Total Bookings by Test Category")
plt.xlabel("Category")
plt.ylabel("Number of Bookings")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("charts_bar_category_bookings.png", dpi=150)
plt.close()

# ---- 4. PIE CHART: Mass vs Premium share of bookings ----------------
tier_share = df.groupby("Tier")["Bookings"].sum()

plt.figure(figsize=(6, 6))
plt.pie(tier_share.values, labels=tier_share.index, autopct="%1.1f%%",
        colors=["#4C8B6F", "#D99A34"], startangle=90)
plt.title("MediCheck: Mass vs Premium Booking Share")
plt.tight_layout()
plt.savefig("charts_pie_tier_share.png", dpi=150)
plt.close()

print("\nSaved: charts_line_revenue_trend.png, charts_bar_category_bookings.png, "
      "charts_pie_tier_share.png")
