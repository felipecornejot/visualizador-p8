import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import requests

# --- Paleta de Colores ---
# Definición de colores en formato RGB (0-1) para Matplotlib
color_primario_1_rgb = (14/255, 69/255, 74/255) # 0E454A (Oscuro)
color_primario_2_rgb = (31/255, 255/255, 95/255) # 1FFF5F (Verde vibrante)
color_primario_3_rgb = (255/255, 255/255, 255/255) # FFFFFF (Blanco)

# Colores del logo de Sustrend para complementar
color_sustrend_1_rgb = (0/255, 155/255, 211/255) # 009BD3 (Azul claro)
color_sustrend_2_rgb = (0/255, 140/255, 207/255) # 008CCF (Azul medio)
color_sustrend_3_rgb = (0/255, 54/255, 110/255) # 00366E (Azul oscuro)

# Selección de colores para los gráficos
colors_for_charts = [color_primario_1_rgb, color_primario_2_rgb, color_sustrend_1_rgb, color_sustrend_3_rgb]

# --- Configuración de la página de Streamlit ---
st.set_page_config(layout="wide")

st.title('✨ Visualizador de Impactos - Proyecto P8')
st.subheader('Agente humectante del suelo 100% natural')
st.markdown("""
    Ajusta los parámetros para explorar cómo las proyecciones de impacto ambiental y económico del proyecto
    varían con diferentes escenarios de producción, reducción de agua y uso de materiales secundarios.
""")

# --- 1. Datos del Proyecto (Línea Base y Proyecciones) ---
# Datos línea base (según ficha P8)
base_agua = 450000  # litros (L/año)
base_material = 12750  # kg/año (85% de 15000 kg/año si el volumen de producción fuera 15000)
base_ingresos = 45000000  # CLP/año (estimado)

# --- 2. Widgets Interactivos para Parámetros (Streamlit) ---
st.sidebar.header('Parámetros de Simulación')

volumen_produccion = st.sidebar.slider(
    'Volumen producido (kg/año):',
    min_value=5000,
    max_value=20000,
    value=10000,
    step=1000,
    help="Volumen anual de producto (agente humectante) en kilogramos."
)

reduccion_agua_pct = st.sidebar.slider(
    'Reducción consumo agua (%):',
    min_value=0.1,
    max_value=0.3,
    value=0.3,
    step=0.01,
    # format='.1%', # Eliminado para evitar SyntaxError
    help="Porcentaje de reducción en el consumo de agua por hectárea tratada."
)

agroquimicos_ev_kg = st.sidebar.slider(
    'Agroquímicos evitados (kg/año):',
    min_value=100,
    max_value=1000,
    value=500,
    step=50,
    help="Cantidad de agroquímicos sintéticos evitados anualmente."
)

porcentaje_secundarias = st.sidebar.slider(
    '% materias primas secundarias:',
    min_value=0.7,
    max_value=0.9,
    value=0.85,
    step=0.01,
    # format='.1%', # Eliminado para evitar SyntaxError
    help="Porcentaje de materias primas secundarias utilizadas en la formulación del producto."
)

precio_venta = st.sidebar.slider(
    'Precio de venta (CLP/kg):',
    min_value=2000,
    max_value=6000,
    value=4000,
    step=200,
    help="Precio de venta por kilogramo del agente humectante."
)

# --- 3. Cálculos de Indicadores ---
ahorro_agua = volumen_produccion * reduccion_agua_pct * 10  # litros, considerando 10 L/kg de producto (como en el script original)
material_valorizado = volumen_produccion * porcentaje_secundarias
ingresos_generados = volumen_produccion * precio_venta
alianzas_comerciales = 5 # Fijo según la descripción
empleos_verdes = 4 # Fijo según la descripción

st.header('Resultados Proyectados Anuales:')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="💧 **Ahorro de Agua**", value=f"{ahorro_agua:,.0f} litros/año")
    st.caption("Ahorro de agua logrado por la aplicación del agente humectante.")
with col2:
    st.metric(label="♻️ **Material Valorizado**", value=f"{material_valorizado:,.0f} kg/año")
    st.caption("Cantidad de materias primas secundarias reincorporadas en el proceso.")
with col3:
    st.metric(label="💰 **Ingresos Generados**", value=f"CLP {ingresos_generados:,.0f}")
    st.caption("Ingresos totales por la venta del agente humectante.")

col4, col5 = st.columns(2)

with col4:
    st.metric(label="🌱 **Agroquímicos Evitados**", value=f"{agroquimicos_ev_kg:,.0f} kg/año")
    st.caption("Reducción en el uso de agroquímicos sintéticos.")
