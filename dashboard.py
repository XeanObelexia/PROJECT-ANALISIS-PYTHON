import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Judul Dashboard
st.title("Dashboard Analisis Peminjaman Sepeda")

# Path folder tempat menyimpan file
folder_path = os.path.dirname(__file__)

# Nama file yang akan dibaca
file_day = os.path.join(folder_path, "processed_day.csv")
file_hour = os.path.join(folder_path, "processed_hour.csv")

if os.path.exists(file_day) and os.path.exists(file_hour):
    # Membaca dataset hasil permodelan
    day_df = pd.read_csv(file_day)
    hour_df = pd.read_csv(file_hour)

    # Sidebar untuk memilih analisis
    st.sidebar.header("Pilih Analisis")
    view = st.sidebar.selectbox(
        "Pilih Analisis", 
        ["Overview", "Pengaruh Musim", "Tren Peminjaman Sepeda Berdasarkan Bulan", "Tren Penggunaan Sepeda Berdasarkan Jam"]
    )

    # Tampilkan Data Overview
    if view == "Overview":
        st.subheader("Tinjauan Data")
        st.write("Dataset Harian:")
        st.dataframe(day_df.head())
        st.write("Dataset Per Jam:")
        st.dataframe(hour_df.head())
        st.write("Statistik Deskriptif:")
        st.dataframe(day_df.describe())

    # Analisis Pengaruh Musim terhadap Peminjaman Sepeda
    elif view == "Pengaruh Musim":
        st.subheader("Pengaruh Musim terhadap Peminjaman Sepeda")
        fig, ax = plt.subplots(figsize=(8,5))
        sns.boxplot(x='season', y='cnt', data=day_df, ax=ax)
        ax.set_xlabel('Musim')
        ax.set_ylabel('Total Peminjaman')
        ax.set_title('Distribusi Peminjaman Sepeda berdasarkan Musim')
        st.pyplot(fig)
        st.write("Insight: Peminjaman sepeda bervariasi berdasarkan musim, dengan peningkatan pada musim panas dan penurunan di musim dingin.")

    # Analisis Tren Peminjaman Sepeda Berdasarkan Bulan
    elif view == "Tren Peminjaman Sepeda Berdasarkan Bulan":
        st.subheader("Tren Peminjaman Sepeda Berdasarkan Bulan dalam Setahun")
        fig, ax = plt.subplots(figsize=(12,6))
        sns.lineplot(x='mnth', y='cnt', data=day_df, estimator='mean', ax=ax)
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Rata-rata Peminjaman Sepeda')
        ax.set_title('Tren Peminjaman Sepeda Berdasarkan Bulan dalam Setahun')
        st.pyplot(fig)
        st.write("Insight: Peminjaman sepeda mengalami kenaikan pada bulan-bulan tertentu, kemungkinan karena faktor cuaca atau aktivitas musiman.")

    # Analisis Tren Penggunaan Sepeda Berdasarkan Jam
    elif view == "Tren Penggunaan Sepeda Berdasarkan Jam":
        st.subheader("Tren Penggunaan Sepeda Berdasarkan Jam dalam Sehari")
        st.write("Kolom yang tersedia dalam hour_df:", day_df.columns.tolist())
        
        if 'hr' in day_df.columns:
            fig, ax = plt.subplots(figsize=(12,6))
            sns.lineplot(x='hr', y='cnt', data=day_df, estimator='mean', ax=ax)
            ax.set_xlabel('Jam dalam Sehari')
            ax.set_ylabel('Rata-rata Peminjaman Sepeda')
            ax.set_title('Tren Penggunaan Sepeda Berdasarkan Jam dalam Sehari')
            st.pyplot(fig)
            st.write("Insight: Peminjaman sepeda meningkat pada jam-jam sibuk seperti pagi (jam berangkat kerja) dan sore (jam pulang kerja).")
        else:
            st.error("Kolom 'hr' tidak ditemukan dalam dataset. Periksa kembali file processed_hour.csv.")

    # Kesimpulan
    st.subheader("Kesimpulan")
    st.write("1. Musim berpengaruh terhadap jumlah peminjaman sepeda, dengan musim tertentu memiliki tren lebih tinggi.")
    st.write("2. Peminjaman sepeda menunjukkan pola musiman, dengan kenaikan pada bulan-bulan tertentu.")
    st.write("3. Tren penggunaan sepeda lebih tinggi pada jam-jam sibuk dalam sehari.")
else:
    st.error("File data tidak ditemukan. Pastikan file 'processed_day.csv' dan 'processed_hour.csv' ada dalam folder yang benar.")
