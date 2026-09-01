import streamlit as st
import folium
from streamlit_folium import st_folium

# Configuration ultra-scannable pour mobile et tablette
st.set_page_config(page_title="Pêche QC - Navigation", page_icon="⚓", layout="wide")

# --- STYLE CSS POUR DE GROS BOUTONS FACILES À CLIQUER ---
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

# --- BARRE LATÉRALE : CONFIGURATION & CALCULATEUR EXPRESS ---
st.sidebar.header("📍 Position & Prises")

zone = st.sidebar.selectbox(
    "Choix du plan d'eau :",
    ["Secteur Saguenay (Fjord/Lac)", "Fleuve Québec / Lévis", "Estuaire Rimouski", "Lac Saint-Pierre", "Fleuve Montréal"]
)

# Coordonnées GPS des secteurs
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
st.sidebar.write("Vérification rapide de la taille sur le bateau :")

espece = st.sidebar.selectbox("Espèce capturée :", ["Doré Jaune", "Truite Mouchetée (Omble)"])
taille = st.sidebar.number_input("Longueur du poisson (en cm) :", min_value=0.0, max_value=120.0, value=35.0, step=0.5)

# Règles simplifiées i-Pêche Québec (Zones majeures)
if espece == "Doré Jaune":
    if 37.0 <= taille <= 53.0:
        st.sidebar.success(f"✅ **PRISE LÉGALE ({taille} cm)** : Vous pouvez le garder dans votre quota standard.")
    elif taille < 37.0:
        st.sidebar.error(f"🚨 **TROP PETIT ({taille} cm)** : Remise à l'eau obligatoire (Limite min: 37cm).")
    else:
        st.sidebar.error(f"🚨 **GRAND GÉNITEUR ({taille} cm)** : Remise à l'eau obligatoire (Limite max: 53cm).")
else:
    if taille >= 10.0:
        st.sidebar.success(f"✅ **PRISE LÉGALE ({taille} cm)** : Respectez la limite de possession de votre zone.")
    else:
        st.sidebar.error(f"🚨 **TROP PETIT ({taille} cm)** : Laissez-le grandir.")

# --- NAVIGATION PRINCIPALE : COMMUTATEUR DE CARTE RAPIDE ---
st.subheader("📺 Mode d'affichage de l'Écran Principal")
col_btn1, col_btn2 = st.columns(2)

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "bathymetrie"

with col_btn1:
    if st.button("🌊 CARTE BATHYMÉTRIQUE (Fonds)"):
        st.session_state.view_mode = "bathymetrie"
with col_btn2:
    if st.button("⛈️ RADAR MÉTÉO (Pluie & Orages)"):
        st.session_state.view_mode = "meteo"

st.markdown("---")

if st.session_state.view_mode == "bathymetrie":
    st.info(f"🟢 **Affichage actuel : Bathymétrie de base** — {zone}. Les nuances bleues indiquent les structures et fosses.")
    m = folium.Map(location=current_coords, zoom_start=11, control_scale=True)
    
    # URL corrigée pour ESRI World Ocean Base
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}',
        attr='Esri, Garmin, GEBCO, NOAA NGDC, and other contributors',
        name='Bathymétrie ESRI',
        overlay=False
    ).add_to(m)
    
    # Couche optionnelle de repères / références
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Reference/MapServer/tile/{z}/{y}/{x}',
        attr='Esri, Garmin, USGS, NGA',
        name='Repères ESRI',
        overlay=True
    ).add_to(m)
    
    folium.Marker(
        current_coords, 
        popup="Position choisie", 
        icon=folium.Icon(color="blue", icon="anchor", prefix="fa")
    ).add_to(m)
    
    st_folium(m, width="100%", height=550, returned_objects=[])

else:
    st.warning(f"⛈️ **Affichage actuel : Radar Météo Temps Réel** — {zone}. Observez les cellules de pluie s'approcher.")
    m = folium.Map(location=current_coords, zoom_start=9, control_scale=True)
    
    folium.TileLayer('OpenStreetMap', name='Carte standard').add_to(m)
    
    # URL corrigée pour le radar de pluie RainViewer
    folium.TileLayer(
        tiles='https://tilecache.rainviewer.com/v2/radar/nowcast/256/{z}/{x}/{y}/2/1_1.png',
        attr='RainViewer Real-time Radar',
        name='Radar Pluie',
        overlay=True,
        opacity=0.65
    ).add_to(m)
    
    folium.Marker(
        current_coords, 
        popup="Position choisie", 
        icon=folium.Icon(color="red", icon="cloud", prefix="fa")
    ).add_to(m)
    
    st_folium(m, width="100%", height=550, returned_objects=[])

st.markdown("---")
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.markdown("🔹 **Astuce terrain :** Si le radar montre des taches **vertes foncées, jaunes ou rouges**, quittez le plan d'eau immédiatement.")
with col_info2:
    st.markdown("🔹 **Réglementation officielle :** Ce calculateur utilise les règles simplifiées du MFFP/M環境. Consultez toujours le site officiel avant de conserver une prise incertaine.")
