Title: JS et Programmation Fonctionnelle - Part 1
Date: 2016-09-13 12:20
Tags: Fonctionelle, Javascript
Category: Programmation

Je vais me lancer sur une série d'articles concernant la programmation fonctionnelle, appliquer au monde JS. L'objectif pour moi est de préparer, à terme, une présentation sur le sujet. Aujourd'hui, je vais donc commencer par les bases : c'est quoi au juste la programmation fonctionnelle.

Du rôle de la fonction
----------------------

Fonctionnelle comme fonction. Mais la fonction dont on parle ici correspond-elle au mots-clés 'function' de notre langage ? Presque, mais pas tout à fait. En fonctionnel, une fonction est un élément **prévisible** qui prend des paramètres entrants et qui renvoies une **nouvelle** valeur. Cela implique que :

- Les paramètres entrants ne sont pas modifiés
- Le retour de la fonction est un nouvel objet ou une nouvelle valeur
- Tout appel avec des paramètres identiques renvoi le même résultat

Les avantages de ce type de fonction sont multiples :

- Meilleure testabilité : elles ne dépendent pas d'un état.
- Meilleure reproductibilité : si l'on trouve un bug, il suffit de rappeler la fonction avec les mêmes paramètres pour obtenir les mêmes résultats.
- Meilleurs "scalabilité" : on ne mute pas les objets, il n'y aura donc pas de problème de concurrences sur des threads différents.

De l'immutabilité
-----------------

Je viens de glisser le point dans le dernier avantage, mais l'un des grands principes de la programmation fonctionnelle est de tirer à maximum parti d'objet immutable : c'est-à-dire un objet qui ne peut pas être modifié. La conséquence, c'est qu'à chaque fois que l'on veut modifier un objet, nous allons créer une nouvelle instance complètement indépendant de l'objet.

Encore une fois les avantages sont multiples :

- La scalabilité, comme abordé plus haut.
- La limitation des effets de bord : vu que l'on ne modifie pas un objet, l'on ne risque pas de modifier par inadvertance un objet qui aurait été transmis à d'autres parties de l'application.

Bien entendu, la plupart des applications ne peuvent pas être 100% immutable : l'idée est d'isoler au maximum les endroits où un état est mémorisé et de ne faire ces mutations que de manières conscientes et complètement volontaire.

De la programmation déclarative
--------------------------------

La programmation impérative met en avant le "comment" : ajoute 1 au compteur, passe à l'élément suivant, modifie tel caractère, ... L'objectif de la programmation déclarative est de s'attacher au "quoi". Pour s'approcher au maximum de ce style, la programmation fonctionnelle, mais en avant non pas les données, mais les traitements : le but est de décrire des chaînes de traitement qui vont s'appliquer aux données.

Prenons l'exemple très simple d'une somme. En impératif :

'''
function sum(vals) {
var total = 0;
for(var i = 0; i < vals.length; i++) {
total = total + vals[i];
}
return sum;
}
'''

Et en fonctionnelle :

'''
function sum(vals) {
return vals.reduce(add);

function add(e1, e2) {
return e1 + e2;
}
}
'''

Le code est équivalent, mais dans le second cas, il décrit l'intention : réduire la liste en additionnant ses éléments.

Pour résumé
-----------

La programmation fonctionnelle a pour objectif :

- d'améliorer la lisibilité du code (style impératif).
- de faire du code plus facile à tester et à debugger (pas d'effet de bord).
- d'être plus résistant aux concurrences.

Par contre, l'immutabilité est une contrainte qui demande une certaine discipline à l'usage.

Fonctionnelle versus POO
------------------------

Souvent, ces deux paradigmes de programmations sont mis en oppositions. Faut-il faire de la POO, ou faut-il faire du fonctionnelle ? Aujourd'hui, je pense sincèrement qu'il faut faire les deux :

- La POO permet de bien structurer son application et d'y faciliter la navigation
- Le fonctionnelle permet de rendre son code plus lisible

Utiliser les deux, c'est avoir accès aux forces de chacun. Pourquoi se priver ?

