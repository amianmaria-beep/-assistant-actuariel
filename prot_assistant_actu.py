#Essai streamlit
import streamlit as st

# 1. TITRES ET TEXTES
st.title("Grand titre")
st.header("Titre moyen")
st.subheader("Petit titre")
st.write("Texte normal")

# 2. ZONE DE SAISIE
question = st.text_input("Tape quelque chose ici :")
if question:
    st.write("Tu as écrit :", question)

# 3. BOUTON
if st.button("Clique moi"):
    st.write("Tu as cliqué sur le bouton !")

# 4. SELECTEUR
choix = st.selectbox("Choisis un indicateur :", 
    ["Ratio sinistres", "Provision", "SCR", "Prime pure"])

if choix == "Ratio sinistres":
    st.write("C'est le rapport entre sinistres payés et primes acquises.")
elif choix == "Provision":
    st.write("Somme réservée pour couvrir des sinistres futurs.")
elif choix == "SCR":
    st.write("Solvency Capital Requirement : capital minimum réglementaire.")
elif choix == "Prime pure":
    st.write("La prime qui couvre exactement le coût des sinistres.")

# 5. CURSEUR NUMERIQUE
nombre = st.slider("Choisis un nombre :", 0, 100, 50)
st.write("Valeur choisie :", nombre)
# 6. ZONE DE TEXTE LONGUE (pour un rapport par exemple)
texte = st.text_area("Colle un extrait de rapport ici :")
if texte:
    st.write("Nombre de mots :", len(texte.split()))

# 7. UPLOAD DE FICHIER ( utile pour le RAG)
fichier = st.file_uploader("Charge un document :", type=["pdf", "txt"])
if fichier:
    st.write("Fichier chargé :", fichier.name)

# 8. COLONNES (pour organiser l'affichage)
col1, col2 = st.columns(2)
with col1:
    st.metric("Ratio sinistres", "72%", "+3%")
with col2:
    st.metric("SCR", "1.2M €", "-5%")

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choisir une section :", 
    ["Accueil", "Indicateurs", "Résumé de portefeuille", "Reporting"])

st.write("Tu es sur la page :", page)
