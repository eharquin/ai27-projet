./python crocomine.py

Test de la taille de la carte pour déterminer comment on joue:
- Si la carte est trop grande, on joue de manière complètement aléatoire pour aller vite mais ce n'est pas fiable du tout.
- Sinon on joue en se basant sur la base de connaissance en l'alimentant avec toutes les informations qu'on récupère,
on teste tous les cas possibles et on prend en compte celui qui renvoie le plus petit nombre de modèle. C'est long mais très fiable.
