import streamlit as st
import plotly.express as px
from PIL import Image
import time

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="PFAD Produksi Biodiesel",
    layout="wide",
    initial_sidebar_state="collapsed"
)

URL_PORTAL_FORIO = "https://forio.com/app/univ_sumaterautara/research-ptpn"
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
    h1 {
        text-align: center;
        font-family: 'Arial', sans-serif;
        margin-bottom: 20px;
    }
    .custom-tab-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: #ffffff;
        color: #31333F;
        border: 1px solid rgba(49, 51, 63, 0.2);
        padding: 0.4rem 1rem;
        border-radius: 0.5rem;
        font-weight: 500;
        font-size: 1.6rem;
        text-decoration: none;
        cursor: pointer;
        transition: background-color 0.16s ease-in-out;
        width: 100%;
        height: 42px;
    }
    .custom-tab-btn:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
        background-color: rgba(255, 75, 75, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

col_nav, _ = st.columns([2, 5])
with col_nav:
    st.markdown(
        f'<a href="{URL_PORTAL_FORIO}" target="_blank" class="custom-tab-btn">🏠 Kembali ke Menu Utama</a>', 
        unsafe_allow_html=True
    )

st.markdown("<h1>PFAD Biodiesel</h1>", unsafe_allow_html=True)

# ==========================================
# 2. MEMUAT BACKGROUND IMAGE
# ==========================================
try:
    img = Image.open("rivaldi.png")
except FileNotFoundError:
    st.error("File 'rivaldi.png' tidak ditemukan. Pastikan file gambar ada di root repository GitHub Anda.")
    st.stop()

# ==========================================
# 3. KORDINAT AKURAT BERDASARKAN GRID ASLI (x0, y0, x1, y1)
# ==========================================
KOTAK_METANOL = [40, 80, 100, 210]
KOTAK_H2SO4   = [40, 240, 100, 370]
KOTAK_NAOH    = [370, 40, 420, 140]

y_arrow = 550 

flow_path = [
    {
        'step_id': 'feedstock_prep',
        'x': 90, 'y': y_arrow, 'label': 'Persiapan Bahan Awal',
        'multiple_areas': [
            KOTAK_METANOL,
            KOTAK_H2SO4,
            [40, 400, 100, 520]
        ]
    },
    {
        'step_id': 'reaktor1',
        'x': 320, 'y': y_arrow, 'label': 'Reaktor 1 Aktif (Esterifikasi)', 
        'tank_area': [295, 400, 360, 510]
    },
    {
        'step_id': 'separator1',
        'x': 420, 'y': y_arrow, 'label': 'Separator 1 Aktif', 
        'tank_area': [430, 400, 500, 500]
    },
    {
        'step_id': 'reaktor2',
        'x': 630, 'y': y_arrow, 'label': 'Reaktor 2 Aktif (TransEsterifikasi)', 
        'tank_area': [600, 400, 660, 500]
    },
    {
        'step_id': 'separator2',
        'x': 745, 'y': y_arrow, 'label': 'Separator 2 Aktif', 
        'tank_area': [770, 410, 820, 500]
    },
    {
        'step_id': 'washdrum',
        'x': 920, 'y': y_arrow, 'label': 'Wash Drum Aktif', 
        'tank_area': [890, 400, 950, 500]
    },
    {
        'step_id': 'evaporator',
        'x': 1025, 'y': y_arrow, 'label': 'Evaporator Aktif', 
        'tank_area': [980, 410, 1050, 500]
    },
    {
        'step_id': 'biodiesel',
        'x': 1200, 'y': y_arrow, 'label': 'Produk Biodiesel', 
        'tank_area': [1150, 400, 1250, 530]
    }
]

# ==========================================
# 4. LOGIKA ANIMASI JALUR PROSES DENGAN KOTAK PRESISI
# ==========================================
placeholder = st.empty()
render_count = 0

while True:
    for step in range(len(flow_path)):
        current = flow_path[step]
        fig = px.imshow(img)
        
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        
        # 1. LOGIKA PEWARNAAN KOTAK HIJAU TRANSPARAN
        if 'multiple_areas' in current:
            for area in current['multiple_areas']:
                fig.add_shape(
                    type="rect", x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                    fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2),
                )
        else:
            area = current['tank_area']
            fig.add_shape(
                type="rect", x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2),
            )
            
        # 2. LOGIKA KONDISIONAL TANGKI PROSES ATAS
        if current['step_id'] == 'reaktor1':
            for area in [KOTAK_METANOL, KOTAK_H2SO4]:
                fig.add_shape(
                    type="rect", x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                    fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2)
                )
        elif current['step_id'] == 'reaktor2':
            fig.add_shape(
                type="rect", x0=KOTAK_NAOH[0], y0=KOTAK_NAOH[1], x1=KOTAK_NAOH[2], y1=KOTAK_NAOH[3],
                fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2)
            )

        # 3. PENANDA PANAH SEGITIGA KUNING ANIMASI
        fig.add_scatter(
            x=[current['x']], y=[current['y']], mode="markers+text",
            marker=dict(size=35, color="yellow", symbol="triangle-right", line=dict(width=3, color="orange")),
            text=[current['label']], textposition="bottom center",
            textfont=dict(size=21, color="darkred", family="Arial Black")
        )
        
        fig.update_layout(margin=dict(l=5, r=5, t=5, b=5), height=680)
        
        with placeholder.container():
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"plotly_render_{render_count}")
        
        render_count += 1
        time.sleep(1.8)