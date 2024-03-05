
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# set title
st.title("Dashboard Rental Sepeda")

# set keterangan
st.write("Nama: Huffaz Muhammad Abdurrofi Baith")
st.write("email: huffazbaith@gmail.com")
st.write("ID Dicoding: Huffaz Muhammad Abdurrofi Baith")

# Pertanyaan bisnis
st.header("Pertanyaan Bisnis")
st.write("- Pertanyaan 1: Bagaimana pola penyewaan sepeda berubah di setiap musim? Apakah ada perbedaan signifikan antara musim semi, panas, gugur, dan musim dingin?")
st.write("- Pertanyaan 2: Bagaimana cuaca mempengaruhi jumlah penyewaan sepeda?")
st.write("- Pertanyaan 3: Apa pola penyewaan sepeda harian dan bagaimana distribusi penyewaan pada jam-jam tertentu dalam sehari?")

with st.expander("Penjelasan mengenai dataset"):
    st.write(
        """Dataset ini merupakan kumpulan data yang berkaitan dengan proses penyewaan sepeda yang sangat terkait dengan lingkungan dan pengaturan musiman. Faktor-faktor seperti kondisi cuaca, presipitasi, hari dalam seminggu, musim, jam dalam sehari, dll. dapat memengaruhi perilaku penyewaan. Data inti dalam dataset ini terkait dengan catatan sejarah dua tahun yang sesuai dengan tahun 2011 dan 2012 dari sistem Capital Bikeshare di Washington D.C., Amerika Serikat, yang tersedia secara publik di http://capitalbikeshare.com/system-data. Data ini dibuat dalam interval dua jam dan harian, kemudian diekstraksi dan ditambahkan informasi cuaca dan musiman yang sesuai. Informasi cuaca diambil dari http://www.freemeteo.com.
        """
    )
with st.expander("Karakteristik Dataset"):
    st.write(
        """
Kedua dataset hour.csv dan day.csv memiliki atribut-atribut berikut, kecuali hr yang tidak tersedia dalam day.csv:
- instant: indeks catatan
- dteday: tanggal
- season: musim (1: musim semi, 2: musim panas, 3: musim gugur, 4: musim dingin)
- yr: tahun (0: 2011, 1: 2012)
- mnth: bulan (1 hingga 12)
- hr: jam (0 hingga 23) [tidak ada dalam day.csv]
- holiday: menunjukkan apakah hari tersebut merupakan hari libur atau tidak (diambil dari http://dchr.dc.gov/page/holiday-schedule)
- weekday: hari dalam seminggu
- workingday: 1 jika hari itu bukan akhir pekan atau hari libur, sebaliknya 0
- weathersit:
        1: Cerah, Sedikit awan, Sebagian berawan, Sebagian berawan
        2: Kabut + Berawan, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut
        3: Salju ringan, Hujan ringan + Petir + Awan bertebaran, Hujan ringan + Awan bertebaran
        4: Hujan lebat + Pecahan Es + Petir + Kabut, Salju + Kabut
- temp: Suhu terstandar dalam Celsius. Nilainya dibagi oleh 41 (maksimum)
- atemp: Suhu terasa terstandar dalam Celsius. Nilainya dibagi oleh 50 (maksimum)
- hum: Kelembaban terstandar. Nilainya dibagi oleh 100 (maksimum)
- windspeed: Kecepatan angin terstandar. Nilainya dibagi oleh 67 (maksimum)
- casual: jumlah pengguna sewa kasual
- registered: jumlah pengguna terdaftar
- cnt: jumlah total sepeda yang disewa, termasuk pengguna kasual dan terdaftar
        """
    )

st.write("Dataset berikut merupakan dataset yang sudah di-update sesuai kebutuhannya")
#read dataset
df_day = pd.read_csv("day_updated.csv", index_col=None)
df_hour = pd.read_csv("hour_updated.csv", index_col=None)

st.subheader("Dataset Rental Sepeda Harian")
st.dataframe(df_day)
st.subheader("Dataset Rental Per Jam")
st.dataframe(df_hour)

st.subheader("Bar Plot Jumlah Penyewa Sepeda berdasarkan musimnya")
# Tinjauan berdasarkan penyewa terdaftar dan penyewa kasual
penyewa_musim = df_day.groupby('season')[['registered', 'casual']].sum().reset_index()

# Membuat bar plot
fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(penyewa_musim['season'], penyewa_musim['registered'], label='Terdaftar')
ax.bar(penyewa_musim['season'], penyewa_musim['casual'], label='Kasual', bottom=penyewa_musim['registered'])

ax.set_title('Jumlah penyewaan sepeda berdasarkan musim')
ax.legend()

