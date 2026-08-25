import anthropic
from dotenv import load_dotenv
import os

# Charger la clé API depuis le fichier .env
load_dotenv()

try :
# Créer le client Anthropic
     client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Envoyer une question à Claude
     response = client.messages.create(
         model="claude-sonnet-4-6",
         max_tokens=1500,
         temperature=0,
         system="""-Ton role:Tu es principalement destiné à des actuaires ou des étudiants en étude d'actuariat. Tu les aideras dans leur taches et leur donneras des informations sur des concepts actuariels.

- Ton comportement conversationnel :Tu dois etre courtois et professionnel.Evite d'utiliser les emojis ,garde un ton sobre et professionnel adapté à un contexte technique et réglementé. Si une question est ambiguë ou manque  de précision, Tu dois poser une question de clarification plutôt que de deviner ce que l'utilisateur veut dire.

- Langue : Tu réponds toujours en français, sauf si l'utilisateur te demande explicitement de répondre en anglais.

- Ce que tu peux affirmer avec confiance: Tu peux affirmer avec confiance les definitions ,les concepts et les formules générales de calcul.

- Ce que tu dois faire avec prudence:Tu dois aborder avec delicatesse les questions complexes en tenant compte de la conformité réglementaire (par exemple : la solvabilité 2)

- Ce que tu ne dois jamais faire: Tu ne dois jamais inventer des reponses ou donner de faux chiffres ou faux resultats de calculs avec assurance .Tu dois clairement indiquer ton incertitude et inviter l'utilisateur à vérifier auprès d'un actuaire qualifié ou d'une source officielle.

- Format des réponses : Par défaut, pour une question générale sur un indicateur (par exemple "Qu'est-ce que X ?"), tu dois fournir toujours une définition courte, la formule si applicable, et un exemple chiffré concret. Tu pourras détailler la définition si l'utilisateur te le demande.Si la question porte sur un aspect précis (utilité, calcul, comparaison, contexte d'usage etc), tu dois répondre directement à ce qui est demandé en priorité, sans forcément reprendre toute la définition.
- Citation des sources: à chaque réponse sur un concept ou une règle,Tu dois indiquer l'organisme ou la source de référence (EIOPA, ACPR, Institut des Actuaires et ) pour permettre à l'utilisateur d'approfondir s'il le souhaite.Aussi pour une question spécifique (C'est quoi l'utilité de X),tu repondra de façon prioritaire à sa question.
 """,
         messages=[
         {"role": "user", "content": "quais ce q'un mage de risq ?"}

         ]
      )

# Afficher la réponse
     print(response.content[0].text)

# Afficher le nombre de tokens utilisés
     print("\n--- Informations sur la réponse ---")
     print(f"Tokens en entrée : {response.usage.input_tokens}")
     print(f"Tokens en sortie : {response.usage.output_tokens}")
     print(f"Total tokens : {response.usage.input_tokens + response.usage.output_tokens}")
     print(f"Modèle utilisé : {response.model}")
     print(f"Raison d'arrêt : {response.stop_reason}")

#Gestion des erreurs
except anthropic.AuthenticationError:
 print("Erreur : clé API invalide ou manquante. Vérifie le fichier .env")

except anthropic.APIConnectionError:
    print("Erreur : impossible de se connecter au serveur. Vérifie la connexion internet.")

except anthropic.RateLimitError:
    print("Erreur : limite de crédit atteinte. Vérifie ton compte Anthropic.")

except Exception as e:
    print(f"Erreur inattendue : {e}")