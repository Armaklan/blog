Title: SRP et Angular
Date: 2023-02-22 09:00
Tags: Angular, SOLID, Architecture
Category: Programmation

Les principes SOLID, introduits par Robert C. Martin, forment 5 principes d'architecture logicielle :

- **S**ingle Responsability Principle
- **O**pen/Close Principle
- **L**iskov Substitution Principle
- **I**nterface Segregation Principle
- **D**ependency Injection Principle

Ils offrent une base solide de réflexion pour obtenir du code maintenable et évolutif. Ces principes sont très intégrés dans le monde du développement back-end, mais je regrette qu'il soit souvent très méconnu ou incompris du côté des développeurs front-end.

Pour apporter ma petite pierre à l'édifice, j'initialise cette série d'articles qui va reprendre les principes un à un, appliqués à du code Angular, l'un de mes domaines d'expertise. Premier principe à l'honneur : le **S**ingle **R**esponsability **P**rinciple (SRP).

Les différents exemples construits pour illustrer cet article ont pour contexte une simple application de gestion de tâches.

## La théorie

Le principe se résume fréquemment par cette phrase : "une classe ne doit avoir qu'une seule et unique raison de changer". Dans son livre, Clean Code, l'auteur va également un peu plus loin en le traduisant avec : "une seule responsabilité, un seul niveau d'abstraction".

Ce principe implique donc :

- Qu'une classe, ou un composant, ne doit avoir qu'un seul et unique rôle dans le système. Gérer à la fois l'affichage et la logique métier au sein d'un seul composant est une violation de ce principe.
- Une classe ne doit pas adresser à la fois des considérations fonctionnelles (le quoi) et des considérations techniques (le comment).

Comment savoir si un composant du système porte plusieurs responsabilités ? Essayez de décrire en français le rôle de votre composant, ce qu'il est amené à réaliser. À chaque fois que, dans ce descriptif, vous êtes amené à utiliser le mot "ET", c'est un indice fort de responsabilités multiples.

## Le SRP à la base du Web

Au cœur du Web, trois technologies cohabitent : HTML, CSS, JS. Les frameworks comme Angular conserve ce découpage qui forme d'ors et déjà 3 responsabilités spécifiques :

- Le HTML a pour rôle de structurer la donnée et les éléments que l'on souhaite afficher.
- Le CSS a pour rôle d'appliquer un style d'affichage aux données et éléments.
- Le JS a pour rôle de rendre la page dynamique en appliquant de la logique.

Même si cette séparation est généralement connue, j'ai pu constater au fil du temps de nombreuses violations, souvent par "facilité". Mais ces violations ont un impact sur le long terme d'une application et peuvent rendre difficile l'évolution de celle-ci.

### Des classes orientés styles

Prenons l'exemple suivant :

```html
<ul class="todos-list">
  <li class="red">
    <input type="checkbox" class="margin-xs" /> Tâche super urgente
  </li>
  <li><input type="checkbox" class="margin-xs" /> Tâche sans urgence</li>
</ul>
```

```cs
.red {
  color: #E53838;
}

.margin-xs {
  margin: 4px;
}
```

Ce code a probablement été construit avec de bonnes intentions : évitez la répétition du code couleur et des informations de marge.

Maintenant, imaginons que demain, on vous demande de passer toutes les tâches urgentes en bleu. Vous serez alors obligé de modifier le fichier css ET le fichier html. Tant que vous n'avez qu'un seul composant, pas de soucis, mais il est fort probable que cette association urgente/couleur se retrouve ailleurs dans l'application : vous allez donc modifier un grand nombre de fichiers.

Le souci est similaire demain pour la marge : si vous voulez passer de 4px à 8px, vous devrez commencer par vérifier que personne n'utilise margin-xs, et le cas échéant, créer une nouvelle classe spécifique à votre cas de figurine.

Quelle est la solution pour associer le respect des responsabilités et le principe de responsabilité ? Pour moi, vous pouvez associer deux outils : un css basé sur des noms métiers ou de la structure, et des variables css.

```html
<ul class="todos-list">
  <li class="urgent"><input type="checkbox" /> Tâche super urgente</li>
  <li><input type="checkbox" /> Tâche sans urgence</li>
</ul>
```

```css
/* Maybe in other file */
root {
  --alert-color: #e53838;
  --margin-xs: 4px;
}

.urgent {
  color: var(--alert-color);
}

ul.todos-list > li {
  margin: var(--margin-xs);
}
```

