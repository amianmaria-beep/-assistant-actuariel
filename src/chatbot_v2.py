import streamlit as st
import anthropic
from dotenv import load_dotenv
import os
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Assistant Actuariel",
    layout="wide"
)

#Mise en forme 
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
    /* Fond de la page principale */
    [data-testid="stAppViewContainer"] {
        background-color: #F0F4F8;
    }
    /* Zone de saisie */
     [data-testid="stChatInput"] {
        background-color: #FFFFFF;
        border: 2px solid #2E4A7A;
        border-radius: 15px;
        padding: 10px;
    }
    [data-testid="stSidebar"] .stButton button {
     background-color: #C9A84C;
     : white;
      border: none;
     rder-radius: 8px;
     idth: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Assistant Actuariel")
    st.markdown("---")
    st.markdown("**Modèle** : Claude Sonnet 4.6")
    st.markdown("**Domaine** : Actuariat ")
    st.markdown("---")
    st.caption("Projet de stage — Juin 2026")
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


# Heure de salutation 
heure = datetime.now().hour

if heure < 12:
    salutation = "Bonjour"
elif heure < 18:
    salutation = "Bon après-midi"
else:
    salutation = "Bonsoir"
message_bienvenue = f"{salutation} ! Je suis votre assistant actuariel. Je peux vous aider à comprendre les indicateurs actuariels, analyser des portefeuilles et vous accompagner dans vos reportings réglementaires. Comment puis-je vous aider ?"
# Titre et description
# grand titre 
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

# message de bienvenue
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

# Charger la clé API depuis le fichier .env
load_dotenv()

# Initialisation de la mémoire de conversation
if "messages" not in st.session_state:
    st.session_state.messages = []


# prompt système
prompt_systeme="""-Ton role:Tu es principalement destiné à des actuaires ou des étudiants en étude d'actuariat. Tu les aideras dans leur taches et leur donneras des informations sur des concepts actuariels.

- Ton comportement conversationnel :Tu dois etre courtois et professionnel.Evite d'utiliser les emojis ,garde un ton sobre et professionnel adapté à un contexte technique et réglementé. Si une question est ambiguë ou manque  de précision, Tu dois poser une question de clarification plutôt que de deviner ce que l'utilisateur veut dire.

- Langue : Tu réponds toujours en français, sauf si l'utilisateur te demande explicitement de répondre en anglais.

- Ce que tu peux affirmer avec confiance: Tu peux affirmer avec confiance les definitions ,les concepts et les formules générales de calcul.

- Ce que tu dois faire avec prudence:Tu dois aborder avec delicatesse les questions complexes en tenant compte de la conformité réglementaire (par exemple : la solvabilité 2)

- Ce que tu ne dois jamais faire: Tu ne dois jamais inventer des reponses ou donner de faux chiffres ou faux resultats de calculs avec assurance .Tu dois clairement indiquer ton incertitude et inviter l'utilisateur à vérifier auprès d'un actuaire qualifié ou d'une source officielle.

- Format des réponses : Par défaut, pour une question générale sur un indicateur (par exemple "Qu'est-ce que X ?"), tu dois fournir toujours une définition courte, la formule si applicable, et un exemple chiffré concret. Tu pourras détailler la définition si l'utilisateur te le demande.Si la question porte sur un aspect précis (utilité, calcul, comparaison, contexte d'usage etc), tu dois répondre directement à ce qui est demandé en priorité, sans forcément reprendre toute la définition.
- Citation des sources: à chaque réponse sur un concept ou une règle,Tu dois indiquer l'organisme ou la source de référence (EIOPA, ACPR, Institut des Actuaires et ) pour permettre à l'utilisateur d'approfondir s'il le souhaite.Aussi pour une question spécifique (C'est quoi l'utilité de X),tu repondra de façon prioritaire à sa question.
  """

# Gestion de la nouvelle question
if prompt := st.chat_input("Votre question :"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("Réponse en cours..."):
        try:
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1500,
                temperature=0,
                system=prompt_systeme,
                messages=st.session_state.messages
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

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])