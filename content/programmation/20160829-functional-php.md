Title: Code fonctionnel en PHP
Date: 2016-08-29 13:38
Tags: Informatique, Php, Functionnel
Category: Programmation

Ah le php... Une technologie que je n'apprécie guère pour des tas de bonnes et mauvaises raisons. Mais il faut bien lui reconnaître une qualité : il est très facile de lui trouver un hébergement.

Mais là n'est pas le sujet du jour ! Un nouveau projet s'ouvre à moi et, bien qu'il soit en php, je n'ai pas envie de mettre de coté mon centre d'interêt du moment : la programmation fonctionnelle. Me voilà donc à chercher comment la mettre en oeuvre en php.

# PHP et Closure.

La base de la programmation fonctionnelle, c'est de manipuler des fonctions. Et l'un des outils très utile autour des fonctions, ce sont les Closures : des fonctions qui "embarque" avec elle des variables en plus de leur paramètre entrant.

En php, la closure est un peu particulière car il faut expliciter les variables qui sont utilisable à l'intérieur de la fonction. Elle se déclare ainsi :

```
function ($param) use ($varEmbarque1, $varEmbarque2) {
    // Mon corps de méthode
    // $varEmbarque1 et $varEmbarque2 sont accessible
}
```

Un exemple d'utilisation ?

```
public function raise($event) {
    Arrays::each($this->listeners, function($fn) use($event) {
        call_user_func($fn, $event);
    });
}
```

Je reviendrai plutard sur le `Arrays::each`. Ce qui est important ici c'est que each appelle la méthode pour chaque élement du table. La valeur de l'élement est alors donné en paramètre. Ici ma fonction a besoin de deux élements pour fonctionner : une callback contenue dans le tableau, et un évènement à transmettre. L'un est passé en paramètre, l'autre est passé via la closure.

Et si comme moi vous n'aimez pas spécialement les fonctions anonymes (question de lisibilité), vous pouvez appliquer le pattern builder :

```
public function raise($event) {
    Arrays:each($this->listeners, $this->emit(event));
}

// (DomainEvent) -> (Fn) -> ()
private function emit($event) {
    return function($fn) use($event) {
        call_user_func($fn, $event);
    };
}
```

# Manipulations de collections et plus si affinité.

`map`, `filter`, ... Ces petites fonctions de manipulations de collections sont le premier outil issue du fonctionnel que j'ai utilisé. Je les trouve tellement confortable que je n'ai pas envie de m'en passer.

Malheureusement les fonctions fournies par php sont limitées (map, filter et reduce uniquement). En fouillant un peu sur internet, je suis tombé sur [underscore.php](http://brianhaveri.github.io/Underscore.php), une librairie très sympathique qui fournit le panel complet des fonctions de ce genre (`all`, `any`, `find`, ...).

Petit bonus, elle nous offre aussi des fonctions de manipulations de fonctions tels que `compose`, `memoize`, `once` et `throttle` qui peuvent s'avérer très pratique.

# Et enfin, les monades

Dernier outils du fonctionnel : les monades. Je ne les utilise pas encore tout à fait naturellement mais je reconnaîs ce qu'elles peuvent apporter. Cette fois-ci j'ai envie de les utiliser davantage et pour cela, j'ai trouvé la librairie [php-functional](http://widmogrod.github.io/php-functional).

Les monades, ce sont des outils très utiles tels que `Either` qui présente deux "chemins" (réussite ou échec), avec deux types de retours différents, ou `Maybe` qui est une autre façon de gérer l'abscence de valeur.

Un exemple d'utilisation :

```
// (String, String) -> Either[FunctionalError, User]
protected function checkAuthentification($login, $password) {
    return $this->userRepository
        ->findByLogin($login)
        ->bind($this->checkPassword(Password::fromValue($password)));
}
```

`$this->userRepository->findByLogin()` est une fonction qui renvoi un `Either`. `Bind` permet d'appliquer à la valeur retourné une autre fonction qui renverra elle aussi un `Either` uniquement dans le cas `Right` (chemin de succès). La fonction donné à bind sera appellé avec la valeur en paramètre.

A l'intérieur de findByLogin, on va retrouvé deux retour possible :

```
\Monad\Either\Right::of($user);
```

ou 

```
\Monad\Either\Left::of(new FunctionalError("Utilisateur inconnu"));
```
Dans un code classique, j'aurai utilisé un mécanisme d'exception qui aurait pas forcément été aussi lisible.

En sortie de checkAuthentification j'ai toujours une Either. L'appellant pourra donc faire quelque chose comme cela : 

```

// (String, String) -> Either[FunctionalError, User]
public function exec($login, $password) {
    $user = $this->checkAuthentification($login, $password);
    $user->map($this->storeInSession())
         ->map($this->raiseUserConnected());
    return $user;
}
```
En cas de succès de l'authentification, j'effectue deux fonctions :

- Stockage en session
- Lever d'un évènement

Quand je veut extraire définitivement la valeur de la monade, je peut faire ceci :

`$myEither->extract()` 

Je m'arrêterais ici dans l'explication sur les monades : ils faudraient un article entier (voir plus) pour vraiment démontrer leurs valeurs.

# Des commentaires étranges ?

Vous avez pu apercevoir au-dessus de mes fonctions des commentaires ayant cette forme : 

```
// (String, String) -> Either[FunctionalError, User]
```

Ces commentaires sont uniquement présent à des fins de documentations. C'est une manière de donner des indications sur les types utilisés sans passé par une phpDoc bien plus verbeuse : je trouve toujours les javadocs / phpdocs aussi useless... 

Ces quelques indications me sont bien plus précieuses et sont suffisament légère pour que je garde la discipline de les rajouter à chaque fois.