Ainsi, pour modifier le style de votre todos-list, vous n'avez qu'à modifier les fichiers css en fonction de votre besoin. Vous ne perdez pas en flexibilité et les informations importantes, telles que le code couleur, ne sont pas répétées.

## Le SRP dans les composants Angular

### Presentational-Container pattern

Pour la suite de ma réflexion, je vais me baser sur le template d'un composant angular. Il s'agit de la page principale de mon application de TodoList.

```html
<header>
  <mat-slide-toggle [(ngModel)]="viewDone" data-test-viewDone>
    Voir les tâches terminées
  </mat-slide-toggle>
  <button
    mat-mini-fab
    color="primary"
    aria-label="Ajout d'une todo"
    data-test-add
    (click)="addItem()"
  >
    <mat-icon>add</mat-icon>
  </button>
</header>
<mat-selection-list>
  <mat-list-option
    *ngFor="let todo of todo$ | async; trackBy: trackById"
    [selected]="todo.done"
    (selectedChange)="updateTodo(todo, $event)"
  >
    <div data-test-content>{{ todo?.content }}</div>
    <mat-chip-list>
      <mat-chip color="primary" selected>{{ todo?.category }}</mat-chip>
    </mat-chip-list>
  </mat-list-option>
</mat-selection-list>
```

Le template de ce composant n'est pas d'une grande complexité, et pourtant, il contient bien plusieurs responsabilités : il pose la structure de la page **ET** décrit l'affichage de la liste des tâches **ET** décrit la barre de header.

Première question à se poser : pourquoi le découper s'il est simple de prime abord ? De mon point de vue, la réponse est multiple :  
- Des composants plus petits facilitent leurs réutilisations.  
- Les écrans commencent toujours par une base simple et se complexifient avec le temps.  
- Une part de la complexité est cachée par le fait que l'on zoome sur le template HTML. Sauf que cette complexité va également avoir un impact dans le typescript, mais surtout dans le style SASS.  
- Un meilleur découpage facilitera l'évolution et la correction des éléments du système : on pourra se concentrer sur des unités de code plus réduites.

Si je commence par extraire un composant pour la liste de tâches, j'obtiens :

```html
<header>
  <mat-slide-toggle [(ngModel)]="viewDone" data-test-viewDone>
    Voir les tâches terminées
  </mat-slide-toggle>
  <button
    mat-mini-fab
    color="primary"
    aria-label="Ajout d'une todo"
    data-test-add
    (click)="addItem()"
  >
    <mat-icon>add</mat-icon>
  </button>
</header>
<app-todos-list-items [todos]="todo$" (todoUpdate)="updateTodo($event)">
</app-todos-list-items>
```

J'extrais ensuite la description de la barre de header :

```html
<app-todos-list-header
  (add)="addItem()"
  [(viewDone)]="viewDone"
></app-todos-list-header>
<app-todos-list-items
  [todos]="todo$"
  (todoUpdate)="updateTodo($event)"
></app-todos-list-items>
```

