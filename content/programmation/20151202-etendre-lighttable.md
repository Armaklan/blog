Title: Étendre LightTable
Date: 2015-12-02 13:00
Tags: Informatique, Outils, LightTable, ClojureScript
Category: Programmation

Pour moi, l'un des domaines où les éditeurs de textes sont aujourd'hui largement supérieur aux IDE est leur faculté à être personnalisé, à être étendu. Développer un plugin pour un IDE est souvent assez lourd, demande pas mal de connaissance, ... Au contraire, les éditeurs de textes sont souvent conçu pour être étendu. C'est bien entendu le cas de LightTable.

Voici un petit cas pratique que j'ai eu à implémenter : je crée une IHM Angular dans un projet à l'architecture assez complexe. Pour mes tests (hors-mock), je me retrouve à devoir :

- Faire mon cycle de build JS (géré par grunt, classiquement)
- Compiler une solution .NET et la déployer sur le serveur IIS
- Compiler une autre solution .NET et lancer un exécutable

Et biensûr, à chaque update je suis obligé de recommencer tout le cycle ! Donc si je résume : deux Visuals Studio lancé, des opérations rébarbative à faire de temps à autres, ... Pourquoi ne pas automatiser tout cela ! Nous somme, à mon sens, devant un bon candidat :)

## Phase 1 - Recherche des commandes

La plupart des tâches que je cherche à exécuter peuvent l'être en ligne de commande. La première étape est donc de chercher comment exécuter chacune de ses étapes de manières isolés :

- Mettre à jour le projet, car tant qu'à faire autant l'automatiser aussi : `svn update xxx`
- Arrêter l'exécutable lancé précédemment : `taskkill /F /IM xxx` (je suis sous windows)
- Compiler et déployer une solution .NET : `devenv  /rebuild debug xxx`
- Lancer l'exécutable... Bon là, pas besoin de vous faire un dessin ;)

Bon, premier soucis en mode dos : devenv rend la main avant terminé la compilation. En DOS, c'est la galère, programmatiquement par contre je pourrais aisément attendre la fin du process. Bref, j'ai toutes les info, plus qu'à introduire tout ça dans LightTable !

## Phase 2 - Où travailler ?

Où dois-je poser mon code pour mettre à disposition de nouvelle commande ? La réponse de LightTable est simple : dans un plugin ! Pour encore plus de simplicité, LightTable fourni par défaut un plugin "User" disponible pour intégrer votre code fait maison.

Etant donné que mon besoin est très spécifique à mon projet, je vais opter pour cette solution. Il me suffit donc de lancer la commande `Settings: User script` pour que le fichier de source s'ouvre dans l'éditeur ! Pratique :)

## Phase 3 - Un peu de ClojureScript

Bon, concrètement je vais devoir :

- Exécuter diverses commandes Dos
- Attendre que ces commandes soit terminé pour en exécuter d'autre

Je vais donc commencer par une petite fonction qui répond à ces deux besoins :

```
  ;; Exécute la commande fourni en paramètre et renvoi le "process"
  (defn cmd-execution [command]
    (println "Execution de : " command)
    (.exec (js/require "child_process")
           command
           (fn [err stdout stderr]
             (when (seq stdout) (println "STDOUT: " stdout))
             (when (seq stderr) (println "STDERR: " stderr)))))

  ;; Exécute la commande, puis quand elle est terminé, execute la fonction de callback
  (defn cmd-execution-then [command cb]
    (let [child (cmd-execution command)]
      (.on child "close" cb)))
```

`js/require` est un module node disponible par défaut dans LightTable. Concernant les sorties standard du programme, je log bêtement dans la console. Cela suffit largement pour mon besoin actuel.

Ensuite pour l'utiliser :

```
  ;; Arrête le process xxx puis lance la fonction buildsocle
  (defn killsocle []
    (cmd-execution-then "taskkill /F /IM xxx" buildsocle))
```

Il me reste donc juste à crée mes fonctions une à une pour les chaîner comme il faut. Dernière étape à faire dans le plugin, définir une commande pour exécuter le code :

```
  (cmd/command {:command :user.my-cde
                :desc "User: Rebuild all"
                :exec (fn [] (rebuild-all))})
```

A partir de là je peut exécuter mon code en invoquant la commande `User: Rebuild All`. `:user.my-cde` est l'identifiant technique de la commande, à vous de choisir sa valeur.

Enjoy ! :)

## Phase 4 - Raccourcis clavier

Et pour finir, autant mapper un raccourci clavier pour invoquer la commande plus facilement.

```
  [:app "f6" :user.my-cde]
```

Et hop, un petit F6 et mon éditeur provoque la mise à jour et la reconstruction de mon environnement ! De quoi alimenter ma fainéantise quotidienne :)
