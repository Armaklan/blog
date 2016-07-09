Title: Seul sur mon code source
Date: 2016-07-09 08:00
Tags: Informatique, Humeurs
Category: Programmation

Au boulot, pendant presque deux ans, j'ai été seul sur mon code source. Je ne travaillais pas seul, mais mes collègues s'occupaient du backend pendant que je construisais la partie front-end Angular de l'application. Bref, j'avais mon source, ils avaient le leur, et nous n'avions qu'un seul point réel de communication : l'API. Et fatalement arriva le jour où, pour des raisons diverses, des collègues durent mettre les mains dans le code source et là... C'est le drame !

J'exagère bien entendu : j'ai une certaine exigence dans la forme de mon code source qui le rend assez facile à lire et a appréhender par de nouvelles ressources. Je suis notamment un acharné du découpage en sous-fonction. Mais malgré cela, je me suis rendu compte que mon code souffrait de quelques problèmes gênants : notamment des comportements qui étaient devenu implicite. Moi, il ne me posait aucun problème, mais pour les nouveaux venus ces comportements avaient l'apparence de magie noire... Et la magie, on ne la comprend pas, et on ne la debuggue pas.

Un exemple ? Je travaille sur du Angular 1 et une poignée de mes services applicatifs reviennent dans presque tout les controllers. Pour alléger un peu le nombre de dépendance injecté en entrée de mes controllers et donc rendre le "spécifique" plus visible, j'ai décidé de placé ces services directements via le `$rootScope`. Ainsi mes controllers en héritent automatiquement.

Bonne solution ? Avec le recul, je pense que non : aujourd'hui, les autres développeurs ont des difficultés à savoir ce qui est réellement exposé et surtout, où ils sont réellement exposés. Pour la même problématique, j'aurai tout simplement pu utiliser un service Facade qui se serait fait le relai : je n'aurais alors eu qu'une seule dépendance commune et n'importe qui aurait pu relire ce service. Le comportement aurait donc été explicite.

Il aura fallu que d'autres personnes touchent au code pour que je me rende compte de ce souci. J'ai rencontré le même souci avec jdRoll : difficile à quelqu'un de s'intégrer dans ce code où j'ai été trop seul, trop longtemps. Bref, l'application aurait probablement gagné en qualité si nous avions été deux sur le source, même si le second développeur avait été moins expérimenté que moi. Et je ne parle même pas ici des interêts d'une bonne relecture ! ;)

Et la prochaine fois que je serai seul, je garderais en tête cette leçon : éviter l'implicite.