J'en arrive à un template extrêmement simple qui ne s'occupe que d'une seule responsabilité : la structure de la page ! Certains trouveront probablement que mon découpage est un peu extrême, mais on arrive ici sur un pattern que j'affectionne particulièrement : [ContainerComponent vs PresentationComponent](https://indepth.dev/posts/1478/designing-angular-architecture-container-presentation-pattern). Dans ce pattern, on considère deux types de composants :

- Des composants "container" dont le rôle est d’interagir avec le système (service, store, etc...). Ces composants ne doivent pas (ou très peu) s'occuper de mise en forme.  
- Des composants de présentation dont le rôle est au contraire de s'occuper de la mise en forme. Eux fonctionnent uniquement en Input / Output.

Ici, le composant qui reflète ma page est un composant "Container". Il délègue la présentation à ses composants enfants. Ce pattern permet d'obtenir une très bonne testabilité. Les composants de Présentations n'ayant que des inputs/output, il est plus aisé d'obtenir les différents cas grâce aux bons Input. Ils sont également très simples à intégrer dans des outils comme Storybook. De son côté, le composant Container n'ayant qu'un template très réduit, je peux me consacrer sur la classe TS au moment du ts.

### Un seul niveau d'abstraction

Regardons le composant que l'on a extrait. Cette fois-ci, je vais m'intéresser au HTML et au CSS.

```html
<header>
  <mat-slide-toggle [(ngModel)]="viewDone" data-test-viewDone>
    Voir les tâches terminées
  </mat-slide-toggle>
  <button
    mat-mini-fab
    color="primary"
    aria-label="Ajout d'une todo"
    data-test-add
    (click)="addItem()"
  >
    <mat-icon>add</mat-icon>
  </button>
</header>
```

```css
:host {
  display: block;
}

header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 16px;
  margin: 16px;
}
```

Même ici, mon composant conserve deux responsabilités : il décrit le contenu de la barre d'action **ET** décrit l'affichage d'une barre d'action au sein de mon application. Le composant reste très simple, et l'on pourrait probablement s'arrêter ici, mais ce serait gâcher l'opportunité de réutiliser le code : toutes mes barres d'actions vont probablement être similaires au sein de mon application.

Même si cela ne simplifie pas réellement mon composant, j'opterai donc pour cette solution :

```html
<app-action-bar>
  <mat-slide-toggle [(ngModel)]="viewDone" data-test-viewDone>
    Voir les tâches terminées
  </mat-slide-toggle>
  <button
    mat-mini-fab
    color="primary"
    aria-label="Ajout d'une todo"
    data-test-add
    (click)="addItem()"
  >
    <mat-icon>add</mat-icon>
  </button>
</app-action-bar>
```

De primes abords, le html ne rencontre qu'une modification : l'utilisation d'un app-action-bar à la place d'un header. La principale différence se trouve au niveau du css : le style sera rattaché à `ActionBarComponent`. Il sera donc facilement trouvable et réutilisable : on se place dans une situation propice à éviter de futures duplications.

### Et le typescript ?

La logique du SRP est la même dans le code typescript :

- Le typescript d'un composant doit s'occuper de l'orchestration (le Quoi), mais pas de l'implémentation des règles métiers (le Comment).
- Le métier doit être réparti entre :
  - Les modèles qui représentent une donnée métier, règle de gestion compris.
  - Des services spécialisés, chaque service ayant une responsabilité propre.

Prenons un exemple concret de composant :

```ts
export class TodosListItemComponent {
  @Input() todo: Todo | null = null;

  get priorityIcon(): string {
    switch (this.todo?.priority) {
      case 1:
        return "i-greatest";
      case 2:
        return "i-great";
      case 3:
        return "i-normal";
      case 4:
        return "i-low";
      default:
        return "i-lowest";
    }
  }

  get authorDesignation() {
    const author = this.todo?.author;
    if (!author) {
      return undefined;
    }
    return `${author.civility} ${author.firstname} ${author.lastname}`;
  }
}
```

Si je prends la responsabilité du composant dans son ensemble, j'obtiens : "Gérer l'affichage d'une tâche unitaire dans la liste des tâches". De primes abords, une seule responsabilité. Toutefois, les deux fonctions données en exemple n'appartiennent pas réellement à cette responsabilité. `priorityIcon` définit la règle d'affichage d'une priorité. `authorDesignation` définit la règle d'affichage du nom de l'auteur d'une tâche. La présence de cette fonction dans cette classe rend ses deux règles difficilement réutilisables (ce qui risque d’entraîner une répétition).

Où faudrait-il les mettre ?

Pour ma part, même si les deux méthodes ont des similitudes, j'appliquerai une stratégie différente :  
- `authorDesignation` est une règle métier lié à une personne : il s'agit du standard permettant de la nommer. Pour moi, cette règle doit aller dans la classe de l’élément utilisé, soit, ici, `Author`.  
- `priorityIcon` à une particularité : elle contient des éléments purement graphiques (un nom d'icône) qui ne rentre pas dans la responsabilité d'une `Tache`. En Angular, un des éléments fournis par le framework est le pipe.

La classe Author ressemblerait donc à ceci :

```ts
export class Author {
  constructor(
    public civility?: string,
    public firstname?: string,
    public lastname?: string
  ) {}

  get designation() {
    return `${this.civility} + ${this.firstname} + ${this.lastname}`;
  }
}
```

Et le pipe `designation` :

```ts
export class PriorityIconPipe implements PipeTransform {
  transform(priority: number): string {
    switch (priority) {
      case 1:
        return "i-greatest";
      case 2:
        return "i-great";
      case 3:
        return "i-normal";
      case 4:
        return "i-low";
      default:
        return "i-lowest";
    }
  }
}
```

## En conclusion

L'application du SRP dans une application Angular demande un peu de réflexion, mais le framework fourni tous les éléments pour l'appliquer facilement. Même si, de prime abord, le découpage obtenu peut paraître très extrême, il offre une structure de base permettant de faire évoluer aisément l'application au fil du temps.

_Relecture : Gregory BACH, merci à lui._
