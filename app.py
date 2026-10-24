import pandas as pd
import streamlit as st

# Setup Halaman Web
st.set_page_config(
    page_title="Pengecekan Data Anggota", page_icon="✅", layout="centered"
)

# Kustomisasi Tampilan Sederhana
st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("📌 Cek Status Keanggotaan")
st.caption(
    "Masukkan nama lengkap Anda untuk memeriksa status pendaftaran di"
    " database."
)
st.divider()

# Fitur Upload Excel Opsional (Bisa untuk Admin update data)
uploaded_file = st.sidebar.file_uploader(
    "Upload Database Excel Baru (Admin Only)", type=["xlsx", "xls"]
)

# Baca data dari upload admin ATAU dari file bawaan 'data_anggota.xlsx'
df = None
if uploaded_file is not None:
  df = pd.read_excel(uploaded_file)
else:
  try:
    df = pd.read_excel("data_anggota.xlsx")
  except Exception:
    df = None

# logika Pencarian
if df is not None:
  # Form Input Nama
  nama_input = st.text_input(
      "Nama Lengkap:", placeholder="Contoh: Budi Santoso"
  )

  if st.button("🔍 Cek Status Sekarang", type="primary"):
    if not nama_input.strip():
      st.warning("⚠️ Harap masukkan nama terlebih dahulu.")
    else:
      # Pencarian nama (mengabaikan huruf besar/kecil)
      # Memastikan kolom 'Nama' di Excel dicari dengan tepat
      hasil = df[
          df["Nama"].astype(str).str.contains(nama_input, case=False, na=False)
      ]

      if not hasil.empty:
        st.balloons()  # Efek animasi selebrasi
        st.success(
            "🎉 **TERDAFTAR!** Nama Anda ditemukan dalam sistem keanggotaan."
        )

        # Tampilkan detail data yang ditemukan
        st.subheader("Detail Data Anggota:")
        st.dataframe(hasil, use_container_width=True, hide_index=True)
      else:
        st.error(
            "❌ **BELUM TERDAFTAR.** Nama tersebut tidak ditemukan dalam"
            " database. Mohon cek kembali ejaan nama Anda."
        )
else:
  st.info(
      "ℹ️ Belum ada data. Silakan upload file Excel melalui menu sidebar di"
      " sebelah kiri."
  )