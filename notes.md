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

# PROMPT SYSTEME

## Recensement des indicateurs actuariels et quelques definitions brève 
Un indicateur est une valeur calculable qui mesure quelquechose.
Comme indicateurs actuariels,on a:
- Best estimate :la meilleure estimation possible de ce que l'assureur devra payer dans le futur, ramenée à sa valeur d'aujourd'hui.

- BSCR (Basic Solvency Capital Requirement) :la somme de tous les risques de l'assureur combinés intelligemment (sans juste les additionner).

- COC (Cost of Capital):le "loyer" que coûte le fait de garder du capital de côté pour les imprévus. Fixé à 6% par an.

- Cout normal/Normal Cost:combien coûte chaque année à l'entreprise les droits à la retraite que ses salariés viennent de gagner.

- Embedded Value :la vraie valeur d'une compagnie d'assurance, en comptant aussi les profits futurs de ses contrats déjà signés.
- Marge de risque (Risk margin):un coussin de sécurité ajouté au Best Estimate, au cas où l'estimation se révélerait fausse.

- Marge de Solvabilité:l'ancien indicateur de capital minimum,utilisé avant 2016, remplacé aujourd'hui par le SCR

- MCR (Minimum Capital Requirement ):la ligne rouge absolue de capital. En dessous, l'assureur risque de perdre son agrément.

- PAF (Provision pour aleas financier):l'argent mis de côté pour tenir les promesses de taux garanti faites aux assurés, même si les marchés ne rapportent pas assez.

- Ratio Combiné : mesure si l'activité d'assurance est rentable.Au-dessus de 100%, l'assureur perd de l'argent sur son activité pure.

- ROA (Return On Asset)/ RONA(Return On Net Asset)/ ROTA(Return On Total Asset):combien de profit l'entreprise génère par rapport à ce qu'elle possède.

- ROE(Return On Equity): combien gagnent les actionnaires par rapport à l'argent qu'ils ont investi dans la compagnie

- ROI(Return on Invest): pour chaque euro investi, combien on en récupère.

- RORAC(Return on Risk Adjusted Capital):comme le ROE, mais qui tient compte du niveau de risque pris pour gagner cet argent

- S/P ou P/C :sur chaque euro de prime encaissé, combien part en sinistres.
- SCR (Solvency Capital Requirement):le capital que l'assureur  doit garder de côté pour pouvoir encaisser un très mauvais événement sans faire faillite.

## Description de mon assistant 
Cela me permettra de definir la personnalité et les limites de mon assistant .
- **Role de l'assistant** :Il est principalement destiné à des actuaires ou des étudiants en étude d'actuariat. Il les aidera dans leur taches et leur donnera des informations sur des concepts actuariels.

- **Son comportement conversattionnel** :l'assistant doit être courtois et professionnel. Si une question est ambiguë ou manque  de précision, il doit poser une question de clarification plutôt que de deviner ce que l'utilisateur veut dire.

- **Langue** : l'assistant répond toujours en français, sauf si l'utilisateur lui demande explicitement de répondre en anglais.

- **Ce qu'il peut affirmer avec confiance**: Il peut affirmer avec confiance les definitions ,les concepts et les formules générales de calcul.

- **²Ce qu'il doit faire avec prudence**:aborder avec delicatesse les questions complexes en tenant compte de la conformité réglementaire (par exemple : la solvabilité 2)

- **Ce qu'il ne doit jamais faire**: inventer des reponses ou donner de faux chiffres ou faux resultats de calculs avec assurance .il doit clairement indiquer son incertitude et inviter l'utilisateur à vérifier auprès d'un actuaire qualifié ou d'une source officielle.

- **Format des réponses** : pour chaque indicateur expliqué,l'assistant fournit toujours une définition courte, la formule si applicable, et un exemple chiffré concret.Il pourra détailler la definition si l'utilisateur le lui demande.

