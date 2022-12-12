# ball_detection

# Algorithme de vision

Le pipeline de l'algorithme de vision est constitué comme suit :
    - D'abord l'image est convertie en HSV pour permettre d'égaliser la saturation vue que les couleurs dans les images sont très jaunâtres
    - Nous en profitons pour utiliser la Hue pour faire un masque qui sélectionne le terrain et faire une bounding box. Cela permet de recarder l'image ensuite pour éliminer le background.
    - Une fois l'image égalisée et recadrée obtenue, nous la convertissons en niveaux de gris pour pouvoir faire de la détection de contour. Nous en profitons pour appliquer un flou gaussien pour éliminer le bruit que les herbes pourraient générer sur la détection de contour.
    - En suite, l'algorithme de Canny est utilisé pour détecter les contours, suivit d'une dilatation pour accentuer ces contours.
    - Enfin, l'algorithme de Hough est utilisé pour détecter les cercles dans ces contours.

Pour lancer le modèle il faut faire : python main.py chemin/vers/image

# Vérification des résulats 

Afin de vérifier les résultats obtenus par l'algorithme de vision, il nous faut saisir manuellement le centre du ballon puis le rayon du ballon sur chaque image. Nous stockons ces valeurs dans deux listes puis nous comparons les points qui appartiennent au disque saisi manuellement et les points qui appartiennent au disque trouvé par l'algorithme.

Pour lancer la vérification, il faut éxécuter le programme. Ainsi il graphique représentant le pourcentage de correspondance des cercles en fonction des images apparaitra. Ainsi, que la moyenne de ces pourcentages. Le programme ne s'effectue que sur la première bases d'images (log1).