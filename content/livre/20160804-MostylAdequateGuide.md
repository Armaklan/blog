Title: The Mostly Adequate Guide to FP
Date: 2016-07-10 23:20
Tags:  Critique, Informatique, Fonctionelle, Javascript
Category: Lectures

En continuant mes recherches a propos de programmation fonctionnelle en javascript, je suis tombé sur un ouvrage disponible gratuitement : [The Mostly Adequate Guide to FP](https://drboolean.gitbooks.io/mostly-adequate-guide/content/). Disponible en ebook ou pour une lecture «en ligne», ce livre d’environ 150 pages abordent les différents aspects de la programmation fonctionnelle de manière plutôt didactique.

Au sommaire : currying, composition, monades et applicative. A mon sens les explications sont un peu moins facile à appréhender que celle-présente dans «Functional Programming in Javascript» mais elles sont tout de même facile à suivre. 

Mention spéciale pour le chapitre sur la composition que je trouve vraiment très complet. Ici l’auteur nous présente vraiment une autre manière de développez et d’agencer nos fonctions. Les exemples donnés sont vraiment très parlant et illustre l’intérêt de cette approche. Je pense notamment à des déclarations comme celle-ci qui sont un exemple de concision : 

```
var loudLastUpper = compose(exclaim, toUpperCase, head, reverse);

loudLastUpper(['jumpkick', 'roundhouse', 'uppercut']);
//=> 'UPPERCUT!'
```

Après la lecture de ces deux ouvrages, me voilà complètement armée pour passer à la pratique ! Et pour m’échauffer, j’ai suivi les exercices de NodeSchool sur le sujet  ( [«functional javascript»](https://github.com/timoxley/functional-javascript-workshop) ). Ces exercices n’explore pas la composition ni les monades, mais le reste y passe.

Au passage pour ceux qui ne connaisse pas (et c’étais mon cas il y a quelques jours), NodeSchool est un site vraiment sympa bourré de «tutoriel» sous la forme d’exercice+corrigé. Vraiment très sympa :)