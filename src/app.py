import streamlit as st
import anthropic
from dotenv import load_dotenv
import os
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import tempfile

# Configuration de la page
st.set_page_config(
    page_title="Assistant Actuariel",
    layout="wide"
)

# Mise en forme
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #2E4A7A;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    [data-testid="stChatInput"] {
        border-color: #2E4A7A;
    }
    h1 {
        color: #2E4A7A;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #F0F4F8;
    }
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
    [data-testid="stFileUploader"] {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 5px;
    }
    [data-testid="stFileUploader"] * {
        color: #1B3A6B !important;
    }
    /* Selectbox visible */
[data-testid="stSelectbox"] > div > div {
    background-color: #FFFFFF;
    color: #1B3A6B !important;
    border-radius: 8px;
    border: 2px solid #C9A84C;
}
</style>
""", unsafe_allow_html=True)

# Charger la clé API
load_dotenv()

# Initialisation session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "fonction" not in st.session_state:
    st.session_state.fonction = "Fonction 1 — Indicateurs actuariels"

# Sidebar
with st.sidebar:
    st.title("Assistant Actuariel")
    st.markdown("---")
    st.markdown("**Modèle** : Claude Sonnet 4.6")
    st.markdown("**Domaine** : Actuariat")
    st.markdown("---")

    # NOUVEAU — Sélecteur de fonction
    st.markdown("**Choisir une fonction**")
    fonction = st.selectbox(
        "",
        [
            "Fonction 1 — Indicateurs actuariels",
            "Fonction 2 — Analyse de documents",
            "Fonction 3 — Aide au reporting"
        ]
    )
    st.markdown(f"""
    <div style='background-color:#C9A84C;color:white;padding:6px 12px;
    border-radius:8px;font-size:13px;font-weight:500;margin-top:5px;'>
    Mode actif : {fonction.split("—")[1].strip()}
    </div>
    """, unsafe_allow_html=True)
    if fonction != st.session_state.fonction:
        st.session_state.messages = []
        st.session_state.vectorstore = None
        st.session_state.fonction = fonction
        st.rerun()
    st.session_state.fonction = fonction
    st.markdown("---")

    # Upload PDF uniquement pour Fonction 2
    if "Fonction 2" in fonction:
        st.markdown("**Charger un document**")
        uploaded_file = st.file_uploader("Uploader un PDF", type="pdf")

        if uploaded_file is not None:
            with st.spinner("Indexation en cours..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                loader = PyPDFLoader(tmp_path)
                documents = loader.load()
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000, chunk_overlap=200
                )
                chunks = splitter.split_documents(documents)
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
                )
                st.session_state.vectorstore = FAISS.from_documents(chunks, embeddings)
                st.success(f"✓ {len(chunks)} chunks indexés")
        st.markdown("---")

    # Bouton effacer
    if st.button("🗑 Effacer la conversation"):
        st.session_state.confirmer_effacement = True

    if st.session_state.get("confirmer_effacement", False):
        st.sidebar.warning("Êtes-vous sûr ? Cette action est irréversible.")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Oui"):
                st.session_state.messages = []
                st.session_state.confirmer_effacement = False
                st.rerun()
        with col2:
            if st.button("Non"):
                st.session_state.confirmer_effacement = False
                st.rerun()

    st.markdown("---")
    st.caption("Projet de stage — Juillet 2026")

# NOUVEAU — Trois prompts système selon la fonction
prompts = {
    "Fonction 1 — Indicateurs actuariels": """-Ton role : Tu es principalement destiné à des actuaires ou des étudiants en étude d'actuariat. Tu les aideras dans leurs tâches et leur donneras des informations sur des concepts actuariels.

- Ton comportement conversationnel : Tu dois être courtois et professionnel. Evite d'utiliser les emojis, garde un ton sobre et professionnel adapté à un contexte technique et réglementé. Si une question est ambiguë ou manque de précision, tu dois poser une question de clarification plutôt que de deviner ce que l'utilisateur veut dire.

- Langue : Tu réponds toujours en français, sauf si l'utilisateur te demande explicitement de répondre en anglais.

- Ce que tu peux affirmer avec confiance : Tu peux affirmer avec confiance les définitions, les concepts et les formules générales de calcul.

