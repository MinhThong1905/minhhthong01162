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
st.subheader("1. Tổng Doanh Thu mỗi 3 Tháng")
df['Quarter3M'] = df['Date'].dt.year.astype(str) + '-Q' + ((df['Date'].dt.month - 1) // 3 + 1).astype(str)
quarterly_sales = df.groupby('Quarter3M')['Weekly_Sales'].sum().reset_index()

fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(quarterly_sales['Quarter3M'], quarterly_sales['Weekly_Sales'], color='lightgreen')
ax1.set_title('Tổng Doanh Thu mỗi 3 Tháng')
ax1.set_xlabel('Quarter')
ax1.set_ylabel('Tổng Doanh Thu')
plt.xticks(rotation=45)
st.pyplot(fig1)

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
