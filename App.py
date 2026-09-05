import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# Configuration de la page
st.set_page_config(
    page_title="Cartographie Bathymétrique - Pêche Québec",
    page_icon="🗺️",
    layout="wide"
)

# Données des lacs avec coordonnées géographiques et points stratégiques
@st.cache_data
def load_lakes_data():
    data = [
        {
            "Nom": "Lac-Saint-Jean (Bassin Central & Fosses)",
            "lat": 48.55,
            "lon": -72.25,
            "Profondeur_Max": 63,
            "Zoom": 10,
            "Description": "Fosses profondes de 60m+ et plateaux sablonneux. Zones clés pour l'ouananiche et le doré.",
            "Points_Strategiques": [
                {"nom": "Fosse Principale Ouest", "lat": 48.62, "lon": -72.40, "prof": "60m+", "type": "Fosse pélagique"},
                {"nom": "Haut-fond de Décharge", "lat": 48.50, "lon": -71.85, "prof": "12m", "type": "Barre de sable et courant"},
                {"nom": "Secteur Embouchure Rivière", "lat": 48.68, "lon": -71.95, "prof": "8m", "type": "Zone d'alimentation"}
            ]
        },
        {
            "Nom": "Lac des Commissaires (Secteur Ouest)",
            "lat": 47.78,
            "lon": -72.23,
            "Profondeur_Max": 155,
            "Zoom": 11,
            "Description": "Lac profond en longueur avec de spectaculaires tombants rocheux et failles de 155m.",
            "Points_Strategiques": [
                {"nom": "Fosse Profonde Nord", "lat": 47.85, "lon": -72.28, "prof": "155m", "type": "Fosse majeure (Touladi)"},
                {"nom": "Tombant Rocheux Est", "lat": 47.75, "lon": -72.18, "prof": "25m", "type": "Cassure abrupte"}
            ]
        },
        {
            "Nom": "Lac Kénogami",
            "lat": 48.33,
            "lon": -71.45,
            "Profondeur_Max": 115,
            "Zoom": 11,
            "Description": "Lac aux bras multiples, chenaux étroits et fosses profondes structurées.",
            "Points_Strategiques": [
                {"nom": "Grande Fosse Kénogami", "lat": 48.35, "lon": -71.50, "prof": "115m", "type": "Fosse profonde"},
                {"nom": "Seuil et Salines", "lat": 48.30, "lon": -71.40, "prof": "15m", "type": "Haut-fond rocheux"}
            ]
        }
    ]
    return data

lacs_data = load_lakes_data()

st.title("🗺️ Carte Interactive & Bathymétrie Stratégique")
st.markdown("Visualisez les emplacements précis, les fosses et les profondeurs maximales pour cibler vos zones de pêche.")

# Sélection du lac dans l'application
noms_lacs = [lac["Nom"] for lac in lacs_data]
lac_selection = st.selectbox("Sélectionnez un plan d'eau à cartographier :", noms_lacs)

# Récupération des données du lac choisi
lac_info = next(lac for lac in lacs_data if lac["Nom"] == lac_selection)

col1, col2, col3 = st.columns(3)
col1.metric("Profondeur Maximale", f"{lac_info['Profondeur_Max']} m")
col2.metric("Type de structure", "Fosses & Tombants")
col3.metric("Statut", "Open Data / Historique 1961")

st.markdown(f"**Description du secteur :** {lac_info['Description']}")

# Création de la carte Folium (style Google Maps / Topographique)
m = folium.Map(location=[lac_info["lat"], lac_info["lon"]], zoom_start=lac_info["Zoom"], tiles="OpenStreetMap")

# Ajout d'un marqueur central pour le lac
folium.Marker(
    [lac_info["lat"], lac_info["lon"]],
    popup=lac_info["Nom"],
    tooltip=lac_info["Nom"],
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(m)

# Ajout des points stratégiques de pêche (fosses, hauts-fonds)
for pt in lac_info["Points_Strategiques"]:
    folium.CircleMarker(
        location=[pt["lat"], pt["lon"]],
        radius=10,
        color="red",
        fill=True,
        fill_color="orange",
        fill_opacity=0.7,
        popup=f"<b>{pt['nom']}</b><br>Profondeur: {pt['prof']}<br>Type: {pt['type']}",
        tooltip=f"{pt['nom']} ({pt['prof']})"
    ).add_to(m)

# Affichage de la carte interactive dans Streamlit
st.subheader("📍 Carte des Spots Stratégiques (Cliquez sur les points rouges)")
st_folium(m, width=1100, height=550)

# Tableau récapitulatif des spots pour consultation rapide
st.subheader("🎯 Coordonnées et Profondeurs des Spots Clés")
df_spots = pd.DataFrame(lac_info["Points_Strategiques"])
st.dataframe(df_spots, use_container_width=True)
