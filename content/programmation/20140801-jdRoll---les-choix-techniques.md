Title: Retrospective jdRoll - Les choix techniques
Date: 2014-08-02 10:46
Tags: Projets, Méthodes, jdRoll, Framework, Outils, Informatique
Category: Programmation

Après avoir parler de ma façon de travailler sur ce projet, il est temps de revenir sur les choix techniques du projet :

- __Git__ et Github
- Base relationnelle et __Mysql__
- Php et Framework __Silex__
- HTML statique et __Twig__
- __Bootstrap__

Auxquel je rajouterai deux points d'outillage, qui a évolué depuis :

- __Composer__, Bower, and co...
- Éditeur de texte et IDE

Avant tout chose, expliquons les critères qui ont conduit à mes choix :

- Produire __rapidement__ un début d'application fonctionnel
- __Déployer__ facilement sur des hébergements standards
- Facilité l'arrivé de __contributeurs__ supplémentaires

Git et Github
-------------

Utiliser un gestionnaire de version me semblait déjà à l'époque indispensable :

- Je travaille sur plusieurs PC : il me faut donc un moyen de synchroniser.
- Je voulais ouvrir la porte à des contributeurs : donc rester facilement accessible.
- L'open source était pour moi un argument important.
- Je savais que j'allais tester des choses et finalement les abandonnées.

À titre professionnel, j'utilisais déjà SVN et avais déjà intégré les principes de la gestion de version.

Ok pour utiliser un outil, mais pourquoi git et github ?

- Quelques clics suffisaient pour avoir un dépôt __prêt à être utilisés__.
- Github avait le vent en poupe.
- Github offre une bonne __visibilité__ public et offre des outils complémentaires (bugtracker, wiki).
- Je voulais m'essayer au célèbre Git.

Et au final, ce choix ?

- Github est vraiment simple d'utilisation
- J'ai utilisé pendant presque un an git en mode svn (push-commit)
- Aujourd'hui, je commence à peine à entrevoir la __réelle puissance de l'outil__.

Donc oui, c'était un bon choix, mais j'aurai dû me pencher sur sa vraie utilisation bien plus tôt !

Du coup, mon SVN du boulot me parait, de plus, en plus fade...

Pour résumer :

- Git et Github : Choix identique aujourd'hui

Base relationnelle et Mysql
-------------------------

Certains collègues m'ont vendue à de nombreuses reprises les avantages du NoSQL et de produit comme __MongoDB__. Je dois avouer que le NoSQL à des arguments de poids : une flexibilité et une rapidité à toute épreuve. Alors si je recommençais jdRoll : NoSql ? En fait... Non...

- Malgré tout, j'ai des habitudes relationnelles bien ancrées dans ma façon de penser.
- On trouve du relationnel chez tous les hébergeurs, du NoSQL (quel que soit le produit) est encore rare.
- Je n'arrive pas à estimer le gain réel sur un projet comme jdRoll (où je ne suis pas en gros volume de données).

Il est certain que je prendrai le temps de jouer avec MongoDB dans un futur proche, mais aujourd'hui, je ne suis pas encore convaincu.

Et pourquoi Mysql ? Ici, l'argument de l'hébergement revient : on trouve Mysql partout. Aujourd'hui, la base de donnée fait son job. Et demain ? Si je devais refaire le projet, j'opterais surement sur __postgresql__. On trouve assez aisément un hébergement l'offrant, et j'ai le sentiment qu'il ferait mieux que mon mysql actuel. Cela dit, je n'ai rien à reprocher à Mysql et le choix me semble toujours valable.

Pour résumer :

- Base relationnel : Choix identique aujourd'hui.
- Produit : surement postregresql en lieu et place de Mysql.

PHP et Silex
------------

Php n'est pas mon langage de prédilection. Il n'est même pas un langage que j'apprécie réellement. S'il n'y avait pas de contrainte d'hébergement, je retournerais sans vergogne au python accompagné d'un framework tel que [Flask](http://flask.pocoo.org/). En dehors de préférence purement esthétique, bah... Php fait son job et me permet d'obtenir des temps de réponses correctes, avec une consommation de ressources plutôt faible... Donc ce n'est pas un mauvais choix, même si ce n'est pas le meilleur.

Quand à Silex ?

Il y a d'abord le choix d'un __micro-framework__, et là je redit oui et encore oui !

