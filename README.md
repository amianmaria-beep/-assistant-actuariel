# PROTOTYPE ASSISTANT ACTUARIEL

## BUT DU PROJET
Mise en place d'un assistant actuariel capable d'expliquer les indicateurs actuariels ,de faire des resumés de portefeuille et d'aider à la production de reportings 

## TECHNOLOGIES UTILISEES 
- Large Language Model (LLM)
- API (anthropic claude)
- Retrieval-Augmented Generation (RAG)
- Streamlit 

## STRUCTURE DU PROJET
- **src/** : code source principal (app.py, versions intermédiaires chatbot_v1, v2, rag)
- **docs/** : documents actuariels utilisés pour les tests (PDF, Excel)
- **tests/** : scripts de test et observations (rag_test.py, test_api.py, tests_api.md)
- **notes.md** : journal de bord technique du projet


## INSTALLATION
1. Cloner le projet
2. Créer un fichier .env avec votre clé API Anthropic :
   ANTHROPIC_API_KEY=votre-clé-ici
3. Installer les dépendances :
   pip install streamlit anthropic python-dotenv langchain 
   langchain-community langchain-anthropic langchain-text-splitters 
   langchain-huggingface langchain-core faiss-cpu pypdf 
   sentence-transformers pandas openpyxl

## COMMENT LANCER L'APPLICATION
streamlit run src/app.py

## LES 3 FONCTIONS
- Fonction 1 : Expliquer les indicateurs actuariels (SCR, BEL, IBNR, 
  ratio combiné...) via le LLM
- Fonction 2 : Analyser des documents PDF/Excel via le RAG
- Fonction 3 : Aider à la rédaction de reportings réglementaires 
  (ORSA, SFCR) avec possibilité d'upload de données

## LIMITES ET PERSPECTIVES D'ÉVOLUTION
- Historique perdu au rechargement de la page (limitation Streamlit)
- Gestion des tableaux dans les PDF non optimale
- Recherche hybride BM25 + FAISS non implémentée
- Pas de système d'authentification multi-utilisateurs
- Perspective : persistance en base de données, déploiement cloud

## HISTORIQUE DU DEELOPPEMENT 
- Creation d'une clé API 
- Securisation de la clé API 
- structuration du projet en sous-dossiers (src,docs,tests)
- installation des bibliothèques anthropic et python-dotenv
- Appel d'API via un script python
- Gestion et test des paramètres de la requete
- Gestion des erreurs potentiel pouvant survenir lors de l'appel de l'API 
- Recherche sur les différents indicateurs actuariels
- Reflexion sur la personnalité et les limites de l'assistant 
- Ecriture du prompt système 
- Amelioration du prompt système après les differents tests 
- Création de l'interface Streamlit (chatbot_v1.py)
- Intégration de l'API Anthropic dans l'interface
- Personnalisation visuelle (CSS, sidebar, message de bienvenue)
- Gestion des erreurs et du spinner dans l'interface
- Ajout de la mémoire de conversation avec st.session_state (chatbot_v2.py)
- Résolution d'un bug d'affichage lié à l'ordre des composants Streamlit
- Implémentation du RAG : chargement PDF, découpage en chunks,base vectorielle FAISS, embeddings HuggingFace, connexion au LLM
- Test du RAG avec un doc PDF (5 questions posées, 4/5 correctes)
- Intégration du RAG dans Streamlit : upload PDF depuis la sidebar
- Indexation automatique avec FAISS et HuggingFace et affichage des sources dans Streamlit
- Création du fichier final app.py intégrant les 3 fonctions de l'assistant
- Sélecteur de fonction dans la sidebar avec mode actif visible
- Réinitialisation automatique du chat lors du changement de fonction
- Test des differentes fonctions de l'assistant
- Amelioration de l'experience d'upload de fichier 
- Mise en place d'un historique 
- Mise en place d'un cache pour accélérer les interactions 
- Support des fichiers Excel en plus des PDF (tables actuarielles,matrices de sinistralité...)
