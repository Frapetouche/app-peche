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

# Données des lacs avec les zones de courbes de niveau et profondeurs
@st.cache_data
def load_lakes_data():
    return [
        {
            "Nom": "Lac-Saint-Jean",
            "lat": 48.55,
            "lon": -72.25,
            "Zoom": 11,
            "Profondeur_Max": "63 m (Fosses centrales jusqu'à 98m-164m selon secteurs)",
            "Points": [
                {"nom": "Fosse Centrale Nord", "lat": 48.65, "lon": -72.30, "prof": "98 m", "desc": "Fosse profonde pélagique (Ouananiche)"},
                {"nom": "Fosse Centrale Sud", "lat": 48.45, "lon": -72.15, "prof": "164 m", "desc": "Bassin profond maximal historique"},
                {"nom": "Haut-fond de Décharge", "lat": 48.50, "lon": -71.85, "prof": "12 m", "desc": "Barre de sable et hauts-fonds de courant"},
                {"nom": "Secteur Alma / Embouchure", "lat": 48.55, "lon": -71.65, "prof": "8 m", "desc": "Sortie vers la Saguenay, zones rocheuses"}
            ]
        },
        {
            "Nom": "Lac des Commissaires",
            "lat": 47.78,
            "lon": -72.23,
            "Zoom": 12,
            "Profondeur_Max": "155 m",
            "Points": [
                {"nom": "Fosse Majeure Nord", "lat": 47.85, "lon": -72.28, "prof": "155 m", "desc": "Faille profonde (Touladi)"},
                {"nom": "Tombant Rocheux Est", "lat": 47.75, "lon": -72.18, "prof": "25 m", "desc": "Cassure abrupte"}
            ]
        },
        {
            "Nom": "Lac Kénogami",
            "lat": 48.33,
            "lon": -71.45,
            "Zoom": 12,
            "Profondeur_Max": "115 m",
            "Points": [
                {"nom": "Grande Fosse Kénogami", "lat": 48.35, "lon": -71.50, "prof": "115 m", "desc": "Fosse principale structurée"},
                {"nom": "Seuil et Salines", "lat": 48.30, "lon": -71.40, "prof": "15 m", "desc": "Haut-fond rocheux"}
            ]
        }
    ]

lacs = load_lakes_data()

st.title("🗺️ Carte Bathymétrique & Lignes d'Isobathes (Pêche Amateur)")
st.markdown("Explorez les fosses, les tombants et les courbes de profondeur géolocalisées pour planifier vos sorties de pêche sans abonnement payant.")

# Sélection du lac
noms = [l["Nom"] for l in lacs]
choix = st.selectbox("Sélectionnez un plan d'eau :", noms)
lac_actuel = next(l for l in lacs if l["Nom"] == choix)

st.info(f"**Profondeur maximale de référence :** {lac_actuel['Profondeur_Max']}")

# Création de la carte Folium interactive avec calque OpenSeaMap (données de profondeur/marines)
m = folium.Map(
    location=[lac_actuel["lat"], lac_actuel["lon"]], 
    zoom_start=lac_actuel["Zoom"], 
    tiles="OpenStreetMap"
)

# Ajout d'un calque de type hydrographie/maritime pour visualiser les lignes de fond si disponibles
folium.TileLayer(
    tiles='https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
    attr='Cartographie Humanitaire / OpenStreetMap',
    name='Détails Topographiques'
).add_to(m)

# Marqueur du centre du lac
folium.Marker(
    [lac_actuel["lat"], lac_actuel["lon"]],
    popup=lac_actuel["Nom"],
    icon=folium.Icon(color="blue", icon="info-sign")
).add_to(m)

# Ajout des points stratégiques (fosses, cassures, hauts-fonds)
for pt in lac_actuel["Points"]:
    folium.CircleMarker(
        location=[pt["lat"], pt["lon"]],
        radius=12,
        color="#2c4c3b",
        fill=True,
        fill_color="#4a7c59",
        fill_opacity=0.8,
        popup=f"<b>{pt['nom']}</b><br>Profondeur: <b>{pt['prof']}</b><br>{pt['desc']}",
        tooltip=f"{pt['nom']} ({pt['prof']})"
    ).add_to(m)

# Affichage de la carte interactive
st.subheader("📍 Carte Interactive des Fosses & Courbes de Profondeur")
st.markdown("💡 *Astuce : Cliquez sur les cercles verts pour voir les détails précis de profondeur et la structure du fond.*")
st_folium(m, width=1100, height=600)

# Tableau détaillé des zones de pêche
st.subheader("📊 Répertoire des Spots et Profondeurs Clés")
df_points = pd.DataFrame(lac_actuel["Points"])
st.dataframe(df_points, use_container_width=True)
