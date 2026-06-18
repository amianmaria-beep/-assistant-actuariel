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
         temperature=1,
         messages=[
         {"role": "user", "content": "Explique-moi la prime pure en actuariat"}
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