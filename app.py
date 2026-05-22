import streamlit as st
import plotly.express as px
from PIL import Image
import time

# ==============================================================================
# 1. KONFIGURASI HALAMAN UTAMA (Wajib Paling Atas)
# ==============================================================================
st.set_page_config(
    page_title="Pabrik PKS - Mode Live",
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
# 3. NAVIGASI & JUDUL SEBARIS
# ==============================================================================
col_btn, col_title, col_calib = st.columns([1.2, 1.8, 1.0])

with col_btn:
    st.link_button("🏠 ke Menu Simulasi", "https://forio.com/app/trisen_syntegra/trisen", use_container_width=True)

with col_title:
    st.subheader("Tri-Sen Syntegra Technology")

with col_calib:
    # FITUR BARU: Sakelar Mode Kalibrasi Grid
    is_calibration_mode = st.checkbox("📐 Mode Kalibrasi (Grid ON)", value=False, help="Aktifkan untuk melihat koordinat X/Y murni dan menghentikan loop animasi.")

st.divider()

# ==============================================================================
# 4. MEMUAT BACKGROUND IMAGE PKS
# ==============================================================================
try:
    img = Image.open("SFDintro.png") 
except FileNotFoundError:
    st.error("File 'diagram.png' tidak ditemukan. Pastikan file gambar diagram Anda ada di root repository GitHub Anda dan namanya sesuai.")
    st.stop()

# ==============================================================================
# 5. DATA KOORDINAT XY MURNI (Hasil Kalibrasi Pas)
#    Format tank_area: [X_Mulai, Y_Mulai, X_Akhir, Y_Akhir]
# ==============================================================================
process_phases = [
    # --- FASE 1: PARAMETER INPUT & INTERVENSI HULU ---
    [
        {'label': 'Frequency Gangguan', 'tank_area': [100, 100, 200, 150]},
        {'label': 'Efektif Desain', 'tank_area': [100, 200, 200, 250]},
        {'label': 'Biaya Rugi Downtime', 'tank_area': [300, 100, 400, 150]},
        {'label': 'Biaya Maintenance', 'tank_area': [300, 200, 400, 250]}
    ],
    
    # --- FASE 2: LAJU ALIRAN SISTEM (FLOWS) ---
    [
        {'label': 'Laju Terjadi Trip', 'tank_area': [500, 100, 600, 150]},
        {'label': 'Aliran Biaya Operasional', 'tank_area': [500, 200, 600, 250]}
    ],
    
    # --- FASE 3: AKUMULASI STOK UTAMA (STOCKS) ---
    [
        {'label': 'Kumulatif Trip', 'tank_area': [700, 100, 800, 150]},
        {'label': 'Total Cost Ownership', 'tank_area': [700, 200, 800, 250]}
    ]
]

# ==============================================================================
# 6. RENDERING LOGIC (ANIMASI LIVE vs MODE KALIBRASI)
# ==============================================================================
placeholder = st.empty()

if is_calibration_mode:
    # --------------------------------------------------------------------------
    # MODE KALIBRASI: Tampilkan Semua Kotak Sekaligus + Grid Aktif
    # --------------------------------------------------------------------------
    fig = px.imshow(img)
    
    # Munculkan Sumbu Aksis dan Grid Garis untuk Mapping Manual
    fig.update_xaxes(visible=True, showgrid=True, gridcolor="rgba(255, 255, 255, 0.3)", ticks="outside")
    fig.update_yaxes(visible=True, showgrid=True, gridcolor="rgba(255, 255, 255, 0.3)", ticks="outside")
    
    # Render seluruh komponen dari semua fase sekaligus agar bisa dicocokkan posisinya
    for phase in process_phases:
        for component in phase:
            area = component['tank_area']
            
            # Gambar Kotak Panduan Pengarah
            fig.add_shape(
                type="rect", 
                x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                fillcolor="rgba(255, 165, 0, 0.2)", # Warna oranye transparan saat kalibrasi
                line=dict(color="Orange", width=2, dash="dash"),
            )
            
            text_x = (area[0] + area[2]) / 2
            text_y = area[3] + 20
            
            fig.add_scatter(
                x=[text_x], y=[text_y], 
                mode="text",
                text=[component['label']], 
                textposition="bottom center",
                textfont=dict(size=10, color="orange", family="Arial Black")
            )
            
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10), 
        height=650, # Sedikit lebih tinggi agar sumbu koordinat bawah kelihatan jelas
        autosize=True,
        showlegend=False
    )
    
    with placeholder.container():
        st.info("💡 **Mode Kalibrasi Aktif**: Arahkan kursor (*hover*) pada sudut diagram untuk melihat koordinat asli $X$ dan $Y$. Salin nilai tersebut ke dalam variabel `process_phases` di kode script Anda.")
        st.plotly_chart(
            fig, 
            use_container_width=True, 
            config={
                'displayModeBar': True, # Mengaktifkan toolbar zoom/pan bawaan Plotly
                'scrollZoom': True,
                'responsive': True
            },
            key="pks_calibration_grid"
        )

else:
    # --------------------------------------------------------------------------
    # MODE NORMAL: Loop Animasi Berjalan Bergantian Sesuai Urutan Fase
    # --------------------------------------------------------------------------
    render_count = 0
    while True:
        for phase in process_phases:
            fig = px.imshow(img)
            
            # Sembunyikan Grid Aksis untuk Estetika Live Dashboard
            fig.update_xaxes(visible=False, showgrid=False)
            fig.update_yaxes(visible=False, showgrid=False)
            
            for component in phase:
                area = component['tank_area']
                
                # 1. Menggambar Kotak Sorotan Hijau
                fig.add_shape(
                    type="rect", 
                    x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                    fillcolor="rgba(0, 255, 0, 0.35)",
                    line=dict(color="LimeGreen", width=3),
                )
                
                # 2. Koordinat Label Dinamis
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
                        'displayModeBar': False, 
                        'responsive': True
                    }, 
                    key=f"pks_live_mode_{render_count}"
                )
            
            render_count += 1
            time.sleep(3.0)
