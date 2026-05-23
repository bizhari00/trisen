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
# 3. NAVIGASI & JUDUL SEBARIS (Balanced Design Button & Title)
# ==============================================================================
st.markdown(
    """
    <style>
    /* 1. Mengatur Ukuran Kotak Tombol Agar Seimbang (Tidak Terlalu Besar) */
    .stLinkButton > a {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important; /* Lengkungan sedikit dikurangi agar lebih formal */
        padding: 8px 20px !important; /* Padding vertikal dikurangi agar kotak lebih tipis */
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25) !important;
        transition: all 0.3s ease-in-out !important;
        text-decoration: none !important;
        
        /* KUNCI KESEIMBANGAN: Batasi lebar maksimal tombol */
        display: inline-flex !important;
        width: auto !important;
        max-width: 320px !important; 
    }

    /* 2. Menyesuaikan Ukuran Font Tombol */
    .stLinkButton > a p {
        font-size: 16px !important; /* Ukuran diturunkan ke 16px agar proporsional */
        font-weight: bold !important;
        color: #FFFFFF !important;
        letter-spacing: 0.5px !important;
    }

    /* 3. Efek Hover */
    .stLinkButton > a:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* 4. Mengatur Teks Judul Diagram Agar Selaras */
    .custom-title {
        font-size: 20px !important; 
        font-weight: 500 !important;
        color: #1E293B;
        margin-top: 8px; /* Disesuaikan agar sejajar lurus vertikal dengan tombol baru */
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Menggunakan kembali rasio kolom asli agar pembagian ruangnya pas
col_btn, col_title = st.columns([1.2, 2.8])

with col_btn:
    # use_container_width diubah ke False agar lebarnya mengikuti aturan CSS max-width di atas
    st.link_button("🏠 Tri-Sen Technology Open Here", "https://forio.com/app/trisen_syntegra/trisen2", use_container_width=False)

with col_title:
    st.markdown('<p class="custom-title">Maintenance-Operational Cost Diagram</p>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 4. MEMUAT BACKGROUND IMAGE PKS
# ==============================================================================
try:
    img = Image.open("SFDintro.png") 
except FileNotFoundError:
    st.error("File 'SFDintro.png' tidak ditemukan. Pastikan file gambar diagram Anda ada di root repository GitHub Anda dan namanya sesuai.")
    st.stop()

# ==============================================================================
# 5. DATA KOORDINAT XY (Untuk Animasi Sorotan Hijau)
# ==============================================================================
process_phases = [
    # --- FASE 1: PARAMETER INPUT & INTERVENSI HULU ---
    [
        {'label': '', 'tank_area': [152, 40, 268, 94]},
        {'label': '', 'tank_area': [74, 155, 203, 231]},
        {'label': '', 'tank_area': [720, 232, 851, 293]},
        {'label': '', 'tank_area': [872, 18, 996, 83]}
    ],
    
    # --- FASE 2: LAJU ALIRAN SISTEM (FLOWS) ---
    [
        {'label': '', 'tank_area': [271, 93, 428, 169]},
        {'label': '', 'tank_area': [779, 88, 925, 165]}
    ],
    
    # --- FASE 3: AKUMULASI STOK UTAMA (STOCKS) ---
    [
        {'label': '', 'tank_area': [465, 75, 606, 161]},
        {'label': '', 'tank_area': [621, 80, 751, 177]}
    ]
]

# ==============================================================================
# 6. RENDERING LOGIC (MODE NORMAL + ANIMASI TANPA GRID)
# ==============================================================================
placeholder = st.empty()
render_count = 0

while True:
    for phase in process_phases:
        fig = px.imshow(img)
        
        # Sembunyikan Grid Aksis total agar diagram estetik dan bersih
        fig.update_xaxes(visible=False, showgrid=False)
        fig.update_yaxes(visible=False, showgrid=False)
        
        # Gambar ulang kotak animasi hijau di tiap fase
        for component in phase:
            area = component['tank_area']
            
            # 1. Menggambar Kotak Sorotan Hijau
            fig.add_shape(
                type="rect", 
                x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                fillcolor="rgba(0, 255, 0, 0.35)",
                line=dict(color="LimeGreen", width=3),
            )
            
            # 2. Koordinat Label Dinamis (Jika nanti ingin diberi teks label)
            text_x = (area[0] + area[2]) / 2
            text_y = area[3] + 20
            
            # 3. Tempel Label Teks
            fig.add_scatter(
                x=[text_x], y=[text_y], 
                mode="text",
                text=[component['label']], 
                textposition="bottom center",
                textfont=dict(size=11, color="darkred", family="Arial Black")
            )
        
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
                    'displayModeBar': False, # Toolbar atas plotly dimatikan agar bersih
                    'responsive': True
                }, 
                key=f"pks_live_mode_{render_count}"
            )
        
        render_count += 1
        time.sleep(3.0)
