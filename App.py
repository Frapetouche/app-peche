import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Pêche 101 - Bathymétrie Lac Saint-Jean", layout="wide")

st.title("Pêche 101 - Carte Bathymétrique du Lac Saint-Jean")
st.write("Visualisation des zones de pêche et repères bathymétriques principaux.")

# 1. Création de la carte avec un fond OpenStreetMap libre (sans clé API)
m = folium.Map(location=[48.55, -72.0], zoom_start=10, tiles="OpenStreetMap")

# 2. Données des repères et fosses clés du Lac Saint-Jean
points_interet = [
    [48.674, -71.642, "Décharge (Rivière Saguenay / Alma)", 15],
    [48.783, -72.350, "Secteur Mistassini", 12],
    [48.633, -72.583, "Secteur Péribonka", 18],
    [48.483, -71.833, "Secteur Chambord", 22],
    [48.580, -72.000, "Centre du Lac Saint-Jean (Zone profonde)", 35],
    [48.500, -72.250, "Secteur Saint-Gédéon / Pointe Taillon", 10]
]

# 3. Ajout des marqueurs sur la carte
for lat, lon, nom, prof in points_interet:
    folium.CircleMarker(
        location=[lat, lon],
        radius=max(6, prof / 1.2),
        color='#1f78b4',
        fill=True,
        fill_color='#33a02c',
        fill_opacity=0.7,
        popup=f"<b>{nom}</b><br>Profondeur estimée : {prof}m",
        tooltip=nom
    ).add_to(m)

# 4. Affichage de la carte dans Streamlit
st_folium(m, width=1000, height=600)

