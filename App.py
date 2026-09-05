import streamlit as st
import json
import os
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Pêche 101 - Bathymétrie", layout="wide")

st.title("Pêche 101 - Carte Bathymétrique du Lac Saint-Jean")
st.write("Visualisation des données bathymétriques issues des sources ouvertes.")

# 1. Charger le fichier GeoJSON depuis le dépôt
@st.cache_data
def load_geojson(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# Cherche automatiquement un fichier .geojson dans le dossier
geojson_files = [f for f in os.listdir('.') if f.endswith('.geojson')]
geojson_data = load_geojson(geojson_files[0]) if geojson_files else None

# 2. Créer la carte centrée sur le Lac Saint-Jean
m = folium.Map(location=[48.55, -72.0], zoom_start=10, tiles="CartoDB positron")

# 3. Ajouter les données sur la carte si le fichier est présent
if geojson_data:
    folium.GeoJson(
        geojson_data,
        name="Bathymétrie",
        style_function=lambda x: {'color': '#1f78b4', 'weight': 1.5, 'fillOpacity': 0.4}
    ).add_to(m)
    st.success(f"Fichier bathymétrique chargé avec succès !")
else:
    st.warning("⚠️ Aucun fichier .geojson trouvé dans le dépôt GitHub. Ajoute ton fichier de données à la racine du projet.")

# 4. Afficher la carte dans l'application
st_folium(m, width=1000, height=600)

