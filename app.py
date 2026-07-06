import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="BigMart Sales Intelligence", layout="wide", page_icon="📊")

# ----------------------------------------------------------------------------
# ESTILOS — Dashboard ejecutivo moderno
# ----------------------------------------------------------------------------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 10% 0%, #101827 0%, #0A0E17 45%, #060810 100%);
        color: #E7EAF0;
    }

    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; }

    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    /* ---------- HERO ---------- */
    .hero {
        position: relative;
        padding: 2.1rem 2.2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(99,102,241,0.16), rgba(16,185,129,0.06) 60%, rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.08);
        overflow: hidden;
        margin-bottom: 1.8rem;
    }
    .hero::before {
        content: "";
        position: absolute;
        top: -60px; right: -60px;
        width: 220px; height: 220px;
        background: radial-gradient(circle, rgba(99,102,241,0.35), transparent 70%);
        border-radius: 50%;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #A5B4FC;
        background: rgba(99,102,241,0.14);
        border: 1px solid rgba(99,102,241,0.3);
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        margin-bottom: 0.9rem;
    }
    .hero h1 {
        font-family: 'Sora', sans-serif;
        font-size: 2.15rem;
        font-weight: 800;
        color: #FFFFFF;
        margin: 0 0 0.45rem 0;
        letter-spacing: -0.01em;
    }
    .hero p {
        color: #9CA6BE;
        font-size: 0.98rem;
        margin: 0;
        max-width: 640px;
        line-height: 1.5;
    }

    /* ---------- KPI CARDS ---------- */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.9rem;
        margin-bottom: 1.9rem;
    }
    .kpi-card {
        background: linear-gradient(160deg, rgba(255,255,255,0.05), rgba(255,255,255,0.015));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.15rem 1.25rem;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(99,102,241,0.4);
    }
    .kpi-label {
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #7C8AA5;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-family: 'Sora', sans-serif;
        font-size: 1.65rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.1;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #22C55E;
        font-weight: 600;
        margin-top: 0.35rem;
    }

    /* ---------- SECTION HEADERS ---------- */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin: 2.1rem 0 1rem 0;
    }
    .section-icon {
        width: 30px; height: 30px;
        border-radius: 9px;
        display: flex; align-items: center; justify-content: center;
        background: linear-gradient(135deg, #6366F1, #4F46E5);
        font-size: 0.95rem;
        flex-shrink: 0;
    }
    .section-header h3 {
        font-family: 'Sora', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #F1F3F9;
        margin: 0;
    }
    .section-header span.tag {
        font-size: 0.72rem;
        color: #7C8AA5;
        font-weight: 500;
        margin-left: 0.3rem;
    }

    /* ---------- PANEL / GROUP CARDS ---------- */
    .panel {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 1.3rem 1.4rem 0.6rem 1.4rem;
        height: 100%;
    }
    .panel-title {
        font-size: 0.88rem;
        font-weight: 700;
        color: #C7CEDE;
        display: flex;
        align-items: center;
        gap: 0.45rem;
        margin-bottom: 0.9rem;
        padding-bottom: 0.7rem;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }

    /* ---------- WIDGET LABELS / INPUTS ---------- */
    label[data-testid="stWidgetLabel"] p {
        color: #AEB6C9 !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
    }
    div[data-testid="stSlider"], div[data-testid="stSelectbox"] {
        margin-bottom: 0.55rem;
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.04) !important;
        border-color: rgba(255,255,255,0.12) !important;
        border-radius: 9px !important;
    }
    div[data-testid="stSlider"] div[role="slider"] {
        background-color: #6366F1 !important;
        box-shadow: 0 0 0 4px rgba(99,102,241,0.2) !important;
    }
    div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"] {
        color: #6B7690 !important;
        font-size: 0.72rem !important;
    }
    div[data-testid="stSliderThumbValue"] {
        color: #C7D2FE !important;
        font-weight: 700 !important;
    }
    div[data-testid="stCaptionContainer"] p {
        color: #7C8AA5 !important;
        font-size: 0.8rem !important;
    }

    /* ---------- SCENARIO PANEL ---------- */
    .scenario-panel {
        background: linear-gradient(135deg, rgba(236,72,153,0.07), rgba(99,102,241,0.05));
        border: 1px solid rgba(236,72,153,0.18);
        border-radius: 16px;
        padding: 1.3rem 1.5rem 0.7rem 1.5rem;
        margin-bottom: 0.5rem;
    }
    .scenario-panel p.desc {
        color: #B7BFD4;
        font-size: 0.88rem;
        margin-top: -0.2rem;
        margin-bottom: 1rem;
    }

    /* ---------- BUTTON ---------- */
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #6366F1, #4338CA);
        color: #FFFFFF;
        border: none;
        border-radius: 12px;
        padding: 0.85rem 1.2rem;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.01em;
        box-shadow: 0 10px 24px rgba(99,102,241,0.35);
        transition: all 0.15s ease;
        margin-top: 0.6rem;
    }
    div[data-testid="stButton"] > button:hover {
        box-shadow: 0 12px 28px rgba(99,102,241,0.5);
        transform: translateY(-1px);
    }

    /* ---------- RESULT ---------- */
    .result-hero {
        background: linear-gradient(135deg, rgba(16,185,129,0.14), rgba(16,185,129,0.02));
        border: 1px solid rgba(16,185,129,0.35);
        border-radius: 18px;
        padding: 1.8rem;
        text-align: center;
        margin-top: 1.4rem;
    }
    .result-hero .rlabel {
        color: #86EFAC;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    }
    .result-hero .rvalue {
        font-family: 'Sora', sans-serif;
        color: #FFFFFF;
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.01em;
    }

    .compare-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.9rem;
        margin-top: 1.3rem;
    }
    .compare-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 1rem 1.1rem;
    }
    .compare-card .clabel {
        color: #7C8AA5;
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.4rem;
    }
    .compare-card .cvalue {
        font-family: 'Sora', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #F1F3F9;
    }
    .compare-card .cdelta-up { color: #22C55E; font-weight: 700; font-size: 0.85rem; }
    .compare-card .cdelta-down { color: #F87171; font-weight: 700; font-size: 0.85rem; }
    .compare-card .cdelta-flat { color: #9CA6BE; font-weight: 700; font-size: 0.85rem; }

    div[data-testid="stAlert"] {
        background-color: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.09) !important;
        border-radius: 12px !important;
        color: #D7DCEA !important;
    }

    .footnote {
        color: #5C6580;
        font-size: 0.8rem;
        margin-top: 2.2rem;
        line-height: 1.6;
        border-top: 1px solid rgba(255,255,255,0.06);
        padding-top: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# CARGA DEL MODELO
# ----------------------------------------------------------------------------
with open('modelo_bigmart.pkl', 'rb') as f:
    modelo = pickle.load(f)
with open('columnas.pkl', 'rb') as f:
    columnas_modelo = pickle.load(f)

# ----------------------------------------------------------------------------
# HERO / ENCABEZADO
# ----------------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-badge">📊 UPAO · Aprendizaje Estadístico</div>
    <h1>BigMart Sales Intelligence</h1>
    <p>Plataforma predictiva de ventas basada en Random Forest. Estima el volumen de
    ventas esperado por artículo y simula el impacto financiero de cambios en precio y
    exhibición en punto de venta.</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# KPIs DEL MODELO
# ----------------------------------------------------------------------------
st.markdown("""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label">Algoritmo</div>
        <div class="kpi-value">Random Forest</div>
        <div class="kpi-sub">↑ 100 árboles</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Correlación</div>
        <div class="kpi-value">0.7396</div>
        <div class="kpi-sub">Ajuste del modelo</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">MAE</div>
        <div class="kpi-value">809.17</div>
        <div class="kpi-sub">Error absoluto medio (USD)</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">RMSE</div>
        <div class="kpi-value">1,150.87</div>
        <div class="kpi-sub">Raíz del error cuadrático (USD)</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# LAYOUT DE TRES COLUMNAS: Producto / Tienda / Visibilidad
# ----------------------------------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-icon">⚙️</div>
    <h3>Parámetros de Predicción <span class="tag">— configura el escenario base</span></h3>
</div>
""", unsafe_allow_html=True)

col_producto, col_tienda, col_visibilidad = st.columns(3)

with col_producto:
    st.markdown('<div class="panel"><div class="panel-title">🛒 Producto</div>', unsafe_allow_html=True)
    item_mrp = st.slider("Precio Máximo de Venta (Item_MRP)", 30.0, 300.0, 140.0)
    item_weight = st.slider("Peso del Producto (Item_Weight)", 4.0, 22.0, 12.0)
    item_fat = st.selectbox("Contenido de Grasa (Item_Fat_Content)", ['Low Fat', 'Regular'])
    item_type = st.selectbox("Categoría de Producto (Item_Type)", [
        'Dairy', 'Soft Drinks', 'Meat', 'Fruits and Vegetables', 'Household',
        'Baking Goods', 'Snack Foods', 'Frozen Foods', 'Breakfast',
        'Health and Hygiene', 'Hard Drinks', 'Canned', 'Breads',
        'Starchy Foods', 'Others', 'Seafood'
    ])
    st.markdown('</div>', unsafe_allow_html=True)

with col_tienda:
    st.markdown('<div class="panel"><div class="panel-title">🏬 Tienda</div>', unsafe_allow_html=True)
    outlet_size = st.selectbox("Tamaño de la Tienda (Outlet_Size)", ['Small', 'Medium', 'High'])
    outlet_location = st.selectbox("Zona de Ubicación (Outlet_Location_Type)", ['Tier 1', 'Tier 2', 'Tier 3'])
    outlet_type = st.selectbox("Tipo de Canal (Outlet_Type)", [
        'Grocery Store', 'Supermarket Type1', 'Supermarket Type2', 'Supermarket Type3'
    ])
    outlet_age = st.slider("Antigüedad del Establecimiento (Años)", 0, 40, 15)
    st.markdown('</div>', unsafe_allow_html=True)

with col_visibilidad:
    st.markdown('<div class="panel"><div class="panel-title">👁️ Visibilidad</div>', unsafe_allow_html=True)
    item_visibility_ratio = st.slider("Ratio de Visibilidad Individual/Promedio", 0.0, 3.5, 1.0)
    st.caption("Valores > 1.0 indican que el producto tiene más exhibición que el promedio de su categoría.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SIMULACIÓN DE ESCENARIOS
# ----------------------------------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-icon">🧪</div>
    <h3>Simulación de Escenarios <span class="tag">— compara contra el escenario base</span></h3>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="scenario-panel"><p class="desc">Ajusta el precio o la exhibición del producto para proyectar el impacto financiero frente al escenario configurado arriba.</p>', unsafe_allow_html=True)
sim_col1, sim_col2 = st.columns(2)
with sim_col1:
    sim_mrp = st.slider("Escenario: Precio Alternativo (Item_MRP)", 30.0, 300.0, item_mrp, key="sim_mrp")
with sim_col2:
    sim_visibility = st.slider("Escenario: Visibilidad Alternativa", 0.0, 3.5, item_visibility_ratio, key="sim_vis")
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# FUNCIÓN DE INFERENCIA
# ----------------------------------------------------------------------------
def predecir(mrp, visibilidad):
    datos = {
        'Item_Weight': item_weight, 'Item_Fat_Content': item_fat, 'Item_Type': item_type,
        'Item_MRP': mrp, 'Outlet_Size': outlet_size, 'Outlet_Location_Type': outlet_location,
        'Outlet_Type': outlet_type, 'Outlet_Age': outlet_age, 'Item_Visibility_MeanRatio': visibilidad
    }
    df_in = pd.DataFrame([datos])
    df_dummies = pd.get_dummies(df_in)
    df_dummies = df_dummies.reindex(columns=columnas_modelo, fill_value=0)
    pred = modelo.predict(df_dummies)[0]
    return max(pred, 0)

# ----------------------------------------------------------------------------
# BOTÓN DE EJECUCIÓN Y RESULTADOS
# ----------------------------------------------------------------------------
if st.button("🚀  Calcular Volumen de Ventas Esperado", use_container_width=True):
    pred_base = predecir(item_mrp, item_visibility_ratio)
    pred_sim = predecir(sim_mrp, sim_visibility)
    delta = pred_sim - pred_base
    delta_pct = (delta / pred_base * 100) if pred_base else 0.0

    st.markdown(f"""
    <div class="result-hero">
        <div class="rlabel">Ventas Proyectadas — Escenario Base</div>
        <div class="rvalue">${pred_base:,.2f} USD</div>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        f"💡 **Interpretación:** bajo estas condiciones de producto y tienda, el modelo estima "
        f"aproximadamente **${pred_base:,.2f} USD** en ventas para este ítem. Esta cifra es una "
        f"proyección estadística, no una garantía comercial."
    )

    if delta > 0:
        delta_class, delta_symbol = "cdelta-up", "▲"
    elif delta < 0:
        delta_class, delta_symbol = "cdelta-down", "▼"
    else:
        delta_class, delta_symbol = "cdelta-flat", "—"

    st.markdown(f"""
    <div class="compare-grid">
        <div class="compare-card">
            <div class="clabel">Escenario Base</div>
            <div class="cvalue">${pred_base:,.2f}</div>
        </div>
        <div class="compare-card">
            <div class="clabel">Escenario Simulado</div>
            <div class="cvalue">${pred_sim:,.2f}</div>
            <div class="{delta_class}">{delta_symbol} ${abs(delta):,.2f}</div>
        </div>
        <div class="compare-card">
            <div class="clabel">Cambio Proyectado</div>
            <div class="cvalue">{delta_pct:+.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if delta > 0:
        st.success("📈 El escenario simulado proyecta un incremento en ventas respecto al escenario base.")
    elif delta < 0:
        st.warning("📉 El escenario simulado proyecta una reducción en ventas respecto al escenario base.")
    else:
        st.info("➖ No se proyecta un cambio significativo entre ambos escenarios.")

    st.balloons()

st.markdown("""
<p class="footnote">
Modelo: Random Forest Regressor (100 árboles) · Validado con métricas de Weka:
Correlación 0.7396 · MAE 809.17 · RMSE 1,150.87<br>
Proyecto Final — Aprendizaje Estadístico — Universidad Privada Antenor Orrego (UPAO)
</p>
""", unsafe_allow_html=True)
