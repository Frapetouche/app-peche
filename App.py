    import streamlit as st
import pandas as pd
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Bathymétrie des Lacs du Québec",
    page_icon="🗺️",
    layout="wide"
)

# Données des lacs avec repères bathymétriques
@st.cache_data
def load_lakes_data():
    data = [
        {
            "Nom": "Lac-Saint-Jean",
            "Superficie": 1053,
            "Profondeur_Max": 63,
            "Profondeur_Moyenne": 11,
            "Contexte_Historique": "Levés et cartes de référence (dont archives 1961 et cartographie hydrographique)",
            "Especes_Cibles": "Ouananiche, Doré jaune, Grand Corégone, Brochet",
            "Secteurs_Cles": "Bassins profonds centraux (jusqu'à 60m+), hauts-fonds sableux, embouchures de rivières",
            "lat": 48.55,
            "lon": -72.25
        },
        {
            "Nom": "Lac des Commissaires (Lac St-Jean Ouest)",
            "Superficie": 45,
            "Profondeur_Max": 155,
            "Profondeur_Moyenne": 28,
            "Contexte_Historique": "Cartes bathymétriques historiques (Fonds BAnQ / Archives 1961)",
            "Especes_Cibles": "Touladi, Ouananiche, Brochet",
            "Secteurs_Cles": "Fosses profondes et tombants rocheux",
            "lat": 47.78,
            "lon": -72.23
        },
        {
            "Nom": "Lac Kénogami",
            "Superficie": 52,
            "Profondeur_Max": 115,
            "Profondeur_Moyenne": 20,
            "Contexte_Historique": "Réseau hydrographique régional Saguenay–Lac-Saint-Jean",
            "Especes_Cibles": "Ouananiche, Doré, Perchaude",
            "Secteurs_Cles": "Salines, chenaux étroits et fosses structurées",
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
    col1.metric("Superficie", f"{lac_info['Superficie']} km²")
    col2.metric("Profondeur Max", f"{lac_info['Profondeur_Max']} m")
    col3.metric("Profondeur Moyenne", f"{lac_info['Profondeur_Moyenne']} m")
    
    st.markdown("---")
    st.markdown(f"**Contexte et Archives :** {lac_info['Contexte_Historique']}")
    st.markdown(f"**Espèces Cibles :** {lac_info['Especes_Cibles']}")
    st.markdown(f"**Secteurs et Structures Clés :** {lac_info['Secteurs_Cles']}")
    
    # Grille de lignes de courbes de fond (Isobathes tabulaires et graphiques natifs)
    st.subheader("📈 Lignes de Courbes de Fond & Isobathes")
    st.markdown("Échelonnement des profondeurs sous-marines pour identifier les paliers de pêche :")
    
    max_d = lac_info['Profondeur_Max']
    paliers = [round(max_d * p, 1) for p in [0.1, 0.25, 0.5, 0.75, 0.9, 1.0]]
    
    df_isobathes = pd.DataFrame({
        "Niveau d'Isobathe": ["Zone côtière / Haut-fond", "Plateau intermédiaire", "Pente / Tombant", "Fosse secondaire", "Bassin profond maximal", "Fond abattu / Fosse clé"],
        "Profondeur (mètres)": paliers,
        "Stratégie de Pêche Recommandée": [
            "Lancer aux abords des herbiers et pointes rocheuses",
            "Recherche de structures et cassures (Doré / Ouananiche)",
            "Pêche à la traîne le long du talus",
            "Migration des grands salmonidés",
            "Zone pélagique profonde",
            "Fonds de cuvette (refuge thermique)"
        ]
    })
    
    st.dataframe(df_isobathes, use_container_width=True)
    
    # Graphique de profil bathymétrique natif Streamlit
    st.subheader("Profil Bathymétrique en Coupe Transversale")
    distances = np.linspace(0, 10, 50)
    profondeurs = max_d * (1 - np.exp(-distances/3))
    
    chart_data = pd.DataFrame({
        "Distance depuis la rive (km)": distances,
        "Profondeur (m)": profondeurs
    })
    st.line_chart(chart_data.set_index("Distance depuis la rive (km)"))

elif selection_mode == "Carte & Coordonnées":
    st.subheader("Cartographie et Localisation des Plans d'Eau")
    st.map(df_lacs, latitude='lat', longitude='lon', size=50, color='#2c4c3b')
    st.dataframe(df_lacs[["Nom", "Superficie", "Profondeur_Max", "Profondeur_Moyenne"]])

else:
    st.subheader("À propos de l'initiative Open Data")
    st.write("""
    Cette application est conçue pour offrir une alternative libre, gratuite et solidaire aux cartes commerciales payantes 
    (Garmin, Navionics) pour les pêcheurs amateurs. En s'appuyant sur les levés historiques (notamment les campagnes des années 1960) 
    et les répertoires publics (BAnQ, Données Québec), l'objectif est de démocratiser l'accès aux connaissances hydrographiques.
    """)
    
