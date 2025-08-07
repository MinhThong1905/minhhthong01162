import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cấu hình Seaborn
sns.set_style('whitegrid')

# Tải dữ liệu
@st.cache_data
def load_data():
    df = pd.read_csv("Walmart_Sales.csv")
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')    
    return df

df = load_data()

st.title("📊 Phân Tích Doanh Thu Walmart")
st.markdown("Dữ liệu doanh thu hàng tuần từ các cửa hàng Walmart. Các biểu đồ dưới đây trình bày phân tích theo thời gian, địa điểm, và theo ngày lễ.")

# 1. Biểu đồ Tổng doanh thu mỗi 3 tháng
# Drop rows with invalid or missing 'Date'
df.dropna(subset=['Date'], inplace=True)

# Create quarter labels in 'YYYY-Qx' format
df['Quarter3M'] = df['Date'].dt.year.astype(str) + '-Q' + (((df['Date'].dt.month - 1) // 3) + 1).astype(str)

# Group by quarter and sum total sales
quarterly_sales = df.groupby('Quarter3M')['Weekly_Sales'].sum().reset_index()

# Plotting
fig, ax = plt.subplots(figsize=(14, 7))
ax.bar(quarterly_sales['Quarter3M'], quarterly_sales['Weekly_Sales'], color='lightblue')

ax.set_title('Tổng Doanh Thu Mỗi Quý (3 Tháng)', fontsize=16)
ax.set_xlabel('Quý (Năm - Qx)', fontsize=14)
ax.set_ylabel('Tổng Doanh Thu', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.6)

# Improve readability of x-axis labels
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

# Display the plot in Streamlit
st.subheader("1. Tổng Doanh Thu Mỗi Quý (3 Tháng)")
st.pyplot(fig)

# 2. Biểu đồ Doanh thu theo Ngày
st.subheader("2. Tổng Doanh Thu theo Ngày")
daily_sales = df.groupby('Date')['Weekly_Sales'].sum()

fig2, ax2 = plt.subplots(figsize=(12, 6))
daily_sales.plot(ax=ax2)
ax2.set_title('Tổng Doanh Thu theo Ngày')
ax2.set_xlabel('Ngày')
ax2.set_ylabel('Tổng Doanh Thu')
plt.xticks(rotation=45)
st.pyplot(fig2)

# 3. Doanh thu trung bình theo cửa hàng
st.subheader("3. Doanh Thu Trung Bình Theo Cửa Hàng (Store)")
avg_store_sales = df.groupby('Store')['Weekly_Sales'].mean().sort_values()

fig3, ax3 = plt.subplots(figsize=(8, 5))
avg_store_sales.plot(kind='barh', ax=ax3)
ax3.set_title('Doanh Thu Trung Bình Theo Store')
ax3.set_xlabel('Doanh Thu Trung Bình')
ax3.set_ylabel('Cửa Hàng')
st.pyplot(fig3)

# 4. Tỷ lệ doanh thu của Top 5 cửa hàng
st.subheader("4. Tỷ Lệ Doanh Thu của Top 5 Cửa Hàng")
city_sales = df.groupby('Store')['Weekly_Sales'].sum()
top_cities = city_sales.sort_values(ascending=False).head(5)

fig4, ax4 = plt.subplots(figsize=(8, 8))
top_cities.plot(kind='pie', autopct='%1.1f%%', startangle=140, ax=ax4)
ax4.set_ylabel('')
ax4.set_title('Top 5 Cửa Hàng có Doanh Thu Cao Nhất')
st.pyplot(fig4)

# 5. Phân phối doanh thu ngày lễ vs ngày thường
st.subheader("5. Phân Phối Doanh Thu: Ngày Lễ vs Ngày Thường")
df['Holiday_Flag'] = df['Holiday_Flag'].astype(bool)

fig5, ax5 = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df, x='Holiday_Flag', y='Weekly_Sales', ax=ax5)
ax5.set_title('Doanh Thu: Ngày Lễ vs Ngày Thường')
ax5.set_xlabel('Holiday (True/False)')
ax5.set_ylabel('Doanh Thu')
st.pyplot(fig5)

import matplotlib.pyplot as plt

# [Your existing code]
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

# Ensure your DataFrame 'df' is loaded and preprocessed before this point

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Extract features from date
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day

# Encode 'Holiday_Flag'
df['Holiday_Flag'] = df['Holiday_Flag'].astype(int)

# Drop missing values
df = df.dropna(subset=['Weekly_Sales', 'Date'])

# Prepare features and target
X = df[['Year', 'Month', 'Day', 'Holiday_Flag']]
y = df['Weekly_Sales']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on test data
y_pred = model.predict(X_test)

# Evaluate model
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
print("R-squared:", r2_score(y_test, y_pred))

# Plot Actual vs Predicted sales
plt.figure(figsize=(10, 5))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual Sales")
plt.ylabel("Predicted Sales")
plt.title("Actual vs Predicted Sales")
plt.grid(True)
plt.show()

st.subheader("6. Mô hình phân tích số lượng bán thực và dự đoán")

fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(y_test, y_pred, alpha=0.5)
ax.set_xlabel("Actual Sales")
ax.set_ylabel("Predicted Sales")
ax.set_title("Actual vs Predicted Sales")
ax.grid(True)

st.pyplot(fig)
