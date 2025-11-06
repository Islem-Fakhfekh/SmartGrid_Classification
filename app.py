# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- CONFIGURATION ---
st.set_page_config(page_title="Smart Grid Dashboard", layout="wide")
sns.set_style("whitegrid")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("full_features.csv")
        return df
    except FileNotFoundError:
        st.error("❌ Le fichier full_features.csv est introuvable. Ajoute-le dans ton repo GitHub.")
        return None

df = load_data()

# --- BARRE LATÉRALE ---
st.sidebar.title("⚡ Navigation")
page = st.sidebar.radio("Aller vers :", ["Accueil", "Visualisation", "Clustering", "Analyse énergétique"])

# --- PAGE ACCUEIL ---
if page == "Accueil":
    st.title("🔌 Tableau de bord - Classification des consommateurs d’électricité")
    st.write("""
    Ce tableau de bord permet de :
    - Visualiser les paramètres de consommation énergétique,
    - Explorer les clusters obtenus par K-Means et DBSCAN,
    - Identifier les comportements de consommation et les opportunités d’optimisation énergétique.
    """)
    st.info("Projet Smart Grid 2025-2026 — SUP'COM / SysTIC")

    if df is not None:
        st.metric("Nombre de compteurs", f"{df['LCLid'].nunique()}")
        st.metric("Nombre de mesures totales", f"{len(df):,}")
        st.metric("Nombre de clusters K-Means", f"{df['kmeans_cluster'].nunique()}")
    else:
        st.warning("⚠️ Aucune donnée chargée.")

# --- PAGE VISUALISATION ---
elif page == "Visualisation":
    st.title("📊 Visualisation des paramètres de consommation")
    if df is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Distribution de la consommation annuelle")
            fig, ax = plt.subplots()
            sns.histplot(df['total_annual'], bins=30, kde=True, ax=ax)
            ax.set_xlabel("Consommation annuelle (kWh)")
            st.pyplot(fig)

        with col2:
            st.subheader("Boxplot de la consommation maximale")
            fig, ax = plt.subplots()
            sns.boxplot(x=df['max_cons'], ax=ax)
            st.pyplot(fig)

        st.subheader("Relation entre la variance et le facteur de charge")
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x='variance', y='load_factor', hue='kmeans_cluster', palette='viridis', ax=ax)
        st.pyplot(fig)
    else:
        st.error("Impossible d’afficher les graphiques : données non chargées.")

# --- PAGE CLUSTERING ---
elif page == "Clustering":
    st.title("🤖 Résultats du Clustering")
    if df is not None:
        st.subheader("Répartition des compteurs par cluster K-Means")
        cluster_counts = df['kmeans_cluster'].value_counts().sort_index()
        st.bar_chart(cluster_counts)

        st.subheader("Visualisation des clusters")
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x='total_annual', y='max_cons', hue='kmeans_cluster', palette='husl', ax=ax)
        ax.set_xlabel("Consommation annuelle (kWh)")
        ax.set_ylabel("Consommation maximale (kWh)")
        st.pyplot(fig)
    else:
        st.error("⚠️ Données non trouvées pour les clusters.")

# --- PAGE ANALYSE ÉNERGÉTIQUE ---
elif page == "Analyse énergétique":
    st.title("💡 Analyse énergétique et indicateurs de performance")
    if df is not None:
        st.write("Voici quelques indicateurs clés calculés par cluster :")
        indicators = df.groupby('kmeans_cluster')[['total_annual', 'max_cons', 'variance', 'load_factor']].mean().round(2)
        st.dataframe(indicators)

        st.info("💬 Interprétation :")
        st.markdown("""
        - Un **fort facteur de charge** indique une consommation stable.
        - Une **variance élevée** signale un comportement irrégulier ou intermittent.
        - Les clusters avec faible pic ou forte variabilité peuvent bénéficier d’un **tarif variable**.
        """)
    else:
        st.warning("Aucune donnée disponible pour l’analyse.")

# --- PIED DE PAGE ---
st.markdown("---")
st.markdown("**Projet Smart Grid - SUP'COM / 2025-2026** | Tableau de bord Streamlit")

