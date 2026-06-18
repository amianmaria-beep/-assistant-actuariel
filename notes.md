# API
## C'est quoi une API (Application Programming Interface)?
Une API c'est une interface qui permet de de conneceter des application entre elles.Elle joue le role d'intermediaire, par exemple en transportant les donner d'un programme vers un serveur .

## Pourquoi faut-il protéger les clés API ?
Une clé API est personnelle car en plus de permettre de converser avec un seveur elle est comme un mot de passe et comme connectée à notre carte bancaire et donc si quelqu'un parvenait à l'avoir elle pourrai l'utiliser et depasser les limites de depenses qu'on se serait soi meme fixée.

## Comment on la protège dans un projet Python ?
On la protège en créant un fichier special .env dans lequel on la met et le fichier .gitignore empeche Git d'envoyer le fichier sur GitHub,car la clé elle meme ne dois jamais y aller .

# CREATION DE SOUS-DOSSIERS 
La creation de sous-dossiers permettra de structurer le projet afin qu'il soit lisible . Pour l'instant je crée **3 dossiers**:

-  **src** pour le code source 
-  **docs** pour tous les documents actuariels que j'aurai à uploader (pour le RAG)
-  **tests** pour mes fichiers test
(fichier test : un code pour evaluer et valider mon assistant)

# INSTALLATION DE LA BIBLIOTHEQUE **ANTHROPIC** et **PYTHON-DOTENV**
Anthropic est la bibliothèque qui permet de parler à l'API depuis python
python-dotenv est la bibliothèque qui me permet de lire automatiquement mon fichie .env pour récuperer ma clé API

# CREATION D'UN README
Le readme doit repondre à 3 questions importantes pour l'instant :
- C'est quoi le projet ?
- Quelles sont les differentes technologies que j'ai utilisé?
- Quelles sont les differentes étapes de l'organisation de mon projet?


# Compréhension du premier script API (test_api.py)

## Les imports
- **anthropic**: le SDK pour communiquer avec Claude
- **load_dotenv** : lit le fichier .env et charge la clé en mémoire
- **os** : bibliothèque intégrée à Python (pas besoin de pip install),
  permet d'accéder aux variables d'environnement via os.getenv()

## Charger la clé API
load_dotenv() charge le fichier .env en mémoire.
os.getenv("ANTHROPIC_API_KEY") va chercher la clé dedans.
Sans load_dotenv(), Python ne sait pas où est la clé.

## Le client Anthropic
client = anthropic.Anthropic(api_key=...) crée la connexion
avec le serveur Anthropic en s'authentifiant avec la clé API.

## Les paramètres de la requête
- model : quel modèle Claude utiliser.
  claude-sonnet-4-6 = meilleur équilibre qualité / coût
- max_tokens : longueur maximale de la réponse (1024 ≈ 700 mots)
- messages : la conversation. Chaque message a un rôle :
    - "system" :instructions invisibles pour Claude (avec le prompt system)
    - "user" :la question qu'on pose
    - "assistant" :la réponse de Claude

## La réponse
La réponse arrive en JSON. Le SDK la décode automatiquement.
response.content est une liste,on prend le premier élément avec content[0].text pour obtenir le texte de la réponse.
C'est une liste car Claude peut renvoyer plusieurs types de contenu en même temps (texte + résultats d'outils).

## Format JSON
Format universel pour transporter des données entre programmes.
{ } = objet, [ ] = liste, "clé": "valeur" = information.

