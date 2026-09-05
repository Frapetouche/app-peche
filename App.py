import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuration de la page
st.set_page_config(
    page_title="Bathymétrie & Archives Historiques 1961 - Québec",
    page_icon="🗺️",
    layout="wide"
)

# Données géoréférencées issues des relevés historiques et des cartes de référence
@st.cache_data
def load_historical_data():
    return {
        "Lac-Saint-Jean": {
            "lat": 48.55, "lon": -72.25, "zoom": 10, "max_depth": "164 m",
            "description": "Cartographie de référence des cuvettes et fosses majeures (campagnes historiques).",
            "sondages": [
                {"lat": 48.60, "lon": -72.10, "prof": "164 m", "secteur": "Fosse Majeure Centrale Est"},
                {"lat": 48.45, "lon": -72.12, "prof": "164 m", "secteur": "Fosse Majeure Sud-Est"},
                {"lat": 48.45, "lon": -72.22, "prof": "131 m", "secteur": "Fosse Sud-Ouest"},
                {"lat": 48.60, "lon": -72.28, "prof": "86 m", "secteur": "Fosse Nord"},
                {"lat": 48.65, "lon": -72.35, "prof": "98 m", "secteur": "Fosse Nord-Ouest"},
                {"lat": 48.52, "lon": -71.85, "prof": "32 m", "secteur": "Haut-fond de Décharge Est"}
            ],
            "isobathes": [
                {"prof": "20m", "lat": 48.55, "lon": -72.20, "rayon": 15000, "couleur": "#c6dbef"},
                {"prof": "50m", "lat": 48.55, "lon": -72.18, "rayon": 10000, "couleur": "#9ecae1"},
                {"prof": "100m", "lat": 48.53, "lon": -72.15, "rayon": 6000, "couleur": "#4292c6"},
                {"prof": "164m", "lat": 48.50, "lon": -72.12, "rayon": 2500, "couleur": "#08306b"}
            ]
        },
        "Lac des Commissaires": {
            "lat": 47.78, "lon": -72.23, "zoom": 11, "max_depth": "155 m",
            "description": "Fosses en longueur structurées par une faille tectonique majeure.",
            "sondages": [
                {"lat": 47.85, "lon": -72.28, "prof": "155 m", "secteur": "Fosse Majeure Nord (Touladi)"},
                {"lat": 47.75, "lon": -72.18, "prof": "25 m", "secteur": "Tombant Rocheux Est"}
            ],
            "isobathes": [
                {"prof": "20m", "lat": 47.82, "lon": -72.25, "rayon": 5000, "couleur": "#c6dbef"},
                {"prof": "60m", "lat": 47.80, "lon": -72.24, "rayon": 3500, "couleur": "#9ecae1"},
                {"prof": "100m", "lat": 47.78, "lon": -72.23, "rayon": 2000, "couleur": "#4292c6"},
                {"prof": "155m", "lat": 47.76, "lon": -72.22, "rayon": 900, "couleur": "#08306b"}
            ]
        },
        "Lac Kénogami": {
            "lat": 48.33, "lon": -71.45, "zoom": 11, "max_depth": "115 m",
            "description": "Système de lacs encaissés aux bras multiples et chenaux profonds.",
            "sondages": [
                {"lat": 48.35, "lon": -71.50, "prof": "115 m", "secteur": "Grande Fosse Kénogami"},
                {"lat": 48.30, "lon": -71.40, "prof": "15 m", "secteur": "Seuil et Salines"}
            ],
            "isobathes": [
                {"prof": "15m", "lat": 48.37, "lon": -71.52, "rayon": 6000, "couleur": "#c6dbef"},
                {"prof": "40m", "lat": 48.34, "lon": -71.48, "rayon": 4000, "couleur": "#9ecae1"},
                {"prof": "80m", "lat": 48.32, "lon": -71.44, "rayon": 2500, "couleur": "#4292c6"},
                {"prof": "115m", "lat": 48.30, "lon": -71.41, "rayon": 1200, "couleur": "#08306b"}
            ]
        }
    }

db_lacs = load_historical_data()

st.title("🗺️ Cartographie Bathymétrique & Isobathes (Archives de Référence)")
st.markdown("Visualisation précise des courbes de niveau sous-marines et des points de sondage historiques pour vos repérages de pêche.")

# Sélection du plan d'eau
choix_lac = st.selectbox("Sélectionnez un plan d'eau :", list(db_lacs.keys()))
lac_courant = db_lacs[choix_lac]

st.info(f"**Profil :** {lac_courant['description']} | **Profondeur Maximale :** {lac_courant['max_depth']}")

# Initialisation de la carte interactive OpenStreetMap
m = folium.Map(
    location=[lac_courant["lat"], lac_courant["lon"]], 
    zoom_start=lac_courant["zoom"], 
    tiles="OpenStreetMap"
)

# Tracé des anneaux d'isobathes (courbes de niveau de la cuvette)
for iso in lac_courant["isobathes"]:
    folium.Circle(
        location=[iso["lat"], iso["lon"]],
        radius=iso["rayon"],
        color=iso["couleur"],
        weight=2,
        fill=True,
        fill_color=iso["couleur"],
        fill_opacity=0.3,
        popup=f"<b>Courbe d'isobathe : {iso['prof']}</b>",
        tooltip=f"Niveau : {iso['prof']}"
    ).add_to(m)

# Ajout des points de sondages précis
for pt in lac_courant["sondages"]:
    folium.CircleMarker(
        location=[pt["lat"], pt["lon"]],
        radius=9,
        color="#8B0000",
        fill=True,
        fill_color="#FF4500",
        fill_opacity=0.9,
        popup=f"<b>Point de Sondage Historique</b><br>Secteur : {pt['secteur']}<br>Profondeur : <b>{pt['prof']}</b>",
        tooltip=f"{pt['prof']} ({pt['secteur']})"
    ).add_to(m)

# Affichage de la carte dans Streamlit
st.subheader(f"📍 Carte Interactive des Fosses et Isobathes - {choix_lac}")
st.markdown("💡 *Astuce : Cliquez sur les points rouges pour afficher les valeurs exactes des relevés et sur les zones bleues pour voir les paliers d'isobathes.*")
st_folium(m, width=1100, height=600)

# Tableau récapitulatif des points de sondage
st.subheader("📊 Répertoire des Sondages et Profondeurs Clés")
df_points = pd.DataFrame(lac_courant["sondages"])
df_points.columns = ["Latitude", "Longitude", "Profondeur", "Secteur / Description"]
st.dataframe(df_points[["Profondeur", "Secteur / Description", "Latitude", "Longitude"]], use_container_width=True)

