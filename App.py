import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuration de la page
st.set_page_config(
    page_title="Cartographie Bathymétrique & Isobathes - Québec",
    page_icon="🗺️",
    layout="wide"
)

# Données structurées des lacs avec des isobathes bien positionnées sur la superficie
@st.cache_data
def load_bathymetry_data():
    return {
        "Lac-Saint-Jean": {
            "lat": 48.60, "lon": -72.00, "zoom": 10, "max_depth": 63,
            "description": "Immense cuvette glaciaire, présence de fosses profondes centrales et de hauts-fonds sableux.",
            "isobathes": [
                {"prof": 10, "desc": "Plateau côtier et herbiers peu profonds", "lat": 48.65, "lon": -72.20, "rayon": 15000, "couleur": "#c6dbef"},
                {"prof": 25, "desc": "Pente intermédiaire de transition", "lat": 48.60, "lon": -72.10, "rayon": 11000, "couleur": "#9ecae1"},
                {"prof": 45, "desc": "Talus et fosses secondaires", "lat": 48.55, "lon": -72.00, "rayon": 7000, "couleur": "#4292c6"},
                {"prof": 63, "desc": "Bassin profond maximal (Fosse centrale historique)", "lat": 48.52, "lon": -71.95, "rayon": 3000, "couleur": "#08306b"}
            ]
        },
        "Lac des Commissaires": {
            "lat": 47.78, "lon": -72.23, "zoom": 11, "max_depth": 155,
            "description": "Lac en longueur structuré par une faille tectonique majeure et des tombants abyssaux.",
            "isobathes": [
                {"prof": 20, "desc": "Banquette littorale rocheuse", "lat": 47.82, "lon": -72.25, "rayon": 5000, "couleur": "#c6dbef"},
                {"prof": 60, "desc": "Pente abrupte / Tombant", "lat": 47.80, "lon": -72.24, "rayon": 3500, "couleur": "#9ecae1"},
                {"prof": 100, "desc": "Fosse profonde intermédiaire", "lat": 47.78, "lon": -72.23, "rayon": 2000, "couleur": "#4292c6"},
                {"prof": 155, "desc": "Fosse maximale (Refuge à Touladi)", "lat": 47.76, "lon": -72.22, "rayon": 900, "couleur": "#08306b"}
            ]
        },
        "Lac Kénogami": {
            "lat": 48.33, "lon": -71.45, "zoom": 11, "max_depth": 115,
            "description": "Système de lacs encaissés aux bras multiples et chenaux profonds.",
            "isobathes": [
                {"prof": 15, "desc": "Seuils et rétrécissements", "lat": 48.37, "lon": -71.52, "rayon": 6000, "couleur": "#c6dbef"},
                {"prof": 40, "desc": "Chenaux secondaires", "lat": 48.34, "lon": -71.48, "rayon": 4000, "couleur": "#9ecae1"},
                {"prof": 80, "desc": "Fosses structurées", "lat": 48.32, "lon": -71.44, "rayon": 2500, "couleur": "#4292c6"},
                {"prof": 115, "desc": "Grande Fosse Kénogami", "lat": 48.30, "lon": -71.41, "rayon": 1200, "couleur": "#08306b"}
            ]
        }
    }

lacs_db = load_bathymetry_data()

st.title("🌊 Cartographie Vectorielle & Lignes d'Isobathes")
st.markdown("Visualisation des courbes de niveau sous-marines et des paliers de profondeur pour optimiser vos repérages de pêche.")

# Sélection du lac
choix_lac = st.selectbox("Sélectionnez un plan d'eau :", list(lacs_db.keys()))
info_lac = lacs_db[choix_lac]

st.info(f"**Description du profil :** {info_lac['description']} (Profondeur max de référence : **{info_lac['max_depth']} m**)")

# Initialisation de la carte Folium avec OpenStreetMap standard (sans message d'erreur d'API)
m = folium.Map(
    location=[info_lac["lat"], info_lac["lon"]], 
    zoom_start=info_lac["zoom"], 
    tiles="OpenStreetMap"
)

# Ajout des courbes de niveau isobathes étalées sur la superficie du lac
for iso in info_lac["isobathes"]:
    folium.Circle(
        location=[iso["lat"], iso["lon"]],
        radius=iso["rayon"],
        color=iso["couleur"],
        weight=2,
        fill=True,
        fill_color=iso["couleur"],
        fill_opacity=0.35,
        popup=f"<b>Courbe d'isobathe : {iso['prof']} m</b><br>{iso['desc']}",
        tooltip=f"Niveau : {iso['prof']} mètres"
    ).add_to(m)

# Marqueur central de la fosse maximale
folium.Marker(
    [info_lac["lat"], info_lac["lon"]],
    popup=f"<b>{choix_lac}</b><br>Fosse Maximale : {info_lac['max_depth']}m",
    icon=folium.Icon(color="red", icon="flag")
).add_to(m)

# Affichage de la carte interactive dans Streamlit
st.subheader(f"🗺️ Carte des Isobathes et Paliers - {choix_lac}")
st.markdown("💡 *Légende : Les zones bleues concentriques indiquent les paliers de profondeur de la cuvette (du bleu pâle au bleu foncé pour les fosses). Cliquez dessus pour les détails.*")
st_folium(m, width=1100, height=600)

# Tableau technique des isobathes
st.subheader("📊 Tableau d'Échelonnement des Paliers de Pêche")
df_iso = pd.DataFrame(info_lac["isobathes"])[["prof", "desc"]]
df_iso.columns = ["Profondeur (m)", "Caractéristique du Fond"]
st.dataframe(df_iso, use_container_width=True)
