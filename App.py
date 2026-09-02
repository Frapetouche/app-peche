import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Guide Pêche Québec Pro", layout="wide", initial_sidebar_state="expanded")

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
<style>
    .main { background-color: #0f172a; color: #f1f5f9; }
    .card { background-color: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 15px; }
    .ice-card { background-color: #082f49; padding: 20px; border-radius: 10px; border: 1px solid #0369a1; margin-bottom: 15px; }
    .alert-ice { background-color: #451a03; padding: 15px; border-radius: 8px; border: 1px solid #b45309; color: #fde68a; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DONNÉES LOCALE VÉRIFIÉE (QUÉBEC) ---
SPOTS_QUEBEC = {
    "Saguenay - Fjord (Village de pêche Baie des Ha! Ha!)": {
        "lat": 48.3332, "lon": -70.8833, "zoom": 12,
        "reglement": "Fjord du Saguenay (Pêche blanche) - Aucun permis de pêche générale requis sur les glaces du Fjord, mais quotas stricts par espèce.",
        "especes": ["Sébaste", "Morue de l'Atlantique", "Turbot (Flétan du Groenland)", "Éperlan arc-en-ciel"],
        "conseil": "Pêche en verticale à l'intérieur des cabanes chauffées avec des dandinettes lestées et des vers ou lanières de poisson."
    },
    "Lac Saint-Jean (Pointe-Taillon / Saint-Gédéon)": {
        "lat": 48.5500, "lon": -71.7333, "zoom": 11,
        "reglement": "Zone 27 - Permis de pêche sportive d'eau douce obligatoire, respect des dates limites d'utilisation des cabanes.",
        "especes": ["Doré jaune", "Perchaude", "Lotte"],
        "conseil": "Utiliser des brimbales (lignes dormantes) calées avec des menés vivants sur les rebords de hauts-fonds."
    }
}

# --- NAVIGATION PRINCIPALE (ONGLETS) ---
onglet_principal, onglet_tutos, onglet_glace = st.tabs([
    "🗺️ Cartographie & Été", 
    "🎥 Montages & Techniques", 
    "❄️ Pêche Blanche (Glace)"
])

with onglet_principal:
    with st.sidebar:
        st.markdown("## 🎣 Paramètres Pêche QC")
        plan_eau = st.selectbox("Choisir un plan d'eau", list(SPOTS_QUEBEC.keys()))
        spot_info = SPOTS_QUEBEC[plan_eau]
        LAT, LON, ZOOM = spot_info["lat"], spot_info["lon"], spot_info["zoom"]
        
        st.markdown("---")
        st.markdown("### 🛠️ Outils Pro")
        mode_carte = st.radio("Fond de carte", ["Satellite HD", "Topographie"])

    col_carte, col_panneau = st.columns([1.5, 1])

    with col_carte:
        st.markdown(f"### 🗺️ Zone : {plan_eau}")
        m = folium.Map(location=[LAT, LON], zoom_start=ZOOM, control_scale=True, tiles=None)
        
        if mode_carte == "Satellite HD":
            folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri Satellite').add_to(m)
        else:
            folium.TileLayer(tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', attr='OpenTopoMap').add_to(m)

        folium.Marker(location=[LAT, LON], tooltip="Structure Clé", icon=folium.Icon(color="blue", icon="anchor", prefix="fa")).add_to(m)
        st_folium(m, width="100%", height=500, returned_objects=[], key="map_v_ete")

    with col_panneau:
        st.markdown("### 📋 Stratégie & Réglementation")
        st.markdown(f"""
        <div class="card">
            <h4 style="color: #38bdf8; margin-top:0;">Espèces cibles</h4>
            <p><b>{', '.join(spot_info['especes'])}</b></p>
            <h4 style="color: #fbbf24;">Réglementation Québec</h4>
            <p style="font-size: 13px; color: #cbd5e1;">{spot_info['reglement']}</p>
            <h4 style="color: #4ade80;">Conseil tactique</h4>
            <p style="font-size: 13px; color: #cbd5e1;">{spot_info['conseil']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<a href="https://webapp.navionics.com/?lang=en#boating@13@{LAT},{LON}" target="_blank" style="background-color: #004b87; color: white; padding: 10px 15px; border-radius: 6px; text-decoration: none; font-weight: bold; display:inline-block; text-align:center; width:100%;">🗺️ Ouvrir la zone sur Navionics Web</a>', unsafe_allow_html=True)

with onglet_tutos:
    st.markdown("## 📚 Académie Pêche 101 : Montages & Techniques")
    col_tuto1, col_tuto2, col_tuto3 = st.columns(3)
    
    with col_tuto1:
        st.markdown("""<div class="card"><h3 style="color: #38bdf8;">🪢 Nœud Albright / FG</h3><p style="font-size: 13px;">Raccord tresse-fluorocarbone ultra résistant.</p></div>""", unsafe_allow_html=True)
    with col_tuto2:
        st.markdown("""<div class="card"><h3 style="color: #fbbf24;">🎯 Jig & Leurre Souple</h3><p style="font-size: 13px;">Technique de grattage de fond pour le doré et le bar rayé.</p></div>""", unsafe_allow_html=True)
    with col_tuto3:
        st.markdown("""<div class="card"><h3 style="color: #4ade80;">🎣 Traîne lente</h3><p style="font-size: 13px;">Réglage des planches planantes pour salmonidés.</p></div>""", unsafe_allow_html=True)

with onglet_glace:
    st.markdown("## ❄️ Pêche Blanche & Sécurité Hivernale")
    st.markdown("Données spécifiques au Fjord du Saguenay et plans d'eau intérieurs : épaisseur de glace, équipements et espèces cibles.")
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("""
        <div class="ice-card">
            <h3 style="color: #38bdf8;">📏 Guide d'Épaisseur de Glace (Sécurité)</h3>
            <p style="font-size: 13px; color: #e2e8f0;">Vérifiez toujours l'épaisseur avant de vous aventurer sur la glace :</p>
            <ul style="font-size: 13px; color: #cbd5e1;">
                <li><b>10 cm (4 pouces) :</b> Sécuritaire pour la marche à pied (pêcheur solo).</li>
                <li><b>20 cm (8 pouces) :</b> Motoneige ou VTT.</li>
                <li><b>30 cm (12 pouces) :</b> Automobile ou petit camion léger.</li>
                <li><b>38 cm+ :</b> Véhicule lourd / cabane de pêche complète.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-ice">
            <b>⚠️ Particularité du Fjord :</b> Attention aux mouvements de marées et aux zones de "pied de glace" près des rives qui fragilisent la couverture glacée de manière imprévisible.
        </div>
        """, unsafe_allow_html=True)

    with col_g2:
        st.markdown("""
        <div class="ice-card">
            <h3 style="color: #38bdf8;">🪝 Montages & Espèces du Fjord en Hiver</h3>
            <p style="font-size: 13px; color: #e2e8f0;"><b>1. Pêche au Sébaste et à la Morue :</b> Utilisation de cannes à dandinette courtes et rigides avec des cuillères plombées ou des jigs phosphorescents dans les grands fonds.</p>
            <p style="font-size: 13px; color: #e2e8f0;"><b>2. Pêche à l'éperlan :</b> Lignes ultra-fines à dandinette légère munies de petits vers de mer (Néréis) dans les villages de cabanes.</p>
            <p style="font-size: 13px; color: #e2e8f0;"><b>3. Équipement indispensable :</b> Tarière, cuillère à glace (skimmer), sondeur portable pour repérer les bancs de poissons pélagiques, et crampons de sécurité.</p>
        </div>
        """, unsafe_allow_html=True)
