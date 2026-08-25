# ASSISTANT ACTUARIEL IA
# Prototype de stage — LLM + RAG + Streamlit

import streamlit as st
import anthropic
from dotenv import load_dotenv
import os
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import tempfile
import pandas as pd

# Chargement de la clé API depuis .env
load_dotenv()

# Client Anthropic mis en cache (instancié une seule fois)
@st.cache_resource
def get_client():
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Configuration de la page
st.set_page_config(page_title="Assistant Actuariel", layout="wide")

# CSS personnalisé
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #2E4A7A; }
    [data-testid="stSidebar"] *:not(select):not(option):not(input) { color: #FFFFFF !important; }
    [data-testid="stAppViewContainer"] { background-color: #F0F4F8; }
    [data-testid="stChatInput"] {
        background-color: #FFFFFF;
        border: 2px solid #2E4A7A;
        border-radius: 15px;
        padding: 10px;
    }
    [data-testid="stSidebar"] .stButton button {
        background-color: #C9A84C;
        color: white;
        border: none;
        border-radius: 8px;
        width: 100%;
    }
    [data-testid="stFileUploader"] { background-color: #FFFFFF; border-radius: 8px; padding: 5px; }
    [data-testid="stFileUploader"] * { color: #1B3A6B !important; }
    [data-testid="stFileUploader"] button { color: #1B3A6B !important; background-color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)

# Initialisation du session_state
# Conserve les données entre les réexécutions Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "vectorstore_f3" not in st.session_state:
    st.session_state.vectorstore_f3 = None
if "fonction" not in st.session_state:
    st.session_state.fonction = "Fonction 1 - Indicateurs actuariels"
if "fichiers_charges" not in st.session_state:
    st.session_state.fichiers_charges = []
if "fichiers_charges_f3" not in st.session_state:
    st.session_state.fichiers_charges_f3 = []
if "historique_conversations" not in st.session_state:
    st.session_state.historique_conversations = {}
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None
if "sources" not in st.session_state:
    st.session_state.sources = []
if "documents_sauvegardes" not in st.session_state:
    st.session_state.documents_sauvegardes = {}
if "question_predifinie" not in st.session_state:
    st.session_state.question_predifinie = None

# Fonction d'indexation des documents
def indexer_documents(uploaded_files):
    """
    Charge et indexe une liste de fichiers PDF ou Excel dans une base vectorielle FAISS.
    Retourne le vectorstore et la liste des chunks créés.
    """
    all_chunks = []
    for uploaded_file in uploaded_files:
        suffix = f".{uploaded_file.name.split('.')[-1]}"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        if uploaded_file.name.endswith((".xlsx", ".xls")):
            # Lecture Excel : chaque feuille est convertie en texte structuré
            df = pd.read_excel(tmp_path, sheet_name=None)
            texte_excel = ""
            for sheet_name, sheet_df in df.items():
                texte_excel += f"\n### Feuille : {sheet_name}\n"
                texte_excel += sheet_df.to_string(index=False)
            documents = [Document(page_content=texte_excel, metadata={"source": uploaded_file.name})]
        else:
            # Lecture PDF page par page
            loader = PyPDFLoader(tmp_path)
            documents = loader.load()

        # Découpage en chunks (1000 caractères, chevauchement 200)
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(documents)
        all_chunks.extend(chunks)

    # Création des embeddings et de la base vectorielle FAISS
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    vectorstore = FAISS.from_documents(all_chunks, embeddings)
    return vectorstore, all_chunks

# Sidebar
with st.sidebar:
    st.title("Assistant Actuariel")
    st.markdown("---")
    st.markdown("**Modèle** : Claude Sonnet 4.6")
    st.markdown("**Domaine** : Actuariat")
    st.markdown("---")

    # Sélecteur de fonction
    st.markdown("**Choisir une fonction**")
    fonction = st.radio("", [
        "Fonction 1 - Indicateurs actuariels",
        "Fonction 2 - Analyse de documents",
        "Fonction 3 - Aide au reporting"
    ])

    # Badge mode actif
    mode_actif = fonction.split("-")[1].strip()
    st.markdown(f"""
    <div style='background-color:#C9A84C;color:white;padding:6px 12px;
    border-radius:8px;font-size:13px;font-weight:500;margin-top:5px;'>
    Mode actif : {mode_actif}
    </div>
    """, unsafe_allow_html=True)

    # Réinitialisation automatique au changement de fonction
    if fonction != st.session_state.fonction:
        # Sauvegarder la conversation en cours avant de changer
        if st.session_state.messages:
            conv_id = st.session_state.conversation_id or datetime.now().strftime("%Y%m%d_%H%M%S")
            premiere_question = st.session_state.messages[0]['content'][:40]
            date_heure = datetime.now().strftime("%d/%m %H:%M")
            st.session_state.historique_conversations[conv_id] = {
                'titre': f"{premiere_question}... — {date_heure}",
                'messages': st.session_state.messages.copy(),
                'fonction': st.session_state.fonction
            }
        st.session_state.messages = []
        st.session_state.vectorstore = None
        st.session_state.fichiers_charges = []
        st.session_state.fonction = fonction
        st.session_state.conversation_id = None
        st.rerun()

    st.markdown("---")

    # Upload documents — Fonction 2
    if "Fonction 2" in fonction:
        st.markdown("**Charger un document**")
        uploaded_files = st.file_uploader(
            "PDF ou Excel", type=["pdf", "xlsx", "xls"],
            accept_multiple_files=True, key="upload_f2"
        )
        if uploaded_files:
            noms_fichiers = [f.name for f in uploaded_files]
            if noms_fichiers != st.session_state.fichiers_charges:
                with st.spinner("Chargement en cours..."):
                    vectorstore, _ = indexer_documents(uploaded_files)
                    st.session_state.vectorstore = vectorstore
                    st.session_state.fichiers_charges = noms_fichiers
                    for f in uploaded_files:
                        st.session_state.documents_sauvegardes[f.name] = f
                    st.success("✓ Document(s) chargé(s) avec succès")

        if st.session_state.documents_sauvegardes:
            st.markdown("**Documents déjà chargés**")
            for nom in st.session_state.documents_sauvegardes:
                st.caption(f"📄 {nom}")
        st.markdown("---")

    # Upload documents — Fonction 3
    if "Fonction 3" in fonction:
        st.markdown("**Charger vos données (optionnel)**")
        uploaded_files_f3 = st.file_uploader(
            "PDF ou Excel avec vos données", type=["pdf", "xlsx", "xls"],
            accept_multiple_files=True, key="upload_f3"
        )
        if 'uploaded_files_f3' in dir() and uploaded_files_f3:
            noms_f3 = [f.name for f in uploaded_files_f3]
            if noms_f3 != st.session_state.fichiers_charges_f3:
                with st.spinner("Chargement en cours..."):
                    vectorstore_f3, _ = indexer_documents(uploaded_files_f3)
                    st.session_state.vectorstore_f3 = vectorstore_f3
                    st.session_state.fichiers_charges_f3 = noms_f3
                    st.success("✓ Document(s) chargé(s) avec succès")
        st.markdown("---")

    # Bouton nouvelle conversation
    if st.button("✏️ Nouvelle conversation"):
        if st.session_state.messages:
            conv_id = st.session_state.conversation_id or datetime.now().strftime("%Y%m%d_%H%M%S")
            premiere_question = st.session_state.messages[0]['content'][:40]
            date_heure = datetime.now().strftime("%d/%m %H:%M")
            st.session_state.historique_conversations[conv_id] = {
                'titre': f"{premiere_question}... — {date_heure}",
                'messages': st.session_state.messages.copy(),
                'fonction': st.session_state.fonction
            }
        st.session_state.messages = []
        st.session_state.conversation_id = None
        st.rerun()

    # Historique des conversations
    if st.session_state.historique_conversations:
        st.markdown("**Historique**")
        for conv_id, conv_data in list(st.session_state.historique_conversations.items())[::-1]:
            date_heure = conv_data['titre'].split('—')[-1].strip()
            titre_court = conv_data['titre'].split('...')[0].strip()
            st.caption(date_heure)
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(f"💬 {titre_court[:25]}...", key=f"hist_{conv_id}"):
                    st.session_state.messages = conv_data['messages'].copy()
                    st.session_state.conversation_id = conv_id
                    st.rerun()
            with col2:
                if st.button("🗑", key=f"del_{conv_id}"):
                    del st.session_state.historique_conversations[conv_id]
                    st.rerun()

    st.markdown("---")

    # Bouton effacer la conversation courante
    if st.button("🗑 Effacer la conversation"):
        st.session_state.confirmer_effacement = True

    if st.session_state.get("confirmer_effacement", False):
        st.sidebar.warning("Êtes-vous sûr ?")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Oui"):
                st.session_state.messages = []
                st.session_state.conversation_id = None
                st.session_state.confirmer_effacement = False
                st.rerun()
        with col2:
            if st.button("Non"):
                st.session_state.confirmer_effacement = False
                st.rerun()

    st.markdown("---")
    st.caption("Projet de stage (juin - Juillet 2026)")

# Prompts système par fonction
prompts = {
    "Fonction 1 - Indicateurs actuariels": """Tu es un assistant actuariel expert destiné aux actuaires et étudiants en actuariat.
Tu expliques les indicateurs actuariels (SCR, BEL, IBNR, ratio combiné, S/P, prime pure, MCR, ROE, RORAC...).
Pour chaque indicateur : définition courte, formule si applicable, exemple chiffré concret.
Tu es courtois, professionnel, sans emojis.
Tu cites toujours tes sources (EIOPA, ACPR, Institut des Actuaires).
Tu ne dois jamais inventer de chiffres ou de faits.""",

    "Fonction 2 - Analyse de documents": """Tu es un assistant actuariel expert en analyse de documents.
Quand un contexte documentaire est fourni, tu bases ta réponse sur ce contexte en priorité.
Tu indiques toujours que l'information provient du document chargé.
Si la réponse n'est pas dans le contexte, tu le dis clairement sans inventer.
Tu es courtois, professionnel, sans emojis, en français.""",

    "Fonction 3 - Aide au reporting": """Tu es un assistant actuariel expert en reportings réglementaires.
Tu aides à rédiger des sections de rapports ORSA, SFCR et autres reportings Solvabilité II.
Quand des données sont fournies, tu les utilises pour rédiger un reporting précis et chiffré.
Tu proposes des formulations professionnelles conformes aux exigences réglementaires.
Tu signales toujours quand une validation par un actuaire qualifié est nécessaire.
Tu es courtois, professionnel, sans emojis, en français."""
}

# Titre et message de bienvenue
heure = datetime.now().hour
salutation = "Bonjour" if heure < 12 else "Bon après-midi" if heure < 18 else "Bonsoir"

descriptions = {
    "Fonction 1 - Indicateurs actuariels": "Posez vos questions sur les indicateurs actuariels : SCR, BEL, IBNR, ratio combiné, prime pure...",
    "Fonction 2 - Analyse de documents": "Chargez un ou plusieurs PDF/Excel dans la sidebar et posez vos questions sur leur contenu.",
    "Fonction 3 - Aide au reporting": "Chargez vos données (optionnel) et décrivez la section de reporting que vous souhaitez rédiger."
}

st.markdown("""
<h1 style='color:#2E4A7A;font-size:2.5rem;font-weight:700;
border-bottom:3px solid #C9A84C;padding-bottom:10px;'>
Assistant Actuariel IA</h1>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style='background-color:#2E4A7A;color:white;padding:15px 20px;
border-radius:10px;margin-bottom:20px;'>
{salutation} ! {descriptions[st.session_state.fonction]}
</div>
""", unsafe_allow_html=True)

# Questions prédéfinies
questions_predefinies = {
    "Fonction 1 - Indicateurs actuariels": [
        "Explique-moi le SCR",
        "C'est quoi le Best Estimate ?",
        "Comment calculer le ratio combiné ?",
        "C'est quoi l'IBNR ?"
    ],
    "Fonction 2 - Analyse de documents": [
        "Fais un résumé de ce document",
        "Quels sont les chiffres clés ?",
        "Quelles sont les conclusions principales ?"
    ],
    "Fonction 3 - Aide au reporting": [
        "Rédige une introduction ORSA",
        "Aide-moi à rédiger la section risques du SFCR",
        "Quelles sont les exigences réglementaires ORSA ?"
    ]
}

st.markdown("**Questions fréquentes :**")
cols = st.columns(len(questions_predefinies[st.session_state.fonction]))
for i, question in enumerate(questions_predefinies[st.session_state.fonction]):
    with cols[i]:
        if st.button(question, key=f"q_{i}"):
            st.session_state.question_predifinie = question

# Zone de saisie
prompt = st.chat_input("Votre question :")

# Si une question prédéfinie a été cliquée, elle prend le dessus
if st.session_state.get("question_predifinie"):
    prompt = st.session_state.question_predifinie
    st.session_state.question_predifinie = None

# Traitement de la question et appel API
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Réponse en cours..."):
        try:
            client = get_client()
            prompt_systeme = prompts[st.session_state.fonction]

            # RAG — Fonction 2 : recherche dans les documents uploadés
            if "Fonction 2" in st.session_state.fonction and st.session_state.vectorstore:
                docs_proches = st.session_state.vectorstore.similarity_search(prompt, k=8)
                contexte = "\n\n".join([
                    f"[Source: {doc.metadata.get('source', 'Document')}]\n{doc.page_content}"
                    for doc in docs_proches
                ])
                st.session_state.sources = docs_proches
                messages_api = st.session_state.messages[:-1] + [
                    {"role": "user", "content": f"Contexte documentaire :\n{contexte}\n\nQuestion : {prompt}"}
                ]

            # RAG — Fonction 3 : recherche dans les données fournies
            elif "Fonction 3" in st.session_state.fonction and st.session_state.vectorstore_f3:
                docs_proches = st.session_state.vectorstore_f3.similarity_search(prompt, k=8)
                contexte = "\n\n".join([
                    f"[Source: {doc.metadata.get('source', 'Document')}]\n{doc.page_content}"
                    for doc in docs_proches
                ])
                messages_api = st.session_state.messages[:-1] + [
                    {"role": "user", "content": f"Données fournies :\n{contexte}\n\nDemande : {prompt}"}
                ]

            # Pas de RAG — Fonction 1 ou Fonction 3 sans document
            else:
                messages_api = st.session_state.messages

            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1500,
                temperature=0,
                system=prompt_systeme,
                messages=messages_api
            )
            reponse_texte = response.content[0].text
            st.session_state.messages.append({
                "role": "assistant",
                "content": reponse_texte
            })

            # Sauvegarde automatique dans l'historique
            if len(st.session_state.messages) >= 2:
                if st.session_state.conversation_id is None:
                    st.session_state.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
                conv_id = st.session_state.conversation_id
                premiere_question = st.session_state.messages[0]['content'][:40]
                date_heure = datetime.now().strftime("%d/%m %H:%M")
                st.session_state.historique_conversations[conv_id] = {
                    'titre': f"{premiere_question}... — {date_heure}",
                    'messages': st.session_state.messages.copy(),
                    'fonction': st.session_state.fonction
                }
        except anthropic.AuthenticationError:
            st.error("Clé API invalide. Vérifiez votre fichier .env")
        except anthropic.APIConnectionError:
            st.error("Connexion impossible. Vérifiez votre connexion internet.")
        except anthropic.RateLimitError:
            st.error("Limite de crédit atteinte. Vérifiez votre compte Anthropic.")
        except Exception as e:
            st.error(f"Erreur inattendue : {e}")

# Affichage de la conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Sources utilisées (Fonction 2 uniquement)
if "Fonction 2" in st.session_state.fonction and st.session_state.get("sources"):
    with st.expander("📄 Voir les extraits utilisés pour cette réponse"):
        for i, doc in enumerate(st.session_state.sources):
            st.markdown(f"**Extrait {i+1}**")
            st.text(doc.page_content[:300])
            st.markdown("---")

# Export de la conversation
if st.session_state.messages:
    conversation_texte = ""
    for msg in st.session_state.messages:
        role = "Utilisateur" if msg["role"] == "user" else "Assistant"
        conversation_texte += f"{role} :\n{msg['content']}\n\n{'—'*50}\n\n"

    st.download_button(
        label="📥 Télécharger la conversation",
        data=conversation_texte.encode("utf-8"),
        file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )