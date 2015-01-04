Title: Retrospective jdRoll - Partie 1
Date: 2014-08-01 13:36
Tags: Projets, Méthodes, jdRoll, Informatique
Category: Programmation

Plus d'un an après le début de jdRoll, je me suis dit qu'il était temps de se poser et de faire une rétrospective du projet. Qu'est-ce qui a marché ? Quels ont été les disfonctionnements ? Qu'ai-je appris durant cette année qui pour moi a été riche en expérience.

## jdRoll aujourd'hui

Avant toute chose, un petit point sur la plateforme.

jdRoll c'est :

- Une grosse trentaine d'utilisateur quotidien (je parle d'utilisateur actif).
- En moyenne 3000 messages par mois.
- 39 parties actives à ce jour.

Pour moi, le résultat est au-delà de mes espérances initiales !

## Quick code, Quick prod

Au moment où les premières lignes de code de jdRoll ont été posé, je n'avais qu'un seul et unique objectif : mettre en production le plus vite possible, quelqu'en soit le cout.

Jusqu'à maintenant, quand je débutais un projet perso, je le faisais avec une approche professionnelle : poser une architecture carrée et propre, mettre en place l'outillage, préparer les builds, ... Soit, plusieurs jours de passé sans n'avoir rien produit de concret.

Pour jdRoll, la tendance a été autre : j'ai choisi un framework très lite pour ne pas avoir à l'apprendre, et j'ai de suite attaqué des écrans. Après quelques jours de dev mes premiers béta-testeurs commençait à cliquer partout et à me dire ce qu'il en pensait.

Lancer un projet en codant rapidement et sans prendre le temps de réflechir... Bon ou mauvais choix ? C'est en réalité une question difficile à répondre. Voici quelques éléments :

- __De la dure loi de la motivation__ : je ne sais pas pour vous, mais la motivation c'est comme un soufflé que tu sors du four, ça retombe bien vite. En partant vite, j'ai profité que le soufflé soit encore haut pour faire le maximum de fonctionnalités. Et quand le soufflé est retombé ? Simple, j'avais déjà des gens qui regardaient, commentaient, et me motivaient ! L'amour-propre et l'envie de ne pas décevoir ces quelques utilisateurs a suffit pour relancer la machine :)
- __Comme ça ? Non ? Alors comme ça ?__ : cet échange représente assez bien les premiers temps de la plateforme. Je faisais des essais, testais, récoltais les retours et idée et... Je cassais la features pour recommencer jusqu'à obtenir quelque chose de satisfaisant. Autant dire que vu que mon développement avait été fait à l'arrache, je n'avais guère de scrupule à le jeter !
- __Le refactoring éternel__ : C'est là que le bât blesse un peu, le code a eu besoin, et a encore besoin de beaucoup de refactorisation. Que ce soit du code fait trop salement, une mauvaise connaissance du framework, ou du code trop retravaillé, quand on décide d'aller vite il faut être prêt à en payer le coup plus tard. Aujourd'hui je mixte refactoring et nouvelles fonctionnalités pour assainir un peu le projet.

Avec le recul... Je pense que je referai ce choix sans hésiter ! Aujourd'hui reprendre mon code est presque agréable tant jdRoll est un petit bébé que j'ai envie de choyer... À l'époque prendre le temps de tout cadrer aurait tué le bébé dans l'œuf.

Pour un projet plus professionnel par contre, je pense qu'il faut tabler sur quelque chose d'intermédiaire : préparer quelque chose de propre et carré, mais rester simple pour garder une vélocité correcte.

## De la version à la feature

Étant donné mon objectif d'aller vite en production, parler de version applicative était un non-sens. Etant donné que mon objectif était d'aller vite en production et de tester rapidement, en cas réel, pourquoi attendre avant de mettre une fonctionnalité à disposition ? Par contre, je pensais revenir au bout d'un mois ou deux à une gestion plus classique : regrouper les fonctionnalités par version.

Et au final, un an plus tard ? Nous fonctionnons toujours par fonctionnalité ! Dès qu'une __fonctionnalité est prête, elle est déployée__ et annoncé aux utilisateurs ! En général ceux-ci se jettent dessus pour la tester et nous faire des retours qu'ils soient positifs, ou négatif.

Aujourd'hui, je n'imagine plus travailler autrement ! Dans le cadre d'un site unique, pourquoi donc ralentir le flux en travaillant par version ? En faisant de petites modifications à chaque fois :

- Je diminue fortement le risque de régressions réellement impactantes (au pire seul un petit périmètre présente un problème)
- Je peux prendre en compte les retours utilisateurs à moindre coût : au moment où les utilisateurs commentent, j'ai encore le code bien en tête. Au bout d'un mois ou deux, il faudrait que je prenne le temps de réapprendre le contexte.

Si je pouvais reproduire le même fonctionnement dans mon univers professionnel, je pense que de nombreux soucis seraient évité...

## Du un vers une équipe

Gailin si tu m'entends, quand tu m'as rejoint dans l'équipe de dev c'est le moment où j'ai le plus souffert de la vie de jdRoll ! Mais rassure toi, je suis content que tu soit encore là ! ^^

Pourquoi donc cette souffrance ?

- Aucune __documentation__
- Aucune __norme__ clairement définie
- Des automatismes humains non scripté (Je monte comment mon environnement ? )
- De mauvais réflexe bien implanté ! (besoin d'une base de donnée locale ? Hop, un dump de la prod)
- Un process... Inexistant !

En fait, l'arrivé d'un développeur m'a fait clairement ressentir tout ce que j'avais mis de côté. Il a donc fallu que je me retrousse les manches, que je l'accompagne, et que je commence à cadrer les choses... Pour information, je suis encore en train de faire se travaille, même s'il a fait un bond en avant ses dernières semaines.

Je me suis également aperçu que j'avais cédé à un autre biais : c'est un contributeur externe donc je ne vais pas trop l'embêter sur son code, mais s'il ne me plait pas. J'ai donc laissé passer du code que je n'aurai pas forcément accepté de moi-même. Grossière erreur ! Heureusement, je me rattrape depuis (hein Gailin ! :p)

## Le feedback au plus près de l'utilisateurs

__30 cerveaux valent mieux qu'un__. Je l'ai déjà dit à plusieurs reprises, je demande toujours le ressenti des utilisateurs sur les nouvelles fonctionnalitées. Nous avons également mis en place depuis le début un système de boite à idée permettant à chacun de proposer son évolution, quelle que soit la taille de la demande.

Résultat ? Des choses que je pensais faire au début sont encore dans la todo, alors que de nombreuses fonctionnalités à laquelle je n'aurait pas pensé ont été implémenter et améliore grandement l'expérience utilisateur. Constat encore plus étonnant : les modifications qui ont le plus amélioré la vie des utilisateurs étaient souvent... Négligeable. Genre une petite heure de développement et tout le monde étaient contents !

Bref, professionnel ou pas : un petit bouton permettant de rapporter des feedbacks ne coûte pas cher et pourra vous apporter beaucoup.