with col5:
    st.metric(label="🤝 **Alianzas Comerciales**", value=f"{alianzas_comerciales}")
    st.caption("Número de alianzas comerciales colaborativas generadas.")

st.markdown("---")

st.header('📊 Análisis Gráfico de Impactos')

# --- Visualización (Gráficos 2D con Matplotlib) ---
# Creamos una figura con 3 subplots (2D)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7), facecolor=color_primario_3_rgb)
fig.patch.set_facecolor(color_primario_3_rgb)

# Definición de etiquetas y valores para los gráficos de barras 2D
labels = ['Línea Base', 'Proyección']
bar_width = 0.6
x = np.arange(len(labels))

# --- Gráfico 1: Ahorro de Agua (L/año) ---
agua_values = [base_agua, ahorro_agua]
bars1 = ax1.bar(x, agua_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax1.set_ylabel('Litros/año', fontsize=12, color=colors_for_charts[3])
ax1.set_title('Ahorro de Agua', fontsize=14, color=colors_for_charts[3], pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax1.yaxis.set_tick_params(colors=colors_for_charts[0])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(axis='x', length=0)
max_agua_val = max(agua_values)
ax1.set_ylim(bottom=0, top=max(max_agua_val * 1.15, 1))
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.0f}", ha='center', va='bottom', fontsize=8, fontweight='bold', color=colors_for_charts[0])

# --- Gráfico 2: Material Valorizado (kg/año) ---
material_values = [base_material, material_valorizado]
bars2 = ax2.bar(x, material_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax2.set_ylabel('kg/año', fontsize=12, color=colors_for_charts[0])
ax2.set_title('Material Valorizado', fontsize=14, color=colors_for_charts[3], pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax2.yaxis.set_tick_params(colors=colors_for_charts[0])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(axis='x', length=0)
max_material_val = max(material_values)
ax2.set_ylim(bottom=0, top=max(max_material_val * 1.15, 1))
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.0f}", ha='center', va='bottom', fontsize=8, fontweight='bold', color=colors_for_charts[0])

# --- Gráfico 3: Ingresos Generados (CLP/año) ---
ingresos_values = [base_ingresos, ingresos_generados]
bars3 = ax3.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax3.set_ylabel('CLP/año', fontsize=12, color=colors_for_charts[3])
ax3.set_title('Ingresos Generados', fontsize=14, color=colors_for_charts[3], pad=20)
ax3.set_xticks(x)
ax3.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax3.yaxis.set_tick_params(colors=colors_for_charts[0])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.tick_params(axis='x', length=0)
max_ingresos_val = max(ingresos_values)
ax3.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000))
for bar in bars3:
    yval = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"CLP {yval:,.0f}", ha='center', va='bottom', fontsize=8, fontweight='bold', color=colors_for_charts[0])

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
st.pyplot(fig)

# --- Funcionalidad de descarga de cada gráfico ---
st.markdown("---")
st.subheader("Descargar Gráficos Individualmente")

# Función auxiliar para generar el botón de descarga
def download_button(fig, filename_prefix, key):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button(
        label=f"Descargar {filename_prefix}.png",
        data=buf.getvalue(),
        file_name=f"{filename_prefix}.png",
        mime="image/png",
        key=key
    )

# Crear figuras individuales para cada gráfico para poder descargarlas
# Figura 1: Ahorro de Agua
fig_agua, ax_agua = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_agua.bar(x, agua_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax_agua.set_ylabel('Litros/año', fontsize=12, color=colors_for_charts[3])
ax_agua.set_title('Ahorro de Agua', fontsize=14, color=colors_for_charts[3], pad=20)
ax_agua.set_xticks(x)
ax_agua.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_agua.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_agua.spines['top'].set_visible(False)
ax_agua.spines['right'].set_visible(False)
ax_agua.tick_params(axis='x', length=0)
ax_agua.set_ylim(bottom=0, top=max(max_agua_val * 1.15, 1))
for bar in ax_agua.patches:
    yval = bar.get_height()
    ax_agua.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.0f}", ha='center', va='bottom', fontsize=8, fontweight='bold', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_agua, "Ahorro_Agua", "download_agua")
plt.close(fig_agua)

