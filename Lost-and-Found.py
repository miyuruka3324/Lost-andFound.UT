import streamlit as st
import json
import os
import base64
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="UT Lost & Found",
    page_icon="🔍",
    layout="wide"
)

# --- FILE DATA PATH ---
DATA_FILE = "data_laporan.json"

# --- FUNGSI UTILITAS ---
def load_data():
    """Membaca data dari file JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    """Menyimpan data ke file JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def image_to_base64(uploaded_file):
    """Mengubah file upload menjadi base64 string untuk disimpan di JSON."""
    if uploaded_file is None:
        return None
    try:
        bytes_data = uploaded_file.getvalue()
        base64_str = base64.b64encode(bytes_data).decode()
        return f"data:image/png;base64,{base64_str}"
    except:
        return None

# --- CUSTOM CSS (Mengadopsi style.css asli) ---
st.markdown("""
    <style>
    :root {
        --biru-ut: #002147;
        --kuning-ut: #ffb800;
        --bg-light: #f8f9fa;
    }
    
    /* Warna Background Utama */
    .stApp {
        background-color: #f8f9fa;
        color: #333;
    }
    
    /* Styling Judul dan Header */
    h1, h2, h3 {
        color: #002147;
        font-family: "Poppins", sans-serif;
    }
    
    /* Styling Tombol Primary */
    .stButton > button {
        background-color: #002147;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #ffb800;
        color: #002147;
        border: 1px solid #002147;
    }

    /* Kartu Laporan Custom */
    .report-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid #ccc;
    }
    .status-hilang { border-left-color: #dc3545 !important; }
    .status-ditemukan { border-left-color: #28a745 !important; }
    
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & SIDEBAR ---
# Menampilkan Logo (Jika ada file logo-ut.png)
col_logo, col_title = st.sidebar.columns([1, 3])
try:
    with col_logo:
        st.image("logo-ut.png", width=60)
except:
    pass # Lanjut jika logo tidak ditemukan

with col_title:
    st.sidebar.title("UT LNF")

menu = st.sidebar.radio(
    "Navigasi", 
    ["Beranda", "Lihat Semua Laporan", "Laporkan Barang", "Kontak"]
)

# --- HALAMAN: BERANDA ---
if menu == "Beranda":
    # Hero Section
    st.markdown("""
    <div style="background: linear-gradient(to right, #002147, #003d80); padding: 60px 20px; text-align: center; color: white; border-radius: 10px;">
        <h2 style="color: black;">UT Lost & Found</h2>
        <p>Situs resmi untuk melaporkan dan mencari barang hilang di lingkungan kampus Universitas Terbuka.</p>
        <h3 style="color: #ffb800; font-size: 18px; margin-top:20px;">Kehilangan Barang? Atau Menemukan Milik Seseorang?</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Spacer

    col1, col2 = st.columns(2)
    with col1:
        st.info("**Visi:** Menjadi platform digital terpercaya yang memfasilitasi pelaporan dan pencarian barang hilang di lingkungan UT.")
    with col2:
        st.success("""
        **Misi:**
        * Membangun sistem pelaporan yang mudah diakses.
        * Meningkatkan kepedulian sosial warga kampus.
        * Menjaga kepercayaan dan transparansi.
        """)

    st.markdown("### Tentang Kami")
    st.write("""
    UT Lost & Found adalah inisiatif mahasiswa Universitas Terbuka untuk saling membantu menemukan kembali barang-barang yang tercecer.
    Kami percaya kejujuran adalah kunci keamanan kampus.
    """)

# --- HALAMAN: LAPORKAN BARANG ---
elif menu == "Laporkan Barang":
    st.title("📝 Laporkan Barang")
    st.markdown("Isi formulir di bawah ini untuk melaporkan barang hilang atau ditemukan.")

    with st.form("form_laporan", clear_on_submit=True):
        nama = st.text_input("Nama Pelapor", placeholder="Masukkan nama lengkap...")
        jenis = st.selectbox("Jenis Laporan", ["Barang Hilang", "Barang Ditemukan"])
        barang = st.text_input("Nama Barang", placeholder="Contoh: Dompet, KTP, Helm...")
        lokasi = st.text_input("Lokasi Kejadian", placeholder="Lokasi ditemukan / hilang...")
        deskripsi = st.text_area("Deskripsi", placeholder="Ciri-ciri barang, warna, kondisi, dll...")
        foto = st.file_uploader("Upload Foto Barang (Opsional)", type=['png', 'jpg', 'jpeg'])
        
        submitted = st.form_submit_button("Kirim Laporan")
        
        if submitted:
            if not nama or not barang or not lokasi or not deskripsi:
                st.error("Mohon lengkapi semua field yang wajib diisi!")
            else:
                # Proses Simpan Data
                existing_data = load_data()
                
                foto_base64 = image_to_base64(foto)
                jenis_key = "hilang" if jenis == "Barang Hilang" else "ditemukan"
                
                new_report = {
                    "id": len(existing_data) + 1,
                    "nama": nama,
                    "jenis": jenis_key,
                    "barang": barang,
                    "lokasi": lokasi,
                    "deskripsi": deskripsi,
                    "foto": foto_base64,
                    "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                existing_data.append(new_report)
                save_data(existing_data)
                
                st.success("Laporan berhasil disimpan! Terima kasih atas partisipasi Anda.")

# --- HALAMAN: LIHAT SEMUA LAPORAN ---
elif menu == "Lihat Semua Laporan":
    st.title("📋 Daftar Laporan")
    
    data = load_data()
    
    if not data:
        st.info("Belum ada laporan yang tercatat saat ini.")
    else:
        # Filter opsi (Opsional fitur tambahan)
        filter_status = st.selectbox("Filter Status:", ["Semua", "Hilang", "Ditemukan"])
        
        # Tampilkan data (Reverse agar yang terbaru di atas)
        for item in reversed(data):
            # Logika Filter
            if filter_status == "Hilang" and item['jenis'] != 'hilang': continue
            if filter_status == "Ditemukan" and item['jenis'] != 'ditemukan': continue
            
            # Tentukan Warna Status
            status_text = "Barang HILANG" if item['jenis'] == 'hilang' else "Barang DITEMUKAN"
            status_color = "red" if item['jenis'] == 'hilang' else "green"
            css_class = "status-hilang" if item['jenis'] == 'hilang' else "status-ditemukan"
            
            # Layout Kartu
            with st.container():
                st.markdown(f"""
                <div class="report-card {css_class}">
                    <h3 style="margin-bottom:0;">{item['barang']}</h3>
                    <p style="color: {status_color}; font-weight: bold; margin-bottom: 5px;">{status_text}</p>
                    <p><strong>📍 Lokasi:</strong> {item['lokasi']}</p>
                    <p><strong>📝 Deskripsi:</strong> {item['deskripsi']}</p>
                    <p style="font-size: 0.8em; color: gray;">Dilaporkan oleh {item['nama']} pada {item['waktu']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Menampilkan Gambar jika ada
                if item['foto']:
                    st.image(item['foto'], width=200)
                
                st.write("---") # Garis pemisah antar item

# --- HALAMAN: KONTAK ---
elif menu == "Kontak":
    st.title("📞 Hubungi Kami")
    st.write("Jika Anda memiliki pertanyaan, saran, atau laporan khusus, silakan hubungi tim kami.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Alamat:** Jl. Cabe Raya, Pondok Cabe, Tangerang Selatan
        
        **Jam Operasional:** Senin - Jumat, 08.00 - 16.00 WIB
        """)
    
    with col2:
        st.markdown("""
        **Email:** lostfound@ecampus.ut.ac.id
        
        **Telepon:** (021) 1234-5678
        """)

# --- FOOTER ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; font-size: 14px; color: #666;">
        &copy; 2025 Universitas Terbuka | Sistem Lost & Found
    </div>

""", unsafe_allow_html=True)
