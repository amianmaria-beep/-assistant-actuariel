# DOCUMENT DE SUIVI DE MES RESULTATS ET OBSERVATIONS APRES MES DIFFERENTS TEST

  ## Premier script de travail 
     J'observe qu'après avoir envoyé ma requete **"Qu'est-ce que le SCR en Solvabilité II"** ,le serveur m'a répondu et la reponse etait moyennement longue avec assez de detail mais le problème c'est que la réponse s'est arreté avnt d'etre complètement terminée. 
     
     J'ai donc décidé d'augmenté la variable max_tokens de 1024 à 1500 pour savoir si j'aurai une réponse entière et complète.
     Après observation,on remarque que la reponse obtenu n'est pas forcement plus longue et detaillée que la première mais est complète ,ce qui signifie que le LLM a adapté la reponse afin d'avoir une reponse ni trop lonngue et ni trop courte afin d'avoir une reponse complète.

     **max_tokens=1500 : c'est idéal**

     J'ai ensuite chercher à connaitre le nombre de tokens d'entrée , de sortie ,le nombre de tokens total utilisé par le LLM avec de savoir si mes 1500 de max_tokens ont été bien calibré pour de bonnes reponse.J'ai aussi cherché à connaitre la cause de l'arret : si la reponse est terminé ou si le max de tokens est atteint .
     j'ai eu commme résultat:Tokens en entrée : 25  (ma question fait seulement 25 tokens)
                             Tokens en sortie : 718 (ma reponse fait 718 tokens)
                             Total tokens : 743 (ma reponse plus ma question font 743 tokens)
                             Modèle utilisé : claude-sonnet-4-6 (modèle utilisé est bien celui que j'ai demandé)
                             Raison d'arrêt : end_turn  (la raison d'arret est bel et bien le fait que la reponse est terminée)

     **CONCLUSION**:max_tokens=1500 est un bon calibrage


     ## Test 1: la temperature 
     Je change de question et cette fois ma quetsion est **"Explique-moi la prime pure en actuariat"**.
     J'ajoute une paramètre de plus dans mon script qui est :temperature .

     - Avec temperature=0,lorsqu'on pose la question plusieurs fois a Claude ,ces reponses sont les memes à seulement quelques mots de differences ,on peut donc dire qu'il est assez prévisible .Ici il agit comme un professeur ,des reponses précises.
     - Avec temperature=1,lorsqu'on pose la question plusieurs fois a Claude ,ces reponses sont plus fluides et variée ,comme s'il prend plus de liberté dans le choix de ses mots.
