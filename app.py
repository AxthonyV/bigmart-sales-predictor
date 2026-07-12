import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="BigMart Sales Intelligence", layout="wide")

# ----------------------------------------------------------------------------
# ESTILOS — Dashboard ejecutivo, minimalista y corporativo
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
        gap: 0.7rem;
        margin: 2.1rem 0 1rem 0;
    }
    .section-marker {
        width: 4px; height: 22px;
        border-radius: 3px;
        background: linear-gradient(180deg, #6366F1, #4F46E5);
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
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.9rem;
        padding-bottom: 0.7rem;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }

    /* ---------- SUMMARY CHIPS (main canvas) ---------- */
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.9rem;
        margin-bottom: 0.4rem;
    }
    .summary-card {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 1rem 1.15rem;
    }
    .summary-card .stitle {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #7C8AA5;
        margin-bottom: 0.65rem;
        padding-bottom: 0.55rem;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .summary-card .srow {
        display: flex;
        justify-content: space-between;
        font-size: 0.83rem;
        padding: 0.22rem 0;
        color: #C7CEDE;
    }
    .summary-card .srow b {
        color: #F1F3F9;
        font-weight: 600;
        text-align: right;
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
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li,
    ul[role="listbox"] {
        background-color: #161B22 !important;
        color: #E7EAF0 !important;
    }
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li[aria-selected="true"] {
        background-color: rgba(99,102,241,0.25) !important;
        color: #FFFFFF !important;
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

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {
        background: #0B0F19;
        border-right: 1px solid rgba(255,255,255,0.07);
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.6rem;
    }
    .sidebar-title {
        font-family: 'Sora', sans-serif;
        font-size: 1.02rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.2rem;
    }
    .sidebar-desc {
        color: #7C8AA5;
        font-size: 0.78rem;
        margin-bottom: 1.3rem;
        line-height: 1.5;
    }
    .sidebar-sub {
        font-size: 0.74rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #A5B4FC;
        margin: 1.1rem 0 0.7rem 0;
    }
    .status-badge {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.35rem 0.65rem;
        border-radius: 8px;
        margin-top: 0.2rem;
    }
    .status-up { background: rgba(34,197,94,0.12); color: #4ADE80; border: 1px solid rgba(34,197,94,0.3); }
    .status-down { background: rgba(248,113,113,0.12); color: #F87171; border: 1px solid rgba(248,113,113,0.3); }
    .status-flat { background: rgba(156,166,190,0.1); color: #9CA6BE; border: 1px solid rgba(156,166,190,0.25); }

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
# DICCIONARIOS DE VISUALIZACIÓN
# ----------------------------------------------------------------------------
tipos_producto = {
    'Dairy': 'Lácteos', 'Soft Drinks': 'Bebidas gaseosas', 'Meat': 'Carnes',
    'Fruits and Vegetables': 'Frutas y verduras', 'Household': 'Artículos del hogar',
    'Baking Goods': 'Repostería', 'Snack Foods': 'Snacks / bocadillos',
    'Frozen Foods': 'Congelados', 'Breakfast': 'Desayunos',
    'Health and Hygiene': 'Salud e higiene', 'Hard Drinks': 'Bebidas alcohólicas',
    'Canned': 'Enlatados', 'Breads': 'Panes', 'Starchy Foods': 'Féculas (papa, arroz, etc.)',
    'Others': 'Otros', 'Seafood': 'Mariscos'
}
tamanos_tienda = {'Small': 'Pequeña', 'Medium': 'Mediana', 'High': 'Grande'}
zonas = {
    'Tier 1': 'Tier 1 — Ciudad principal / grande',
    'Tier 2': 'Tier 2 — Ciudad intermedia',
    'Tier 3': 'Tier 3 — Ciudad pequeña'
}
tipos_tienda = {
    'Grocery Store': 'Tienda de abarrotes (pequeña, de barrio)',
    'Supermarket Type1': 'Supermercado estándar (mediano)',
    'Supermarket Type2': 'Supermercado grande',
    'Supermarket Type3': 'Hipermercado (el formato más grande)'
}

# ----------------------------------------------------------------------------
# SIDEBAR — CONFIGURACIÓN DEL ESCENARIO BASE
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-title">Configuración del Escenario</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-desc">Define las características del producto y del punto '
        'de venta que se usarán como escenario base para la predicción.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-sub">Producto</div>', unsafe_allow_html=True)
    item_mrp = st.slider(
        "Precio Máximo de Venta (USD)", 30.0, 300.0, 140.0,
        help="Precio de lista sugerido del producto. A mayor precio, generalmente mayor ingreso por unidad vendida."
    )
    item_weight = st.slider(
        "Peso del Producto (kg)", 4.0, 22.0, 12.0,
        help="Peso del artículo en kilogramos."
    )
    item_fat = st.selectbox(
        "Contenido de Grasa", ['Low Fat', 'Regular'],
        help="Clasificación nutricional del producto: bajo en grasa o regular.",
        format_func=lambda x: "Bajo en grasa" if x == "Low Fat" else "Regular"
    )
    item_type = st.selectbox(
        "Categoría de Producto", list(tipos_producto.keys()),
        help="Rubro o categoría a la que pertenece el producto.",
        format_func=lambda x: tipos_producto[x]
    )

    st.divider()
    st.markdown('<div class="sidebar-sub">Tienda</div>', unsafe_allow_html=True)
    outlet_size = st.selectbox(
        "Tamaño de la Tienda", list(tamanos_tienda.keys()),
        help="Tamaño físico del establecimiento.",
        format_func=lambda x: tamanos_tienda[x]
    )
    outlet_location = st.selectbox(
        "Zona de Ubicación", list(zonas.keys()),
        help="Nivel de la ciudad donde está la tienda. Tier 1 son las ciudades más grandes/importantes, Tier 3 las más pequeñas.",
        format_func=lambda x: zonas[x]
    )
    outlet_type = st.selectbox(
        "Tipo de Canal", list(tipos_tienda.keys()),
        help="Formato o tamaño comercial del punto de venta.",
        format_func=lambda x: tipos_tienda[x]
    )
    outlet_age = st.slider(
        "Antigüedad del Establecimiento (años)", 0, 40, 15,
        help="Años que la tienda lleva funcionando desde su apertura."
    )

    st.divider()
    st.markdown('<div class="sidebar-sub">Visibilidad</div>', unsafe_allow_html=True)
    item_visibility_ratio = st.slider(
        "Nivel de Exhibición", 0.0, 3.5, 1.0,
        help="Compara la exhibición del producto contra el promedio de su categoría. 1.0 = exhibición promedio."
    )
    if item_visibility_ratio > 1.0:
        st.markdown('<span class="status-badge status-up">Sobre el promedio de la categoría</span>', unsafe_allow_html=True)
    elif item_visibility_ratio < 1.0:
        st.markdown('<span class="status-badge status-down">Bajo el promedio de la categoría</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-flat">Exhibición promedio</span>', unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# HERO / ENCABEZADO
# ----------------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-badge">UPAO · Aprendizaje Estadístico</div>
    <h1>BigMart Sales Intelligence</h1>
    <p>Plataforma predictiva de ventas basada en Random Forest. Estima el volumen de
    ventas esperado por artículo y simula el impacto financiero de cambios en precio y
    exhibición en punto de venta.</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# GLOSARIO — para que cualquiera entienda las variables antes de usarlas
# ----------------------------------------------------------------------------
with st.expander("Referencia de variables (haga clic para expandir)"):
    st.markdown("""
    <div style="color:#C7CEDE; font-size:0.9rem; line-height:1.7;">

    <b>Producto</b><br>
    • <b>Item_MRP</b>: precio máximo de venta sugerido para el producto (en USD).<br>
    • <b>Item_Weight</b>: peso del producto en kilogramos.<br>
    • <b>Item_Fat_Content</b>: si el producto es bajo en grasa o regular.<br>
    • <b>Item_Type</b>: categoría o rubro del producto (lácteos, bebidas, carnes, etc.).<br><br>

    <b>Tienda</b><br>
    • <b>Outlet_Size</b>: tamaño físico del establecimiento (pequeño, mediano o grande).<br>
    • <b>Outlet_Location_Type</b>: nivel de la ciudad donde está ubicada la tienda.
      "Tier 1" son ciudades grandes/principales, "Tier 3" son ciudades más pequeñas.<br>
    • <b>Outlet_Type</b>: tipo de establecimiento comercial:<br>
      &nbsp;&nbsp;— <i>Tienda de abarrotes</i>: local pequeño de barrio.<br>
      &nbsp;&nbsp;— <i>Supermercado estándar</i>: tamaño mediano, surtido básico.<br>
      &nbsp;&nbsp;— <i>Supermercado grande</i>: mayor variedad y espacio.<br>
      &nbsp;&nbsp;— <i>Hipermercado</i>: el formato más grande de la cadena.<br>
    • <b>Outlet_Age</b>: años que tiene la tienda funcionando desde su apertura.<br><br>

    <b>Visibilidad</b><br>
    • <b>Item_Visibility_MeanRatio</b>: qué tan visible está el producto en la tienda
      comparado con el promedio de su categoría. Un valor de 1.0 significa "exhibición
      promedio"; más de 1.0 significa que tiene más espacio o mejor ubicación en el
      punto de venta que productos similares.

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
        <div class="kpi-sub">100 árboles</div>
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
# RESUMEN DEL ESCENARIO CONFIGURADO (lienzo principal)
# ----------------------------------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-marker"></div>
    <h3>Escenario Base <span class="tag">— configurado desde el panel lateral</span></h3>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="summary-grid">
    <div class="summary-card">
        <div class="stitle">Producto</div>
        <div class="srow"><span>Precio</span><b>${item_mrp:,.2f}</b></div>
        <div class="srow"><span>Peso</span><b>{item_weight:.1f} kg</b></div>
        <div class="srow"><span>Grasa</span><b>{"Bajo en grasa" if item_fat == "Low Fat" else "Regular"}</b></div>
        <div class="srow"><span>Categoría</span><b>{tipos_producto[item_type]}</b></div>
    </div>
    <div class="summary-card">
        <div class="stitle">Tienda</div>
        <div class="srow"><span>Tamaño</span><b>{tamanos_tienda[outlet_size]}</b></div>
        <div class="srow"><span>Zona</span><b>{outlet_location}</b></div>
        <div class="srow"><span>Canal</span><b>{outlet_type}</b></div>
        <div class="srow"><span>Antigüedad</span><b>{outlet_age} años</b></div>
    </div>
    <div class="summary-card">
        <div class="stitle">Visibilidad</div>
        <div class="srow"><span>Nivel de exhibición</span><b>{item_visibility_ratio:.2f}</b></div>
        <div class="srow"><span>Referencia</span><b>1.00 = promedio</b></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# SIMULACIÓN DE ESCENARIOS
# ----------------------------------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-marker"></div>
    <h3>Simulación de Escenarios <span class="tag">— compara contra el escenario base</span></h3>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="scenario-panel"><p class="desc">Ajuste el precio o la exhibición del producto para proyectar el impacto financiero frente al escenario configurado en el panel lateral. Todo lo demás (peso, categoría, tienda) se mantiene igual.</p>', unsafe_allow_html=True)
sim_col1, sim_col2 = st.columns(2)
with sim_col1:
    sim_mrp = st.slider(
        "Precio Alternativo a Probar (USD)", 30.0, 300.0, item_mrp, key="sim_mrp",
        help="¿Qué pasaría si el precio fuera este en vez del configurado en el panel lateral?"
    )
with sim_col2:
    sim_visibility = st.slider(
        "Exhibición Alternativa a Probar", 0.0, 3.5, item_visibility_ratio, key="sim_vis",
        help="¿Qué pasaría si el producto tuviera este nivel de exhibición en vez del configurado en el panel lateral?"
    )
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
if st.button("Calcular Predicción", type="primary", use_container_width=True):
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
        f"**Interpretación:** bajo estas condiciones de producto y tienda, el modelo estima "
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
        st.success("El escenario simulado proyecta un incremento en ventas respecto al escenario base.")
    elif delta < 0:
        st.warning("El escenario simulado proyecta una reducción en ventas respecto al escenario base.")
    else:
        st.info("No se proyecta un cambio significativo entre ambos escenarios.")

st.markdown("""
<p class="footnote">
Modelo: Random Forest Regressor (100 árboles) · Validado con métricas de Weka:
Correlación 0.7396 · MAE 809.17 · RMSE 1,150.87<br>
Proyecto Final — Aprendizaje Estadístico — Universidad Privada Antenor Orrego (UPAO)
</p>
""", unsafe_allow_html=True)
