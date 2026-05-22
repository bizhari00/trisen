Tentu, ini adalah kode yang sudah dibersihkan. Semua logika yang berkaitan dengan Mode Kalibrasi, checkbox di navbar, sumbu/grid overlay, serta kotak hijau animasi (fig.add_shape & fig.add_scatter) telah dihapus.

Sekarang kodenya murni memuat gambar background SFDintro.png secara bersih dalam loop animasi (jika Anda masih membutuhkan transisi fase gambar murni), tanpa gangguan visual grid maupun komponen kalibrasi.

Python
import streamlit as st
import plotly.express as px
from PIL import Image
import time

# ==============================================================================
# 1. KONFIGURASI HALAMAN UTAMA (Wajib Paling Atas)
# ==============================================================================
st.set_page_config(
    page_title="Trisen Syntegra - Mode Live",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Pengaturan padding halaman utama agar aman di Forio 80%
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.0rem !important; 
        padding-bottom: 1.5rem !important;
        padding-left: 2.0rem !important;
        padding-right: 2.0rem !important;
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# 2. STRATEGI TURUNKAN LAYOUT 
# ==============================================================================
st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 3. NAVIGASI & JUDUL SEBARIS (Tanpa Checkbox Kalibrasi)
# ==============================================================================
col_btn, col_title = st.columns([1.2, 2.8])

with col_btn:
    st.link_button("🏠 ke Menu Simulasi", "https://forio.com/app/trisen_syntegra/trisen2", use_container_width=True)

with col_title:
    st.subheader("Tri-Sen Syntegra Technology")

st.divider()

# ==============================================================================
# 4. MEMUAT BACKGROUND IMAGE PKS
# ==============================================================================
try:
    img = Image.open("SFDintro.png") 
} except FileNotFoundError:
    st.error("File 'SFDintro.png' tidak ditemukan. Pastikan file gambar diagram Anda ada di root repository GitHub Anda dan namanya sesuai.")
    st.stop()

# ==============================================================================
# 5. RENDERING LOGIC (MODE NORMAL TANPA GRID & KALIBRASI)
# ==============================================================================
placeholder = st.empty()
render_count = 0

# Jumlah total fase (berdasarkan struktur data Anda sebelumnya ada 3 fase)
total_phases = 3 

while True:
    for phase_index in range(total_phases):
        fig = px.imshow(img)
        
        # Sembunyikan Grid Aksis secara total untuk estetika bersih
        fig.update_xaxes(visible=False, showgrid=False)
        fig.update_yaxes(visible=False, showgrid=False)
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=15, b=0), 
            height=550,
            autosize=True,
            showlegend=False
        )
        
        with placeholder.container():
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={
                    'displayModeBar': False, # Mematikan toolbar Plotly agar bersih
                    'responsive': True
                }, 
                key=f"pks_live_mode_{render_count}"
            )
        
        render_count += 1
        time.sleep(3.0)
