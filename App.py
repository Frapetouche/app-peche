import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Pêche QC - Navigation", page_icon="⚓", layout="wide")

st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 20px !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚓ Application Pêche & Marées Québec")

st.sidebar.header("📍 Position & Prises")

zone = st.sidebar.selectbox(
    "Choix du plan d'eau :",
    ["Secteur Saguenay (Fjord/Lac)", "Fleuve Québec / Lévis", "Estuaire Rimouski", "Lac Saint-Pierre", "Fleuve Montréal"]
)

coords_dict = {
    "Secteur Saguenay (Fjord/Lac)": [48.4167, -70.8333],
    "Fleuve Québec / Lévis": [46.8139, -71.2082],
    "Estuaire Rimouski": [48.4484, -68.5239],
    "Lac Saint-Pierre": [46.1950, -72.9242],
    "Fleuve Montréal": [45.5017, -73.5673]
}
current_coords = coords_dict[zone]

st.sidebar.markdown("---")
st.sidebar.subheader("⚖️ Calculateur de Prise i-Pêche")

espece = st.sidebar.selectbox("Espèce capturée :", ["Doré Jaune", "Truite Mouchetée (Omble)"])
taille = st.sidebar.number_input("Longueur du poisson (en cm) :", min_value=0.0, max_value=120.0, value=35.0, step=0.5)

if espece == "Doré Jaune":
    if 37.0 <= taille <= 53.0:
        st.sidebar.success(f"✅ **PRISE LÉGALE ({taille} cm)**")
    elif taille < 37.0:
        st.sidebar.error(f"🚨 **TROP PETIT ({taille} cm)** (Min: 37cm)")
    else:
        st.sidebar.error(f"🚨 **GRAND GÉNITEUR ({taille} cm)** (Max: 53cm)")
else:
    if taille >= 10.0:
        st.sidebar.success(f"✅ **PRISE LÉGALE ({taille} cm)**")
    else:
        st.sidebar.error(f"🚨 **TROP PETIT ({taille} cm)**")

st.subheader("📺 Mode d'affichage de l'Écran Principal")
col_btn1, col_btn2 = st.columns(2)

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "bathymetrie"

with col_btn1:
    if st.button("🌊 CARTE BATHYMÉTRIQUE"):
        st.session_state.view_mode = "bathymetrie"
with col_btn2:
    if st.button("⛈️ RADAR MÉTÉO"):
        st.session_state.view_mode = "meteo"

st.markdown("---")

# --- FONCTIONS EN CACHE POUR CHARGEMENT ÉCLAIR ---
@st.cache_resource
def get_bathymetry_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=11, control_scale=False, tiles=None)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Bathymétrie',
        overlay=False
    ).add_to(m)
    folium.Marker([lat, lon], popup="Position", icon=folium.Icon(color="blue", icon="anchor", prefix="fa")).add_to(m)
    return m

@st.cache_resource
def get_meteo_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=9, control_scale=False)
    folium.TileLayer(
        tiles='https://tilecache.rainviewer.com/v2/radar/nowcast/256/{z}/{x}/{y}/2/1_1.png',
        attr='RainViewer',
        name='Radar Pluie',
        overlay=True,
        opacity=0.65
    ).add_to(m)
    folium.Marker([lat, lon], popup="Position", icon=folium.Icon(color="red", icon="cloud", prefix="fa")).add_to(m)
    return m

# Affiche la carte pré-chargée en mémoire
if st.session_state.view_mode == "bathymetrie":
    st.info(f"🟢 **Bathymétrie** — {zone}")
    map_obj = get_bathymetry_map(current_coords[0], current_coords[1])
else:
    st.warning(f"⛈️ **Radar Météo** — {zone}")
    map_obj = get_meteo_map(current_coords[0], current_coords[1])

st_folium(map_obj, width="100%", height=500, returned_objects=[], key=f"map_{st.session_state.view_mode}_{zone}")

st.markdown("---")
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.markdown("🔹 **Astuce terrain :** Taches vertes foncées, jaunes ou rouges = quittez l'eau.")
with col_info2:
    st.markdown("🔹 **Réglementation :** Règles simplifiées du MFFP.")