- Montée en compétence facile
- Je construis mon cadre comme je l'entends, pas comme d'autre l'ont voulu (Je dis ça en rapport à symfony qui est trop... Encombrant !)
- Performance correcte sans recourir à des mécanismes de cache (Il me reste donc des améliorations de performance possible ! ^^)

Alors demain, Silex ?

Il y a une chose qui change un peu la donne : j'ai découvert il y a peu [__Phalcon__](http://phalconphp.com/). Ce framework est composé d'une extension C et offre donc des performances très très bonne. De plus, même si c'est un framework complet, il semble aisé à personnaliser et à adapté à ses besoins. Mes projets iront donc surement sur ce nouveau choix !

Pour résumer :

- PHP : Oui, pour le coté abordable et courant.
- Framework : J'irais plus probablement sur Phalcon

HTML statique et Twig
---------------------

Cette dernière année, mes compétences Front-End ont largement augmenté. J'ai redécouvert le JS et surtout des technologies comme Angular. Je suis convaincu que les applications de demain devraient utiliser majoritairement des framework front complet.

Utiliser du HTML quasiment statique et Twig est donc finalement le choix que je ne referai pas. D'ailleurs, ces derniers temps de l'ajax apparait de plus en plus dans le site pour rajouter le dynamisme qui était absent aux origines de jdRoll.

Twig est une bonne technologie : fiable et efficace. Par contre l'approche templating serveur est pour moi une approche dépassé qui n'offre pas autant de flexibilité que celle orienté coté client.

Pour résumer :

- Exit le templating serveur, vive Angular ;)

Composer, Bower, et Co
----------------------

Les outils sont apparus progressivement dans jdRoll :
- Au début, seul composer était présent pour les __dépendances__ Php.
- J'ai rajouté bower quelques mois plus tard pour les dépendances Web. La migration s'est faite assez facilement dans l'ensemble. Rien à redire, bower s'utilise simplement.
- Et plus récemment j'ai commencé à utiliser grunt pour minifier, mais aussi pour lancer le serveur de développement.

Le triptyque Composer, Grunt, Bower, et Npm fonctionnent bien, mais il a tout de même un coût : une complexité pour les nouveaux arrivants. J'ai cherché des solutions pour masquer ses outils derrière une sorte __d'interface "maître"__, mais je ne suis pas arrivé à quelque chose de satisfaisant pour l'instant.

Si certains ont des solutions magiques, je suis preneur !

Pour résumer :

- Conservation du tryptique (composer, bower, grunt) à défaut de solution "unique".

Bootstrap
---------

Vos compétences de graphistes sont réduites ? Vous n'êtes pas spécialement un as du CSS ? Vous voulez faire une interface agréable à l'œil à moindre coût ? Bootstrap est fait pour vous !

Honnêtement, Bootstrap est un outil assez magique : il suffit de l'appliquer correctement pour avoir un site plus qu'acceptable en terme de rendu. Qui plus est, le framework offre les outils pour faire du responsives : ça ne fait pas tout, mais ça aide sacrément !

Après si votre équipe comprend un designer, faite du vrai web sémantique et laissez votre designer travailler : vous aurez un résultat plus abouti, plus adapté à votre site et à son ambiance.

Pour résumer :

- Au vu de mes compétences, Bootstrap est devenu un incontournable

Editeur de texte et IDE
-----------------------

Quelques retours sur ce que j'ai pu utiliser au cours du projet, dans l'ordre d'apparition :

- __Eclipse :__ bon autant pour le Java l'IDE fait pas mal de chose, autant pour le Php c'est assez... Vide. Les fonctionnalités ne compensent pas la lourdeur, je l'ai très vite banni.
- __VIM __: ah vim ! Bardé de plugin, c'est un outil très puissant qu'on personnalise petit à petit. C'est vraiment un éditeur qui vaut le coup d'être apprivoisé.
- __Sublime Text :__ pour moi, Sublime Text, c'est un peu VIM avec une ergonomie plus actuel. Un éditeur que tu personnalises à fond pour répondre à ton besoin précis. Un have must à mon sens !
- __PhpStorm :__ depuis une dizaine de jours j'essaye PhpStorm via la version d'évaluation. C'est franchement un très bon produit ! Je retrouve des méthodes de __refactoring__ qui m'aurait bien aidé depuis le début. Je regrette juste les snippets qui sont tout de même moins facile d'accès.

J'ai posé une demande de licence OpenSource pour ce dernier. Si jamais je l'obtient, je switcherai à plein temps dessus :)

Pour résumer :

- Editeur : PhpStorm si possible. Sinon Sublime Text.