-  **Citation des sources** : à chaque réponse sur un concept ou une règle, l'assistant doit indiquer l'organisme ou la source de référence (EIOPA, ACPR, Institut des Actuaires et ) pour permettre à l'utilisateur d'approfondir s'il le souhaite.

## Prompt système (brouillon)
Pour le prompt système je vais réécrire les grands points de la description de mon assistant mais en m'adressant directement à lui.
- **Ton role** :Tu es principalement destiné à des actuaires ou des étudiants en étude d'actuariat. Tu les aideras dans leur taches et leur donneras des informations sur des concepts actuariels.

- **Ton comportement conversattionnel** :Tu dois etre courtois et professionnel. Si une question est ambiguë ou manque  de précision, Tu dois poser une question de clarification plutôt que de deviner ce que l'utilisateur veut dire.

- **Langue** : Tu réponds toujours en français, sauf si l'utilisateur te demande explicitement de répondre en anglais.

- **Ce que tu peux affirmer avec confiance**: Tu peux affirmer avec confiance les definitions ,les concepts et les formules générales de calcul.

- **²Ce que tu dois faire avec prudence**:Tu dois aborder avec delicatesse les questions complexes en tenant compte de la conformité réglementaire (par exemple : la solvabilité 2)

- **Ce que tu ne doit jamais faire**: Tu ne dois jamais inventer des reponses ou donner de faux chiffres ou faux resultats de calculs avec assurance .Tu dois clairement indiquer ton incertitude et inviter l'utilisateur à vérifier auprès d'un actuaire qualifié ou d'une source officielle.

- **Format des réponses** : pour chaque indicateur expliqué,tu dois fournir toujours une définition courte, la formule si applicable, et un exemple chiffré concret.Tu pourras détailler la definition si l'utilisateur le lui demande.

-  **Citation des sources** : à chaque réponse sur un concept ou une règle,Tu dois indiquer l'organisme ou la source de référence (EIOPA, ACPR, Institut des Actuaires et ) pour permettre à l'utilisateur d'approfondir s'il le souhaite.

## Affiner le prompt système
Je decide donc de faire une liste de questions pour verifier chaque grand point de mon prompt système et ensuite aporter des modifications.

**Question 1**: Explique-moi la prime pure en actuariat

Après l'inclusion du prompt system dans mon script et après l'avoir exécuté . 

**Resultat** :le comportement conversationnel,le structure des reponses,les sources, les formules et les définitions etaient "ok"

Mais J'ai remarqué qu'il y avait des emojis dans les reponses. 
**Modifications**:J'ai donc ajouter au **comportement conversationnel**:Evite d'utiliser les emojis ,garde un ton sobre et professionnel adapté à un contexte technique et réglementé

**Question 2**: May you explain the utility of ROA ?

Cette question nous permettra de verifier le volet **Langue** et aussi sa reaction **l'ambiguité des questions**
**Resultat**: il a en plus d'avoir respecté les instructions de la langue et m'avoir demandé d'etre plus précise au niveau de mon indicateur,a respecté toutes les autres instructions en tenant aussi compte de la modification apporté ci dessus .
Pour cette question j'ai aussi fait des relances comme "approfondis cette partie" pour verifier s'il respecte le format des reponsses . Mais ce qui me pose problème c'est que bien qu'il respecte le format de reponse , si quelqu'un veux des informations sur l'utilité d'un indicateur ,ça devrait etre prioritaire par rapport à la definition ou par à la formule de calcul.
**Modifications**:J'ai demandé à l'assistant d'utiliser le format de reponse par défaut que lorsque les question sont générales et lorsque les questions sont précise qu'ils les traitent prioritairement sans forcement tenir compte du format par defaut.

