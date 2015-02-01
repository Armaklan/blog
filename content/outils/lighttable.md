Title: LightTable, le challenger des éditeurs
Date: 2015-02-01 11:00
Tags:  Libre, Traitement De Texte, Programmation, Informatique
Category: Outils

A l'heure où l'on parle énormément de Sublime Text, Atom, et Brackets, j'aimerai vous présenter un de leur challenger : LightTable. Pour tout vous dire, c'est celui que j'utilise au quotidien. Avant de rentrer dans le détail, un petit condensé des plus et moins de ce programme.

<center>![LightTable]({filename}/images/lt.jpg)</center>

# En rapide

## Pourquoi choisir LightTable

- __Opensource__ : Si je n'attachais pas d'importance à l'opensource, je serait probablement encore en train d'utiliser Sublime Text qui me semble rester au-dessus du lot.
- __Keyboard friendly__ : Toutes les commandes de l'éditeur, même la plus insignifiante, peut être lancer au clavier que ce soit à l'aide de raccourcis, ou du panels de commandes. J'ai fuit Brackets à cause de ce point.
- __Personnalisable__ : A l'instar de ses concurrents, on peut configurer tous les petits détails de son éditeur très finement.
- __Stable et rapide__ : Peu de ralentissement, peu de plantage, ce qui n'était pas le cas par exemple avec Atom.
- __Centré sur les sources__ : Tout au plus près du code : la documentation, les erreurs, les résultats...
- __Watch et REPL__ : Pour certains langages il est possible de se connecter un REPL et d'exécuter du code directement depuis son éditeur. Une sorte de mode debug permanent ;)

## Les points moins cool

- __Un eco-système moins riches__ : Au moment où j'écrit ces lignes, j'ai compté environ 120 plugins disponible. On est loin de l'eco-système des autres éditeurs, mais, on trouve tout de même l'essentiel.
- __Clavier internationaux__ : Par défaut, certains mappings ne fonctionnent pas sur clavier français (AZERTY). Je pense nottament au système d'autoclose des `[`,`(` et qu'il a fallut que je configure manuellement (cf Chapitre configuration).
- __ClojureScript et API mal documenté__ : Le système de plugins s'appuie sur ClojureScript. L'API est plutôt mal documenté, il faut donc mettre les mains dans les sources pour comprendre. Autrement dit, aujourd'hui, batir un plugin pour LightTable n'est pas des plus évident.

# Les mains dans le camboui

## Naviguer dans les fichiers

LightTable est installé et lancé, vous êtes dans sa petite interface toute noir. A droite, un editeur avec un message de bienvenu. A gauche, un appel aux allures vides. Et en haut un menu des plus standard que je vous invite à ne pas utiliser ! Que faire ? Selon moi, le premier réflexe à avoir est de lancer le panel de commande avec un petit `Ctrl-Space`, aussi accessible via View > Commands. Ce panel permet de rechercher pamis toutes les commandes de l'éditeurs. En premier lieu vous voudrez probablement ouvrir un fichier ou un dossier. Si vous tapez `folder`, le panel vous proposera en premier résultat : `Workspace : Add folder`.

LightTable est organisé autour de Workspace au sein duquels vous pouvez ouvrir des fichiers et des dossiers. Le panel de gauche (celui actuellement vide) est un navigateur qui montre tout les fichiers disponible au sein du workspace actif. Si vous voulez travailler dans le projet "Hello-World", vous voudrez probablement ouvrir le dossier de source. `Add folder` est là pour cela ! En validant la commande (touche entrée ou click souris), votre système affichera un composant de choix de dossier. Naviguez, choississez et valider, le dossier apparaitra alors dans l'explorateur à gauche de l'éditeur.

Maintenant que le dossier est ouvert, vous pouvez utiliser l'explorateur pour parcourir les dossiers et ouvrir des fichiers. Vous pouvez également ouvrir des dossiers grâce au panel `View > Navigator` ou le raccourci `Ctrl-o`. Ce panel permet de chercher un fichier de l'ouvrir en tapant une partie de son nom. A noter qu'en plus du `Ctrl-o`, vous pouvez ouvrir ce panel via la command `Navigate: open navigate`.

