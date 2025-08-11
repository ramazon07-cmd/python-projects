import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import plotly.express as px

# Demo uchun soxta real vaqtli ma'lumot generatori
def generate_data(n=1000):
    now = datetime.now()
    timestamps = [now - timedelta(minutes=i) for i in range(n)][::-1]
    prices = np.cumsum(np.random.randn(n)) + 100
    volumes = np.random.randint(100, 1000, size=n)
    sensors = np.random.choice(['Sensor A', 'Sensor B', 'Sensor C'], size=n)
    return pd.DataFrame({
        'timestamp': timestamps,
        'price': prices,
        'volume': volumes,
        'sensor': sensors
    })

# Ma'lumotlarni olish
df = generate_data()

st.set_page_config(page_title="Real Vaqtli Ma'lumotlar Dashboard", layout="wide")
st.title("Real Vaqtli Ma'lumotlar Vizualizatsiyasi Dashboard")

# Filtrlar paneli
with st.sidebar:
    st.header("Filtrlar")
    sensor_options = df['sensor'].unique()
    selected_sensors = st.multiselect("Sensor(lar)ni tanlang", sensor_options, default=list(sensor_options))
    min_date = df['timestamp'].min()
    max_date = df['timestamp'].max()
    date_range = st.date_input("Vaqt oralig'ini tanlang", [min_date.date(), max_date.date()])
    export_btn = st.button("Ma'lumotlarni CSV ko'rinishida yuklab olish")

# Filtrlangan ma'lumotlar
filtered_df = df[
    (df['sensor'].isin(selected_sensors)) &
    (df['timestamp'].dt.date >= date_range[0]) &
    (df['timestamp'].dt.date <= date_range[1])
]

# Ma'lumotlarni eksport qilish
if export_btn:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="CSV faylni yuklab olish",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv'
    )

# Grafiklar
st.subheader("Narxlar dinamikasi")
fig = px.line(filtered_df, x='timestamp', y='price', color='sensor', title="Narxlar o'zgarishi")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Hajmlar bo'yicha taqsimot")
fig2 = px.bar(filtered_df, x='timestamp', y='volume', color='sensor', title="Hajmlar")
st.plotly_chart(fig2, use_container_width=True)

# Jadval va hisobot
st.subheader("Ma'lumotlar jadvali")
st.dataframe(filtered_df.tail(100), use_container_width=True)

st.subheader("Hisobot")
st.write(f"Umumiy yozuvlar soni: {len(filtered_df)}")
st.write(f"Narxning o'rtacha qiymati: {filtered_df['price'].mean():.2f}")
st.write(f"Umumiy hajm: {filtered_df['volume'].sum()}")