**Question 3**: Quel est le SCR de la compagnie AXA 
Comme instructions je lui ai demandé de n'inventer aucun chiffre ,il est donc censé ne rien donné comme chiffre car il ne doit pas me donner des chiffres obsolètes.
**Resultat**:Il explique clairement qu'il ne peux pas fournir de chiffres au sisque de se tromper et explique comment pouvoir yrouver les chiffres que je veux . Merveilleux ,Aucunes mofications à faire .

**Question 4** : Quand est ce que la coupe du monde se termine ?
Je lui pose une question hors dommaine pour savoir s'il a bien compris son role et s'il sait quel genre d'utilisateurs s'adressent à lui .
**Resultat**:Il repond en disant de se tourner vers un moteur de recherche car c'est pas son role . Pas besoin de modification car il fait exactement ce qui lui est demandé

**Question 5** :Quel est le SCR exact que doit avoir une compagnie d'assurance non-vie avec 50 millions d'euros de primes ?
C'est une question piège pour savoir s'il me dira que c'est pas suffisant et s'il abordera la question de façon délicate 
**Resultat** : sa reponse *Je dois être transparent avec vous : **il m'est impossible de vous donner un SCR exact** à partir de la seule donnée du volume de primes....* .Il repond bel et bien comme il le fallait et en donnant des recommandations et comment obtenir un SCR fiable.Aucune modification nécessaire 

**Question 6**: quais ce q'un mage de risq ?
Je mets expressement des fautes dans ma question pour savoir comment reagira mon assistant 
**Resultat**:RAS il donne ce qu'il pense etre juste et demande la confirmation de l'utilisateur .

# INTERFACE STREAMLIT
## Intégration API dans Streamlit

J'ai créé le fichier chatbot_v1.py qui est le debut de la vraie interface 
de mon assistant. Contrairement à test_api.py qui s'executait dans le terminal,
chatbot_v1.py s'affiche dans le navigateur grâce à Streamlit.

## Ce que j'ai appris
- st.set_page_config : permet de configurer le titre et la mise en page de l'app
- st.chat_input : zone de saisie qui s'affiche en bas de page comme un vrai chat,
  envoie le message quand on appuie sur Entrée sans avoir besoin d'un bouton séparé
- st.chat_message : affiche les messages avec des bulles différenciées 
  pour l'utilisateur et l'assistant
- st.spinner : affiche un indicateur de chargement pendant l'appel API
- st.sidebar : panneau latéral gauche pour les informations du projet

## CSS dans Streamlit
On peut personnaliser l'interface avec du CSS via st.markdown avec 
unsafe_allow_html=True. J'ai modifié la couleur de la sidebar, 
du fond de page et de la zone de saisie.

## Bug rencontré et corrigé
Le message "Veuillez écrire une question" s'affichait au lancement 
à cause du else relié au if question. En supprimant ce else, 
le message n'apparaît plus qu'au bon moment.

## st.session_state
Tiroir spécial de Streamlit qui conserve les données entre les 
réexécutions. Sans lui, l'historique repart à zéro à chaque interaction.

## Bug résolu — ordre d'affichage
La boucle for doit être APRÈS le if prompt. Si elle est avant, 
il y a un conflit d'affichage qui efface les messages précédents.

## Structure qui fonctionne
1. if prompt := st.chat_input() : traite et sauvegarde dans session_state
2. for msg in st.session_state.messages :affiche tout l'historique

# RAG (Retrieval Augmented Generation)
Il va permettre a l'assistant d'avoir accès à des documents internes et baser ces reponses sur ceux-ci lorsqu'il lui sera demandé.

Cette methode passe par plusieurs etapes:
## Les chunks
Lorsque les  documents seront uploadé vu que le LLM ne peux pas lire des longs documents ,ils seront découpé en plusieurs morceaux qui ont du sens appélés *Chunks*

## Les embeddings 
Le LLM ne comprends que les chiffres et pas les mots vu que c'est un reseau de neurones. Les Chunks seront donc transformé en vecteurs que le LLM pourra comprendre.

