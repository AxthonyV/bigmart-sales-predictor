import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="BigMart Sales Intelligence", layout="wide", page_icon="📊")

# ----------------------------------------------------------------------------
# ESTILOS - Identidad corporativa (Dark Mode ejecutivo)
# ----------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #F8FAFC;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
    }
    .main-header {
        padding: 1.4rem 1.25rem;
        border: 1px solid #243041;
        border-radius: 14px;
        background: linear-gradient(90deg, rgba(79, 139, 249, 0.16), rgba(255,255,255,0.02));
        margin-bottom: 1.4rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
    }
    .main-header h1 {
        color: #FAFAFA;
        font-size: 2.2rem;
        margin-bottom: 0.25rem;
        font-weight: 700;
        letter-spacing: 0.01em;
    }
    .main-header p {
        color: #E5E7EB;
        font-size: 0.96rem;
        margin: 0;
    }
    .section-title {
        color: #FAFAFA;
        font-size: 1.16rem;
        font-weight: 700;
        margin-top: 1.45rem;
        margin-bottom: 0.85rem;
        border-left: 4px solid #4F8BF9;
        padding-left: 0.7rem;
        letter-spacing: 0.01em;
    }
    div[data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #2C3440;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.24);
        margin-bottom: 0.9rem;
    }
    div[data-testid="stMetricLabel"] {
        color: #E5E7EB !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em;
    }
    div[data-testid="stMetricValue"] {
        color: #FAFAFA !important;
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        line-height: 1.2;
    }
    div[data-testid="stMetricDelta"] {
        color: #CBD5E1 !important;
        font-size: 0.93rem !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricDelta"][style*="color: rgb(0, 128, 0)"],
    div[data-testid="stMetricDelta"][style*="color: green"],
    div[data-testid="stMetricDelta"][style*="color: #22C55E"],
    div[data-testid="stMetricDelta"][style*="color: rgb(34, 197, 94)"] {
        color: #22C55E !important;
    }
    div[data-testid="stMetricDelta"][style*="color: rgb(255, 0, 0)"],
    div[data-testid="stMetricDelta"][style*="color: red"],
    div[data-testid="stMetricDelta"][style*="color: #EF4444"],
    div[data-testid="stMetricDelta"][style*="color: rgb(239, 68, 68)"] {
        color: #EF4444 !important;
    }
    label[data-testid="stWidgetLabel"] {
        color: #F3F4F6 !important;
        font-size: 0.96rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.25rem;
    }
    div[data-testid="stSelectbox"],
    div[data-testid="stSlider"] {
        margin-bottom: 0.4rem;
    }
    div[data-testid="stCaption"] {
        color: #D1D5DB !important;
        font-size: 0.9rem !important;
    }
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #4F8BF9, #3B82F6);
        color: #FFFFFF;
        border: 1px solid #3B82F6;
        border-radius: 10px;
        padding: 0.7rem 1.1rem;
        font-weight: 700;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.24);
    }
    div[data-testid="stButton"] > button:hover {
        border-color: #7FB0FF;
        box-shadow: 0 8px 18px rgba(79, 139, 249, 0.3);
    }
    div[data-testid="stAlert"] {
        background-color: rgba(22, 27, 34, 0.95);
        border: 1px solid #2C3440;
        color: #F8FAFC;
        border-radius: 10px;
    }
    .scenario-box {
        background-color: #161B22;
        border: 1px solid #2C3440;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.16);
    }
    .result-box {
        background: linear-gradient(135deg, #10291E, #163A2D);
        border: 1px solid #2E8B57;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 1rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    }
    .result-box h2 {
        color: #4ADE80;
        margin: 0;
        font-size: 2rem;
        font-weight: 800;
    }
    .footnote {
        color: #9CA3AF;
        font-size: 0.84rem;
        margin-top: 1rem;
        line-height: 1.5;
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
# ENCABEZADO
# ----------------------------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>📊 BigMart Sales Intelligence</h1>
    <p>Sistema de estimación de ventas mediante Aprendizaje Estadístico — Universidad Privada Antenor Orrego (UPAO)</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# KPIs DEL MODELO
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title">📈 Métricas de Desempeño del Modelo</div>', unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Algoritmo", "Random Forest", "100 árboles")
kpi2.metric("Correlación", "0.7396")
kpi3.metric("MAE", "809.17", help="Error Absoluto Medio (USD)")
kpi4.metric("RMSE", "1,150.87", help="Raíz del Error Cuadrático Medio (USD)")

st.markdown("---")

# ----------------------------------------------------------------------------
# LAYOUT DE TRES COLUMNAS: Producto / Tienda / Visibilidad
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title">⚙️ Parámetros de Predicción</div>', unsafe_allow_html=True)
col_producto, col_tienda, col_visibilidad = st.columns(3)

with col_producto:
    st.markdown("**🛒 Producto**")
    item_mrp = st.slider("Precio Máximo de Venta (Item_MRP)", 30.0, 300.0, 140.0)
    item_weight = st.slider("Peso del Producto (Item_Weight)", 4.0, 22.0, 12.0)
    item_fat = st.selectbox("Contenido de Grasa (Item_Fat_Content)", ['Low Fat', 'Regular'])
    item_type = st.selectbox("Categoría de Producto (Item_Type)", [
        'Dairy', 'Soft Drinks', 'Meat', 'Fruits and Vegetables', 'Household',
        'Baking Goods', 'Snack Foods', 'Frozen Foods', 'Breakfast',
        'Health and Hygiene', 'Hard Drinks', 'Canned', 'Breads',
        'Starchy Foods', 'Others', 'Seafood'
    ])

with col_tienda:
    st.markdown("**🏬 Tienda**")
    outlet_size = st.selectbox("Tamaño de la Tienda (Outlet_Size)", ['Small', 'Medium', 'High'])
    outlet_location = st.selectbox("Zona de Ubicación (Outlet_Location_Type)", ['Tier 1', 'Tier 2', 'Tier 3'])
    outlet_type = st.selectbox("Tipo de Canal (Outlet_Type)", [
        'Grocery Store', 'Supermarket Type1', 'Supermarket Type2', 'Supermarket Type3'
    ])
    outlet_age = st.slider("Antigüedad del Establecimiento (Años)", 0, 40, 15)

with col_visibilidad:
    st.markdown("**👁️ Visibilidad**")
    item_visibility_ratio = st.slider("Ratio de Visibilidad Individual/Promedio", 0.0, 3.5, 1.0)
    st.caption("Valores > 1.0 indican que el producto tiene más exhibición que el promedio de su categoría.")

st.markdown("---")

# ----------------------------------------------------------------------------
# SIMULACIÓN DE ESCENARIOS (para gerencia)
# ----------------------------------------------------------------------------
st.markdown('<div class="section-title">🧪 Simulación de Escenarios Financieros</div>', unsafe_allow_html=True)
st.markdown('<div class="scenario-box">', unsafe_allow_html=True)
st.markdown("Ajusta el precio o la exhibición del producto para comparar el impacto proyectado en ventas frente al escenario base.")

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
# BOTÓN DE EJECUCIÓN
# ----------------------------------------------------------------------------
if st.button("🚀 Calcular Volumen de Ventas Esperado", use_container_width=True):
    pred_base = predecir(item_mrp, item_visibility_ratio)
    pred_sim = predecir(sim_mrp, sim_visibility)
    delta = pred_sim - pred_base

    st.markdown(f"""
    <div class="result-box">
        <p style="color:#D1D5DB; margin-bottom:0.35rem; font-weight:600;">Ventas Proyectadas — Escenario Base</p>
        <h2>${pred_base:,.2f} USD</h2>
    </div>
    """, unsafe_allow_html=True)

    st.info(
        f"💡 **Interpretación:** el modelo estima que, bajo estas condiciones de producto y tienda, "
        f"el punto de venta generará aproximadamente **${pred_base:,.2f} USD** en ventas para este ítem. "
        f"Esta cifra es una proyección estadística, no una garantía comercial."
    )

    st.markdown("#### 📊 Comparación de Escenarios")
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Escenario Base", f"${pred_base:,.2f}")
    res_col2.metric("Escenario Simulado", f"${pred_sim:,.2f}", f"{delta:+,.2f}")
    res_col3.metric("Cambio Proyectado", f"{(delta / pred_base * 100 if pred_base else 0):+.1f}%")

    if delta > 0:
        st.success("📈 El escenario simulado proyecta un incremento en ventas respecto al escenario base.")
    elif delta < 0:
        st.warning("📉 El escenario simulado proyecta una reducción en ventas respecto al escenario base.")
    else:
        st.info("➖ No se proyecta un cambio significativo entre ambos escenarios.")

    st.balloons()

st.markdown("""
<p class="footnote">
Modelo: Random Forest Regressor (100 árboles) · Validado con métricas de Weka: Correlación 0.7396 · MAE 809.17 · RMSE 1,150.87<br>
Proyecto Final — Aprendizaje Estadístico — UPAO
</p>
""", unsafe_allow_html=True)