- Ce que tu dois faire avec prudence : Tu dois aborder avec délicatesse les questions complexes en tenant compte de la conformité réglementaire (par exemple : la Solvabilité II).

- Ce que tu ne dois jamais faire : Tu ne dois jamais inventer des réponses ou donner de faux chiffres. Tu dois clairement indiquer ton incertitude et inviter l'utilisateur à vérifier auprès d'un actuaire qualifié ou d'une source officielle.

- Format des réponses : Par défaut, pour une question générale sur un indicateur, tu dois fournir une définition courte, la formule si applicable, et un exemple chiffré concret. Si la question porte sur un aspect précis, tu réponds directement à ce qui est demandé en priorité.

- Citation des sources : à chaque réponse sur un concept ou une règle, tu dois indiquer l'organisme ou la source de référence (EIOPA, ACPR, Institut des Actuaires) pour permettre à l'utilisateur d'approfondir.""",

    "Fonction 2 — Analyse de documents": """-Ton role : Tu es un assistant actuariel expert en analyse de documents.
- Quand un contexte documentaire est fourni, tu bases ta réponse sur ce contexte en priorité.
- Tu indiques toujours que l'information provient du document chargé.
- Si la réponse n'est pas dans le contexte, tu le dis clairement sans inventer.
- Tu es courtois, professionnel, sans emojis, en français.""",

    "Fonction 3 — Aide au reporting": """-Ton role : Tu es un assistant actuariel expert en reportings réglementaires.
- Tu aides à rédiger des sections de rapports ORSA, SFCR et autres reportings Solvabilité II.
- Tu proposes des formulations professionnelles conformes aux exigences réglementaires.
- Tu signales toujours quand une validation par un actuaire qualifié est nécessaire.
- Tu es courtois, professionnel, sans emojis, en français."""
}

# Heure de salutation
heure = datetime.now().hour
if heure < 12:
    salutation = "Bonjour"
elif heure < 18:
    salutation = "Bon après-midi"
else:
    salutation = "Bonsoir"

# NOUVEAU — Message de bienvenue dynamique selon la fonction
descriptions = {
    "Fonction 1 — Indicateurs actuariels": "Posez vos questions sur les indicateurs actuariels : SCR, BEL, IBNR, ratio combiné, prime pure...",
    "Fonction 2 — Analyse de documents": "Chargez un PDF dans la sidebar et posez vos questions sur son contenu.",
    "Fonction 3 — Aide au reporting": "Décrivez la section de reporting que vous souhaitez rédiger (ORSA, SFCR...)."
}

message_bienvenue = f"{salutation} ! {descriptions[st.session_state.fonction]}"

# Titre
st.markdown("""
<h1 style='
    color: #2E4A7A;
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    border-bottom: 3px solid #C9A84C;
    padding-bottom: 10px;
    margin-bottom: 5px;
'>Assistant Actuariel IA</h1>
""", unsafe_allow_html=True)

# Message de bienvenue
st.markdown(f"""
<div style='
    background-color: #2E4A7A;
    color: white;
    padding: 15px 20px;
    border-radius: 10px;
    margin-bottom: 20px;
'>
    {message_bienvenue}
</div>
""", unsafe_allow_html=True)

# Gestion de la question
if prompt := st.chat_input("Votre question :"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Réponse en cours..."):
        try:
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            # Prompt selon la fonction choisie
            prompt_systeme = prompts[st.session_state.fonction]

            # RAG uniquement pour Fonction 2
            if "Fonction 2" in st.session_state.fonction and st.session_state.vectorstore:
                docs_proches = st.session_state.vectorstore.similarity_search(prompt, k=3)
                contexte = "\n\n".join([doc.page_content for doc in docs_proches])
                messages_api = st.session_state.messages[:-1] + [
                    {"role": "user", "content": f"Contexte documentaire :\n{contexte}\n\nQuestion : {prompt}"}
                ]
            else:
                messages_api = st.session_state.messages

            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1500,
                temperature=0,
                system=prompt_systeme,
                messages=messages_api
            )
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.content[0].text
            })

        except anthropic.AuthenticationError:
            st.error("Clé API invalide.")
        except anthropic.APIConnectionError:
            st.error("Connexion impossible.")
        except anthropic.RateLimitError:
            st.error("Limite de crédit atteinte.")
        except Exception as e:
            st.error(f"Erreur : {e}")

# Afficher l'historique
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])