# Figura 2: Material Valorizado
fig_material, ax_material = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_material.bar(x, material_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax_material.set_ylabel('kg/año', fontsize=12, color=colors_for_charts[0])
ax_material.set_title('Material Valorizado', fontsize=14, color=colors_for_charts[3], pad=20)
ax_material.set_xticks(x)
ax_material.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_material.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_material.spines['top'].set_visible(False)
ax_material.spines['right'].set_visible(False)
ax_material.tick_params(axis='x', length=0)
ax_material.set_ylim(bottom=0, top=max(max_material_val * 1.15, 1))
for bar in ax_material.patches:
    yval = bar.get_height()
    ax_material.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.0f}", ha='center', va='bottom', fontsize=8, fontweight='bold', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_material, "Material_Valorizado", "download_material")
plt.close(fig_material)

# Figura 3: Ingresos Generados
fig_ingresos, ax_ingresos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_ingresos.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax_ingresos.set_ylabel('CLP/año', fontsize=12, color=colors_for_charts[3])
ax_ingresos.set_title('Ingresos Generados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_ingresos.set_xticks(x)
ax_ingresos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_ingresos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_ingresos.spines['top'].set_visible(False)
ax_ingresos.spines['right'].set_visible(False)
ax_ingresos.tick_params(axis='x', length=0)
ax_ingresos.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000))
for bar in ax_ingresos.patches:
    yval = bar.get_height()
    ax_ingresos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"CLP {yval:,.0f}", ha='center', va='bottom', fontsize=8, fontweight='bold', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_ingresos, "Ingresos_Generados", "download_ingresos")
plt.close(fig_ingresos)

st.markdown("---")
st.markdown("### Información Adicional:")
st.markdown(f"- **Estado de Avance y Recomendaciones:** El proyecto se encuentra en fase piloto de validación técnica del producto humectante, con pruebas de formulación avanzadas y estudios de desempeño agronómico en curso. Se ha logrado estabilizar una versión funcional del agente humectante a partir de descartes de quillay, con propiedades fisicoquímicas adecuadas para su aplicación en suelos agrícolas. Asimismo, se ha iniciado la fase de ensayos de campo para validar la eficiencia hídrica y el comportamiento del producto en comparación con soluciones convencionales.\nDesde el punto de vista de la valorización de materias primas secundarias, se ha logrado articular una cadena de suministro con proveedores locales de descartes agroindustriales, asegurando la disponibilidad y trazabilidad del insumo base. También se están evaluando alianzas comerciales con empresas del sector agrícola y hortofrutícola para el escalamiento de la solución.\nEn cuanto a la documentación de impactos, se ha iniciado la recopilación de datos para aplicar metodologías cuantitativas en eficiencia hídrica y circularidad. No obstante, algunos indicadores ambientales y económicos aún requieren ajustes metodológicos y validación empírica, especialmente en lo relativo a ahorro de agua por hectárea y sustitución efectiva de productos sintéticos.")

st.markdown("---")
# Texto de atribución centrado
st.markdown("<div style='text-align: center;'>Visualizador Creado por el equipo Sustrend SpA en el marco del Proyecto TT GREEN Foods</div>", unsafe_allow_html=True)

# Aumentar el espaciado antes de los logos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Mostrar Logos ---
col_logos_left, col_logos_center, col_logos_right = st.columns([1, 2, 1])

with col_logos_center:
    sustrend_logo_url = "https://drive.google.com/uc?id=1vx_znPU2VfdkzeDtl91dlpw_p9mmu4dd"
    ttgreenfoods_logo_url = "https://drive.google.com/uc?id=1uIQZQywjuQJz6Eokkj6dNSpBroJ8tQf8"

    try:
        sustrend_response = requests.get(sustrend_logo_url)
        sustrend_response.raise_for_status()
        sustrend_image = Image.open(BytesIO(sustrend_response.content))

        ttgreenfoods_response = requests.get(ttgreenfoods_logo_url)
        ttgreenfoods_response.raise_for_status()
        ttgreenfoods_image = Image.open(BytesIO(ttgreenfoods_response.content))

        st.image([sustrend_image, ttgreenfoods_image], width=100)
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar los logos desde las URLs. Por favor, verifica los enlaces: {e}")
    except Exception as e:
        st.error(f"Error inesperado al procesar las imágenes de los logos: {e}")

st.markdown("<div style='text-align: center; font-size: small; color: gray;'>Viña del Mar, Valparaíso, Chile</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align: center; font-size: smaller; color: gray;'>Versión del Visualizador: 1.8</div>", unsafe_allow_html=True) # Actualizada la versión
st.sidebar.markdown(f"<div style='text-align: center; font-size: x-small; color: lightgray;'>Desarrollado con Streamlit</div>", unsafe_allow_html=True)
