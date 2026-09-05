import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Bathymétrie des Lacs du Québec",
    page_icon="🗺️",
    layout="wide"
)

# Données intégrées des lacs (incluant le Lac-Saint-Jean et archives 1961)
@st.cache_data
def load_lakes_data():
    data = [
        {
            "Nom": "Lac-Saint-Jean",
            "Superficie (km²)": 1053,
            "Profondeur Max (m)": 63,
            "Profondeur Moyenne (m)": 11,
            "Contexte Historique": "Levés et cartes de référence (dont archives 1961 et cartographie hydrographique)",
            "Espèces Cibles": "Ouananiche, Doré jaune, Grand Corégone, Brochet",
            "Secteurs Clés": "Bassins profonds centraux (jusqu'à 60m+), hauts-fonds sableux, embouchures de rivières",
            "lat": 48.55,
            "lon": -72.25
        },
        {
            "Nom": "Lac des Commissaires (Lac St-Jean Ouest)",
            "Superficie (km²)": 45,
            "Profondeur Max (m)": 155,
            "Profondeur Moyenne (m)": 28,
            "Contexte Historique": "Cartes bathymétriques historiques (Fonds BAnQ / Archives 1961)",
            "Espèces Cibles": "Touladi, Ouananiche, Brochet",
            "Secteurs Clés": "Fosses profondes et tombants rocheux",
            "lat": 47.78,
            "lon": -72.23
        },
        {
            "Nom": "Lac Kénogami",
            "Superficie (km²)": 52,
            "Profondeur Max (m)": 115,
            "Profondeur Moyenne (m)": 20,
            "Contexte Historique": "Réseau hydrographique régional Saguenay–Lac-Saint-Jean",
            "Espèces Cibles": "Ouananiche, Doré, Perchaude",
            "Secteurs Clés": "Salines, chenaux étroits et fosses structurées",
            "lat": 48.33,
            "lon": -71.45
        }
    ]
    return pd.DataFrame(data)

df_lacs = load_lakes_data()

# En-titre de l'application
st.title("🌊 Bathymétrie des Lacs du Québec")
st.markdown("Explorez les données bathymétriques, les structures sous-marines et les repères historiques (cartes de 1961) pour les pêcheurs amateurs.")

# Barre latérale de navigation
st.sidebar.header("Navigation")
selection_mode = st.sidebar.radio("Mode d'affichage", ["Explorateur de Lacs", "Carte & Coordonnées", "À propos / Open Data"])

if selection_mode == "Explorateur de Lacs":
    st.subheader("Sélectionnez un plan d'eau")
    lac_selection = st.selectbox("Choisissez un lac :", df_lacs["Nom"].tolist())
    
    lac_info = df_lacs[df_lacs["Nom"] == lac_selection].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Superficie", f"{lac_info['Superficie (km²)]']} km²")
    col2.metric("Profondeur Max", f"{lac_info['Profondeur Max (m)]']} m")
    col3.metric("Profondeur Moyenne", f"{lac_info['Profondeur Moyenne (m)]']} m")
    
    st.markdown("---")
    st.markdown(f"**Contexte et Archives :** {lac_info['Contexte Historique']}")
    st.markdown(f"**Espèces Cibles :** {lac_info['Espèces Cibles']}")
    st.markdown(f"**Secteurs et Structures Clés :** {lac_info['Secteurs Clés']}")
    
    # Simulation d'un profil bathymétrique basé sur les profondeurs de référence
    st.subheader("Profil Bathymétrique Théorique / Repères de Profondeur")
    distances = np.linspace(0, 10, 50)
    profondeurs = lac_info['Profondeur Max (m)'] * (1 - np.exp(-distances/3)) + np.random.normal(0, 0.5, 50)
    profondeurs = np.clip(profondeurs, 0, lac_info['Profondeur Max (m)'])
    
    chart_data = pd.DataFrame({
        "Distance depuis la rive (km)": distances,
        "Profondeur (m)": profondeurs
    })
    st.line_chart(chart_data.set_index("Distance depuis la rive (km)"))

elif selection_mode == "Carte & Coordonnées":
    st.subheader("Cartographie et Localisation des Plans d'Eau")
    st.map(df_lacs, latitude='lat', longitude='lon', size=50, color='#2c4c3b')
    st.dataframe(df_lacs[["Nom", "Superficie (km²)", "Profondeur Max (m)", "Profondeur Moyenne (m)"]])

else:
    st.subheader("À propos de l'initiative Open Data")
    st.write("""
    Cette application est conçue pour offrir une alternative libre, gratuite et solidaire aux cartes commerciales payantes 
    (Garmin, Navionics) pour les pêcheurs amateurs. En s'appuyant sur les levés historiques (notamment les campagnes des années 1960) 
    et les répertoires publics (BAnQ, Données Québec), l'objectif est de démocratiser l'accès aux connaissances hydrographiques.
    """)
    
