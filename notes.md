# API
## C'est quoi une API (Application Programming Interface)?
Une API c'est une interface qui permet de de conneceter des application entre elles.Elle joue le role d'intermediaire, par exemple en transportant les donner d'un programme vers un serveur .

## Pourquoi faut-il protéger les clés API ?
Une clé API est personnelle car en plus de permettre de converser avec un seveur elle est comme un mot de passe et comme connectée à notre carte bancaire et donc si quelqu'un parvenait à l'avoir elle pourrai l'utiliser et depasser les limites de depenses qu'on se serait soi meme fixée.

## Comment on la protège dans un projet Python ?
On la protège en créant un fichier special .env dans lequel on la met et le fichier .gitignore empeche Git d'envoyer le fichier sur GitHub,car la clé elle meme ne dois jamais y aller .

# CREATION DE SOUS-DOSSIERS 
La creation de sous-dossiers permettra de structurer le projet afin qu'il soit lisible . Pour l'instant je crée **3 dossiers**:
-**src** pour le code source 
-**docs** pour tous les documents actuariels que j'aurai à uploader (pour le RAG)
-**tests** pour mes fichiers test
(fichier test : un code pour evaluer et valider mon assistant)