## La base vectorielle et recherche semantique
Les embeddings seront ensuite rangés dans une base appélée *base vectorielle* qui permettra de comparer le vecteur de la question aux differents vecteurs de ceux de la base vectorielle et retenir ceux qui sont les plus proches. C'est ainsi que le LLM comprendra dans quelle Chunk se servir afin d'avoir la reponse à la question.

## Premier RAG fonctionnel

### Bibliothèques installées
- langchain-community : charge les documents PDF
- langchain-text-splitters : découpe le texte en chunks
- faiss-cpu : stocke et recherche les vecteurs (créé par Facebook)
- sentence-transformers + langchain-huggingface : transforme les 
  chunks en vecteurs (gratuit, fonctionne en local, supporte le français)

### Ce qu'on a fait
1. Chargé le PDF ACPR-AMF 2025 (24 pages → 59 chunks)
2. Créé la base vectorielle FAISS avec de vrais embeddings HuggingFace
3. Testé la recherche sémantique : une question → 3 chunks proches retrouvés
4. Connecté au LLM Claude : les chunks deviennent le contexte de la réponse

### Observation importante
Le LLM a répondu honnêtement "pas disponible" quand le bon chunk 
n'était pas dans les résultats. C'est le comportement attendu — 
il ne doit pas inventer.

### La chaîne RAG complète
PDF ->chunks -> vecteurs FAISS ->recherche sémantique -> contexte LLM ->réponse

# FINALISATION DU PROTOTYPE
Je crée le fichier final du prototype de mon assistant *app.py*
Dans ce code on va separer les trois fonctionnalités de l'assistant pour rendre l'interface fluide à utiliser . Ainsi pour chacune des ses fonctions ,un prompt bien defini sera fait afin de reguler les agissements de l'assistant

# TEST DES LIMITES DU PROTOTYPE ET AMELIORATION
## Test des fonctions de l'assistant 
## Fontion 2
### Test 1 : Fonction 2 sans document chargé
Question posée : "Combien de publicités ont été analysées en 2025 ?"
Résultat : L'assistant refuse de répondre et invite à charger un document 

### Test 2 : Document volumineux (7MB - 170 pages)
Résultat : 529 chunks créés, indexation réussie sans erreur
L'interface reste stable pendant l'indexation 

### Test 3 : Question sur un grand document (mémoire actuariel 170 pages)
Question : "De quoi parle ce mémoire et qui l'a écrit ?"
Résultat : Sujet bien identifié. 
Auteur non trouvé : l'assistant l'indique honnêtement sans inventer ✅
####  Observation importante sur le RAG
La formulation de la question influence la qualité des résultats.
Première question "qui l'a écrit ?" → auteur non trouvé
Deuxième tentative :auteur trouvé (Mulah MORIAH)
Conclusion : le RAG est sensible à la façon dont on pose la question.

### Test 4 : Changement de fonction en pleine conversation
Résultat : La conversation repart bien de zéro à chaque changement 
de fonction 

## Fonction 3 : Aide au reporting 
Je vais vérifier si l'aide au reporting marche réellement 
Ma question :*Aide-moi à rédiger l'introduction d'un rapport ORSA pour une compagnie d'assurance non-vie*
Résultat : Introduction complète et conforme Solvabilité II générée,avec sections structurées et points d'attention pour validation.


## Amelioration de l'ergonomie 
- Rendre clairement visible les trois fonctions et la sélection est évidente avec le bouton rouge et le "Mode actif" en dessous
### Amélioration : upload multiple de documents
- k augmenté à 8 pour couvrir plusieurs documents
- Source du document ajoutée dans le contexte
- Test avec 3 documents : résultats corrects 

### Ajout d'un historique de conversation 

Chaque conversation est sauvegardée avec un nom et une date
L'utilisateur peut voir la liste de ses conversations passées
Il peut en sélectionner une pour la continuer