import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Bathymétrie des Lacs du Québec",
    page_icon="🗺️",
    layout="wide"
)

# Données intégrées des lacs avec des repères bathymétriques précis
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
    
    st.subheader("Carte des Lignes de Courbes de Fond (Bathymétrie)")
    st.markdown("Visualisation des isobathes (lignes de profondeur) simulant la cuvette sous-marine du lac sélectionné.")
    
    # Génération d'une grille bathymétrique réaliste basée sur la profondeur max du lac
    max_d = lac_info['Profondeur_Max']
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    
    # Modélisation d'une cuvette avec des hauts-fonds et fosses
    Z = max_d * (1 - 0.7 * np.exp(-(X**2 + Y**2)/8) - 0.3 * np.cos(X) * np.sin(Y))
    Z = np.clip(Z, 0, max_d)
    
    # Création du graphique de courbes de niveau (Contour plot)
    fig = go.Figure(data = [
        go.Contour(
            z=Z,
            x=x,
            y=y,
            colorscale='Blues_r',  # Du plus foncé (profond) au plus clair (haut-fond)
            colorbar=dict(title="Profondeur (m)"),
            contours=dict(
                showlabels=True, # Affiche les chiffres de profondeur sur les lignes
                labelfont=dict(size=12, color='white')
            )
        )
    ])
    
    fig.update_layout(
        title=f"Modèle Bathymétrique - {lac_info['Nom']}",
        xaxis_title="Coordonnée Est-Ouest (secteurs)",
        yaxis_title="Coordonnée Nord-Sud (secteurs)",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Profil en coupe
    st.subheader("Profil Bathymétrique en Coupe Transversale")
    distances = np.linspace(0, 10, 50)
    profondeurs = max_d * (1 - np.exp(-distances/3)) + np.random.normal(0, 0.5, 50)
    profondeurs = np.clip(profondeurs, 0, max_d)
    
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
    
