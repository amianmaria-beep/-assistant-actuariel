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
        color: ##2E4A7A;
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
    s}
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
# Zone de saisie utilisateur
question = st.chat_input("Votre question :")

# Bouton envoyer
if question:
    # Afficher la question de l'utilisateur
    with st.chat_message("user"):
        st.write(question)

    if question.strip() == "":
        st.warning("Veuillez écrire une question avant d'envoyer.")
    else:
        with st.spinner("Réponse en cours..."):
    
            try :
            # Créer le client Anthropic
                client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

            # Envoyer une question à Claude
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1500,
                    temperature=0,
                    system=prompt_systeme,
                    messages=[
                    {"role": "user", "content": question}

                    ]
                )

            # Afficher la réponse
                with st.chat_message("assistant"):
                  st.markdown(response.content[0].text)

            #Gestion des erreurs
            except anthropic.AuthenticationError:
                print("Erreur : clé API invalide ou manquante. Vérifie le fichier .env")

            except anthropic.APIConnectionError:
                print("Erreur : impossible de se connecter au serveur. Vérifie la connexion internet.")

            except anthropic.RateLimitError:
              print("Erreur : limite de crédit atteinte. Vérifie ton compte Anthropic.")

            except Exception as e:
               print(f"Erreur inattendue : {e}")



