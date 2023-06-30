Title: Liskov et DI chez Angular
Date: 2023-06-29 21:00
Tags: Angular, SOLID, Architecture
Category: Programmation

Il m'a fallu du temps pour rédiger la suite de mes articles au sujet de SOLID, en partie par manque de temps, en partie par difficulté à trouver leurs applications avec Angular. J'ai finalement décidé de faire un article double parlant du principe de Liskov et de l'Inversion de dépendance.

N'hésitez pas à me faire un retour et à me proposer des améliorations !

## Le principe de substitution de Liskov

Le principe de substitution de Liskov est un principe objet qui s'applique à l'héritage : quand une méthode ou une classe dépend d'une classe parente, elle doit pouvoir utiliser les différents enfants indistinctement.

Prenons un exemple pour comprendre cette règle.

Imaginons que nous ayons les classes suivantes :

```ts
abstract class Animal() {
    voler();
}

class Pelican() {
    voler() {
        // implementation
    }
}

class Cygne() {
    voler() {
        // implementation
    }
}
```

Jusque là, le principe de Liskov semble respecter. Si nous possédons un tableau d'animaux, nous pouvons faire voler indistinctement des Pélicans et des Cygnes.

```ts
const animaux = [new Pelican(), new Cygne()];
// this code works
animaux.forEach((animal) => animal.voler());
```

Maintenant rajoutons la classe enfant suivante :

```ts
class Souris() {
    voler() {
        throw new Error("Les souris ne volent pas !")
    }
}
```

Le code suivant :

```ts
const animaux = [new Pelican(), new Cygne(), new Souris()];
// this code throw an error
animaux.forEach((animal) => animal.voler());
```

L'introduction de la classe Souris viole le principe de Liskov : notre code, jusqu'alors fonctionnel, va lever une erreur. Ici, nous sommes face à une mauvaise abstraction : la classe "Animal" ne devrait pas définir la méthode voler.

La levée d'erreur n'est pas le seul cas qui peut poser problème : dans les enfants, les méthodes ne doivent pas avoir d'effets de bord imprévu. Le comportement des enfants doit donc rester "prévisible".

Pour ma part, je n'ai pas trouvé d'application "spécifique" à Angular concernant ce principe. Il s'applique aux objets angular comme il s'appliquerait aux objets standards. Mais si vous avez des idées ou cas d'application, je suis preneur !

## Dependency Inversion Principle

Si je cite wikipedia :

> Les deux assertions de ce principe sont :
>
> 1. Les modules de haut niveau ne doivent pas dépendre des modules de bas niveau. Les deux doivent dépendre d'abstractions.
> 2. Les abstractions ne doivent pas dépendre des détails. Les détails doivent dépendre des abstractions.

Si je reformule ce principe : une classe ne doit pas dépendre de l'implémentation, mais uniquement du contrat d'interface, de ses dépendances.

C'est un principe que l'on respecte assez facilement pour une simple et bonne raison : l'injection de dépendance. Ce mécanisme, fourni dans le framework Angular, répond directement à ce besoin. Grâce à l'injection, je peux modifier une implémentation, modifier ses propres dépendances, voir la remplacer totalement, sans pour autant modifier le code utilisant ma classe modifiée.

Je profite tout de même de parler de l'injection de dépendant pour rappeler une fonctionnalité avancée de l'injecteur angular : l'injection par token. Cette fonctionnalité vous permet de fournir un service non par sa classe, mais par un "nom".

Imaginons le cas de figure suivant : une application prévue pour fonctionner soit "in memory", soit avec une base de donnée Firestore. Pour ma couche d'accès aux données, je définis l'interface suivante :

```ts
export interface TodoRepository {
  save(todo: Todo): Promise<void>;
  find(filter: { tag?: string }): Promise<Todo[]>;
}
```

Au sein de mon application, je crée 2 implémentations différentes, correspondant à mes deux cas de figure :

```ts
export class InMemoryTodoRepository implements TodoRepository {
  private todos: Todo[] = [];

  get(): Promise<Todo | undefined> {
    return Promise.resolve(this.todos[this.todos.length - 1]);
  }

  save(todo: Todo): Promise<void> {
    this.todos.push(todo);
    return Promise.resolve();
  }

  find(filter: { tag?: string | undefined }): Promise<Todo[]> {
    return Promise.resolve(
      this.todos.filter((t) =>
        filter && filter.tag ? t.tags?.includes(filter.tag) : true
      )
    );
  }

  clear() {
    this.todos = [];
  }
}
```

```ts
export class FirestoreTodoRepository implements TodoRepository {
  constructor(private firestore: Firestore) {}

  private readonly todosCollections = collection(this.firestore, "todos");

  async save(todo: Todo): Promise<void> {
    await addDoc(this.todosCollections, {
      description: todo.description,
      done: todo.done || false,
      tags: todo.tags || [],
    });
  }

  async find(filter: { tag?: string | undefined }): Promise<Todo[]> {
    const data: DocumentData[] = await firstValueFrom(
      collectionData(this.todosCollections)
    );
    return data
      .filter((d) => !filter?.tag || d["tags"].include(filter.tag))
      .map(
        (d) =>
          ({
            description: d["description"],
            done: d["done"] || false,
            tags: d["tags"] || [],
          } as Todo)
      );
  }
}
```

Comment permettre à l'application de passer facilement d'une implémentation à l'autre ? La réponse est justement l'injection par token :

```ts
export class CreateTodoUseCase {
  constructor(
    @Inject("TODO_REPOSITORY") private todoRepository: TodoRepository
  ) {}
}
```

`CreateTodoUseCase` déclare ici injecter le todoRepository qui sera défini par le token "TODO_REPOSITORY". Au niveau de mes modules, il ne me restera qu'à fournir le bon service :

```ts
{ provide: 'TODO_REPOSITORY', useClass: environnement.inMemory ? InMemoryTodoRepository : FirestoreTodoRepository },
```

Le simple changement de configuration me permettra d'avoir l'une ou l'autre de mes implémentations. C'est une fonctionnalité méconnue, mais qui peut rendre de grands services.

Il ne me reste plus qu'à parler du "I" de SOLID, l'interface segregation. Suite dans le prochain épisode !

_Relecture : encore Gregory BACH. Toujours un grand merci à lui._