# Menampilkan plot di Streamlit
st.pyplot(fig)
st.write("Dari hasil analisis dengan menggunakan barplot, dapat disimpulkan bahwa musim yang paling disukai oleh pengguna sepeda (baik Casual maupun Registered) adalah musim gugur (Fall), diikuti oleh musim panas (Summer), musim dingin (Winter), dan musim semi (Spring) berada pada urutan terakhir. Hal ini juga senada dengan jumlah penyewa kasual dan penyewa terdaftar.")

st.subheader("Bar Plot Penyewa Sepeda berdasarkan Cuaca Harian")
# Tinjauan berdasarkan penyewa terdaftar dan penyewa kasual
penyewa_cuaca_day = df_day.groupby('weathersit')[['registered', 'casual']].sum().reset_index()

# Membuat bar plot
fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(penyewa_cuaca_day['weathersit'], penyewa_cuaca_day['registered'], label='Terdaftar')
ax.bar(penyewa_cuaca_day['weathersit'], penyewa_cuaca_day['casual'], label='Kasual', bottom=penyewa_cuaca_day['registered'])

ax.set_title('Jumlah penyewaan sepeda berdasarkan cuaca')
ax.legend()

# Menampilkan plot di Streamlit
st.pyplot(fig)
st.write("Dari hasil analisis dengan menggunakan barplot, dapat disimpulkan bahwa mpenyewa sepeda terbanyak ada pada cuaca cerah/sedikit berawan, sedangkan penyewa sepeda paling sedikit ada pada saat cuaca sedikit bersalju/hujan. Adapun secara jumlah, penyewa terdaftar lebih banyak dibanding penyewa kasual pada semua cuaca.")

st.subheader("Plot Tren Rental Sepeda per Jam")
# Menghitung rata-rata penyewa per jam
penyewa_hour = df_hour.groupby('hr')[["cnt"]].mean().reset_index()

# Membuat plot
fig, ax = plt.subplots(figsize=(17, 7))
ax.plot(penyewa_hour['hr'], penyewa_hour['cnt'], linestyle='-', marker='o')

# Menyesuaikan tata letak plot
ax.set_title("Tren Rerata Penyewa Sepeda per Jam", fontsize=17)
ax.set_xticks(penyewa_hour['hr'])
ax.set_xlabel("Waktu (24 jam)", fontsize=13)
ax.set_ylabel("Rata-rata Penyewa Sepeda", fontsize=14)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

# Menampilkan plot di Streamlit
st.pyplot(fig)
st.write("Dari hasil analisis line chart, pukul 7-8 dan pukul 17-18 memiliki rerata penyewa sepeda tertinggi. Ini mungkin mencerminkan waktu-waktu puncak di mana orang lebih cenderung menyewa sepeda, seperti pagi hari untuk bepergian ke tempat kerja atau sore hari setelah jam kerja.Sedangkan pada pukul 4-5 memiliki rerata penyewa sepeda terendah. Ini bisa mencerminkan kurangnya minat atau kebutuhan untuk menyewa sepeda pada pagi hari.")

st.header("Conclusion")
st.write("- Conclusion Pertanyaan 1: Dari hasil analisis dengan menggunakan barplot, dapat disimpulkan bahwa musim yang paling disukai oleh pengguna sepeda (baik Casual maupun Registered) adalah musim gugur (Fall), diikuti oleh musim panas (Summer), musim dingin (Winter), dan musim semi (Spring) berada pada urutan terakhir. Hal ini juga senada dengan jumlah penyewa kasual dan penyewa terdaftar.")
st.write("- Conclusion Pertanyaan 2: Dari hasil analisis dengan menggunakan barplot, dapat disimpulkan bahwa mpenyewa sepeda terbanyak ada pada cuaca cerah/sedikit berawan, sedangkan penyewa sepeda paling sedikit ada pada saat cuaca sedikit bersalju/hujan. Adapun secara jumlah, penyewa terdaftar lebih banyak dibanding penyewa kasual pada semua cuaca.")
st.write("- Conclusion Pertanyaan 3: Dari hasil analisis line chart, pukul 7-8 dan pukul 17-18 memiliki rerata penyewa sepeda tertinggi. Ini mungkin mencerminkan waktu-waktu puncak di mana orang lebih cenderung menyewa sepeda, seperti pagi hari untuk bepergian ke tempat kerja atau sore hari setelah jam kerja.Sedangkan pada pukul 4-5 memiliki rerata penyewa sepeda terendah. Ini bisa mencerminkan kurangnya minat atau kebutuhan untuk menyewa sepeda pada pagi hari.")

st.caption('Copyright (c) 2024')
