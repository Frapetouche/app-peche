import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# Configuration de la page
st.set_page_config(
    page_title="Modélisation Bathymétrique & Isobathes - Québec",
    page_icon="🗺️",
    layout="wide"
)

# Données structurées des lacs et de leurs cuvettes basées sur les archives de référence
@st.cache_data
def load_bathymetry_data():
    return {
        "Lac-Saint-Jean": {
            "lat": 48.55, "lon": -72.25, "zoom": 10, "max_depth": 63,
            "description": "Immense cuvette glaciaire, présence de fosses profondes centrales et de hauts-fonds sableux.",
            "isobathes": [
                {"prof": 10, "desc": "Plateau côtier et herbiers", "lat_off": 0.05, "lon_off": 0.08},
                {"prof": 25, "desc": "Pente intermédiaire de transition", "lat_off": 0.03, "lon_off": 0.05},
                {"prof": 45, "desc": "Talus et fosses secondaires", "lat_off": 0.015, "lon_off": 0.025},
                {"prof": 63, "desc": "Bassin profond maximal (Fosse centrale)", "lat_off": 0.0, "lon_off": 0.0}
            ]
        },
        "Lac des Commissaires": {
            "lat": 47.78, "lon": -72.23, "zoom": 11, "max_depth": 155,
            "description": "Lac en longueur structuré par une faille tectonique majeure et des tombants abyssaux.",
            "isobathes": [
                {"prof": 20, "desc": "Banquette littorale rocheuse", "lat_off": 0.03, "lon_off": 0.02},
                {"prof": 60, "desc": "Pente abrupte / Tombant", "lat_off": 0.02, "lon_off": 0.012},
                {"prof": 100, "desc": "Fosse profonde intermédiaire", "lat_off": 0.01, "lon_off": 0.006},
                {"prof": 155, "desc": "Fosse maximale (Refuge à Touladi)", "lat_off": 0.0, "lon_off": 0.0}
            ]
        },
        "Lac Kénogami": {
            "lat": 48.33, "lon": -71.45, "zoom": 11, "max_depth": 115,
            "description": "Système de lacs encaissés aux bras multiples et chenaux profonds.",
            "isobathes": [
                {"prof": 15, "desc": "Seuils et rétrécissements", "lat_off": 0.04, "lon_off": 0.05},
                {"prof": 40, "desc": "Chenaux secondaires", "lat_off": 0.025, "lon_off": 0.03},
                {"prof": 80, "desc": "Fosses structurées", "lat_off": 0.01, "lon_off": 0.015},
                {"prof": 115, "desc": "Grande Fosse Kénogami", "lat_off": 0.0, "lon_off": 0.0}
            ]
        }
    }

lacs_db = load_bathymetry_data()

st.title("🌊 Cartographie Vectorielle & Lignes d'Isobathes (Archives Historiques)")
st.markdown("Visualisation des courbes de niveau sous-marines et des paliers de profondeur pour optimiser vos repérages de pêche.")

# Sélection du lac
choix_lac = st.selectbox("Sélectionnez un plan d'eau :", list(lacs_db.keys()))
info_lac = lacs_db[choix_lac]

st.info(f"**Description du profil :** {info_lac['description']} (Profondeur max de référence : **{info_lac['max_depth']} m**)")

# Initialisation de la carte Folium
m = folium.Map(
    location=[info_lac["lat"], info_lac["lon"]], 
    zoom_start=info_lac["zoom"], 
    tiles="CartoDB positron"
)

# Ajout dynamique des cercles concentriques représentant les lignes de niveaux isobathes
colors = ["#c6dbef", "#9ecae1", "#4292c6", "#08306b"]

for idx, iso in enumerate(info_lac["isobathes"]):
    rayon_metres = max(500, int((info_lac['max_depth'] - iso['prof'] + 20) * 45))
    
    lat_pos = info_lac["lat"] + iso["lat_off"]
    lon_pos = info_lac["lon"] + iso["lon_off"]
    
    couleur_cercle = colors[idx % len(colors)]
    
    folium.Circle(
        location=[lat_pos, lon_pos],
        radius=rayon_metres,
        color=couleur_cercle,
        weight=2,
        fill=True,
        fill_color=couleur_cercle,
        fill_opacity=0.25,
        popup=f"<b>Isobathe / Courbe : {iso['prof']} m</b><br>{iso['desc']}",
        tooltip=f"Courbe de niveau : {iso['prof']} mètres"
    ).add_to(m)

# Marqueur central de la cuvette profonde
folium.Marker(
    [info_lac["lat"], info_lac["lon"]],
    popup=f"<b>{choix_lac}</b><br>Fosse Maximale : {info_lac['max_depth']}m",
    icon=folium.Icon(color="red", icon="flag")
).add_to(m)

# Affichage de la carte interactive dans Streamlit
st.subheader(f"🗺️ Carte des Isobathes et Paliers - {choix_lac}")
st.markdown("💡 *Légende des anneaux : Les cercles concentriques simulent les lignes de niveaux bathymétriques de la cuvette. Cliquez sur chaque anneau pour voir la profondeur associée.*")
st_folium(m, width=1100, height=600)

# Tableau technique des isobathes
st.subheader("📊 Tableau d'Échelonnement des Paliers de Pêche")
df_iso = pd.DataFrame(info_lac["isobathes"])[["prof", "desc"]]
df_iso.columns = ["Profondeur (m)", "Caractéristique du Fond"]
st.dataframe(df_iso, use_container_width=True)