Rajoutons à cela le classique `Ctrl-f`pour rechercher dans le fichier actif, et `Ctrl-Shift-f` pour rechercher dans tous les fichiers du workspace, et vous avez de quoi naviguez confortablement.

## Configurer son editeur

La configuration de l'éditeur passe par deux fichiers :
- User behaviors : qui définit les comportements de l'éditeur et de ses plugins
- User keymap : qui définit les raccourcis claviers

Et pour les ouvrir ? Rien de plus simple, il suffit d'invoquer les commandes `Settings : User behaviors` et `Settings : User keymap`. Par défaut la structure du fichier est déjà posé et vous pouvez y voir un exemple. Pour rajouter un raccourci clavier, la ligne va ressembler à quelques chose de ce genre :

    [:editor "ctrl-n" :editor.sublime.selectNextOccurrence]

Qui se traduit par " dans un editeur, le raccourci `Ctrl-n` permet de déclencher l'action `selectNextOccurence` ". Pour ceux qui se pose la question, il s'agit de la selection multi-curseur. Avec `Ctrl-n`, j'ajoute à la selection la prochaine occurence du mot selectionné.

Pour les français, un petit block que je rajoute toujours pour la fermeture automatique des symboles `[`, `(`, et `{` :

    [:editor ")" (:editor.close-pair ")")]
    [:editor "(" (:editor.open-pair "(")]
    [:editor "ctrl-alt-[" (:editor.close-pair "]")]
    [:editor "ctrl-alt-4" (:editor.open-pair "{")]
    [:editor "ctrl-alt-5" (:editor.open-pair "[")]
    [:editor "ctrl-alt-=" (:editor.close-pair "}")]

Il y a un point que je tient à signaler concernant les fichiers de configuration : l'autocomplétion de LightTable a été vraiment bien travaillé sur ce point ! Ainsi si je tape `[:editor "ctrl-n" ]`, je peut commencer à taper le mot "Next" pour la commande à exécuter. Là, LightTable va me proposer une liste de commande avec le même libellé que dans le panel de commande ! Bref, il est facile de s'y retrouver !

<center>![Configuration et LightTable]({filename}/images/lt-config.jpg)</center>

Coté configuration des comportements, la structure est assez similaire et la complétion tout aussi agréable :

    [:editor :lt.objs.editor/line-numbers]

Ce petit bout de code permet d'afficher les numéro de lignes à gauche de l'éditeur.

## Evaluer du code

Pour certains langages (de base : javascript, python, et cloure), il est possible de connecter son éditeur à un REPL (Read Eval Print loop). Vous pouvez ainsi exécuter des bouts de code depuis votre éditeur et récupérer le résultat.

Pour le javascript par exemple, la procédure la plus simple est la suivante :

- Ouvrir un fichier javascript
- Lancer la commande `Connect: Add Connection` et choisir Browser. Lighttable va ouvrir un onglet navigateur à l'intérieur duquel vous pouvez naviguez normalement.
- Selectionner une ligne de code javascript et lancer la commande `Eval: eval a form in editor`

LightTable exécutera le code dans votre éditeur, et vous renverra le résultat.

<center>![Evaluation in LightTable]({filename}/images/lt-eval.jpg)</center>

# Les extensions cool

La command `Plugins: Show plugin manager` permet d'afficher le gestionnaire de paquet et d'installer facilement les extensions. Voilà les principales extensions que j'utilise :

- __Photons__ : pour ajouter et supprimer facilement mes dossiers de source.
- __lt_snippets__ : Pour sa gestion fine des templates de code
- __JsHint__ : Pour les contrôles de sources Js
- __JsBeautifier__ : Etant donné que c'est moi-même qui est crée ce plugin
- __Markdown__ : Pour la prévisualisation live de mes fichiers markdowns.
- __Paredit__ et __Paredit Plus__ : Pour leurs commandes d'édition de texte avancé
- __Vim__ et __Emacs__ : Pour les fans de ces deux éditeurs qui veulent se sentir comme à la maison ;)

