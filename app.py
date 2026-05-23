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
    /* 1. Mengatur Ukuran Kotak Tombol Agar Seimbang */
    .stLinkButton > a {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important; 
        padding: 8px 20px !important; 
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25) !important;
        transition: all 0.3s ease-in-out !important;
        text-decoration: none !important;
        
        display: inline-flex !important;
        width: auto !important;
        max-width: 320px !important; 
    }

    /* 2. Menyesuaikan Ukuran Font Tombol */
    .stLinkButton > a p {
        font-size: 16px !important; 
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
        margin-top: 8px; 
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col_btn, col_title = st.columns([1.2, 2.8])

with col_btn:
    st.link_button("🏠 Tri-Sen Technology Open Here", "https://forio.com/app/trisen_syntegra/trisen2", use_container_width=False)

with col_title:
    st.markdown('<p class="custom-title">Maintenance-Operational Cost Diagram</p>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 4. MEMUAT BACKGROUND IMAGE PKS
# ==============================================================================
try:
    img = Image.open("qcd1.png") 
except FileNotFoundError:
    st.error("File 'qcd1.png' tidak ditemukan. Pastikan file gambar diagram Anda ada di root repository GitHub Anda dan namanya sesuai.")
    st.stop()

# ==============================================================================
# 5. DATA KOORDINAT XY (Atas Kotak, Bawah Lingkaran/Circle/Kotak Lembut)
# ==============================================================================
process_phases = [
    # --- FASE 1: PARAMETER INPUT (ATAS) + KOTAK BAWAH ---
    [
        # Koordinat Asli Atas (Bentuk Kotak)
        {'label': '', 'shape_type': 'rect', 'is_bottom': False, 'tank_area': [152, 40, 268, 94]},
        {'label': '', 'shape_type': 'rect', 'is_bottom': False, 'tank_area': [74, 155, 203, 231]},
        {'label': '', 'shape_type': 'rect', 'is_bottom': False, 'tank_area': [720, 232, 851, 293]},
        {'label': '', 'shape_type': 'rect', 'is_bottom': False, 'tank_area': [872, 18, 996, 83]},
        # Kotak Bawah (Diberi penanda 'is_bottom': True agar warnanya lembut & tanpa garis)
        {'label': '', 'shape_type': 'rect', 'is_bottom': True, 'tank_area': [130, 429, 468, 688]} 
    ],
    
    # --- FASE 2: LAJU ALIRAN/FLOWS (ATAS) + KOTAK BAWAH ---
    [
        # Koordinat Asli Atas (Bentuk Kotak)
        {'label': '', 'shape_type': 'rect', 'is_bottom': False, 'tank_area': [271, 93, 428, 169]},
        {'label': '', 'shape_type': 'rect', 'is_bottom': False, 'tank_area': [779, 88, 925, 165]},
        # Kotak Bawah
        {'label': '', 'shape_type': 'rect', 'is_bottom': True, 'tank_area': [479, 435, 802, 683]} 
    ],
    
    # --- FASE 3: AKUMULASI STOK/STOCKS (ATAS) + KOTAK BAWAH ---
    [
        # Koordinat Asli Atas (Bentuk Kotak)
        {'label': '', 'shape_type': 'rect', 'is_bottom': False, 'tank_area': [465, 75, 606, 161]},
        {'label': '', 'shape_type': 'rect', 'is_bottom': False, 'tank_area': [621, 80, 751, 177]},
        # Kotak Bawah
        {'label': '', 'shape_type': 'rect', 'is_bottom': True, 'tank_area': [816, 429, 1181, 690]} 
    ]
]

# ==============================================================================
# 6. RENDERING LOGIC
# ==============================================================================
placeholder = st.empty()
render_count = 0

while True:
    for phase in process_phases:
        fig = px.imshow(img)
        
        # Sembunyikan Grid Aksis total agar diagram estetik dan bersih
        fig.update_xaxes(visible=False, showgrid=False)
        fig.update_yaxes(visible=False, showgrid=False)
        
        # Gambar ulang kotak animasi di tiap fase
        for component in phase:
            area = component['tank_area']
            shape = component.get('shape_type', 'rect')
            is_bottom = component.get('is_bottom', False)
            
            # PENGATURAN WARNA BARU DI SINI:
            if is_bottom:
                # Kotak bawah: tanpa garis tepi (width=0) & warna hijau pastel yang sangat lembut (alpha 0.15)
                border_color = "rgba(0,0,0,0)"
                border_width = 0
                fill_color = "rgba(144, 238, 144, 0.15)" 
            else:
                # Kotak atas tetap mempertahankan warna hijau asli Anda
                border_color = "LimeGreen" 
                border_width = 3
                fill_color = "rgba(0, 255, 0, 0.35)"
            
            # Menggambar Bentuk Sorotan Dinamis
            fig.add_shape(
                type=shape, 
                x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                fillcolor=fill_color,
                line=dict(color=border_color, width=border_width),
            )
            
            # Koordinat Label Dinamis
            text_x = (area[0] + area[2]) / 2
            text_y = area[3] + 20
            
            # Tempel Label Teks
            fig.add_scatter(
                x=[text_x], y=[text_y], 
                mode="text",
                text=[component['label']], 
                textposition="bottom center",
                textfont=dict(size=11, color="darkred", family="Arial Black")
            )
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=15, b=0), 
            height=720, 
            autosize=True,
            showlegend=False
        )
        
        with placeholder.container():
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={
                    'displayModeBar': False, 
                    'responsive': True
                }, 
                key=f"pks_live_mode_{render_count}"
            )
        
        render_count += 1
        time.sleep(3.0)
