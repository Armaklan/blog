Title: Open/Close et Angular
Date: 2023-02-22 09:00
Tags: Angular, SOLID, Architecture
Category: Programmation

Second article de la série sur les principes SOLID, il s'agit aujourd'hui de parler du Open/Close Principle. Je dois bien avouer que dans les différents principes introduits par Robert C. Martin, il s'agit de celui dont l'explication me vient le moins naturellement... Cet article est donc également, pour moi, une manière de prendre le temps d'y réfléchir plus en détail.

## La théorie

Le principe est énoncé de la manière suivante : un élément logiciel doit être à la fois ouvert (à l'extension) et fermé (à la modification). En d'autres mots : de nouvelles fonctionnalités doivent pouvoir être rajoutées en créant du nouveau code, et non en modifiant le code existant.

Pourquoi appliquer cette règle ?
Les éléments de code déjà existants sont utilisés au sein de notre application. Les modifier présente ainsi un risque : créer des régressions applicatives. En étendant les éléments sans les modifier, on crée de nouveaux comportements disponibles pour nos besoins, sans entraîner de modification des comportements existants.

## Open/Close sur les classes Typescript

Le premier endroit où l'on peut facilement appliquer ce principe, ce sont dans les classes Typescript, notamment les modèles. Dans le code suivant, nous avons une classe `Invoice` qui, en plus des données courantes de la facture, définit quels sont les champs éditables ou non de celle-ci (en fonction de leurs sources).

Pour l'instant, nous avons :

- des factures "importées", pour lesquels seul le libellé est éditable.
- des factures manuelles qui sont entièrement éditables

```ts
export type SourceInvoice = "import" | "manual";
export class Invoice {
  constructor(
    public source: SourceInvoice,
    public labek: string,
    public amount: number,
    public tva: number,
    public currency: Currency
  ) {}

  public get labelEditable(): boolean {
    return true;
  }

  public get tvaEditable(): boolean {
    return this.source === "manual";
  }

  public get amountEditable(): boolean {
    return this.source === "manual";
  }

  public get currencyEditable(): boolean {
    return this.source === "manual";
  }
}
```

Comme les choses ne sont jamais figées dans un programme informatique, notre client rajoute une nouvelle source que l'on appelle "tiers". Cette source vient de facture créée par un programme tiers. Dans ces factures, on souhaite que :

- le libellé soit éditable
- le taux de tva soit éditable
- les autres éléments de la facture soit en lecture seule.

Pour répondre à ce besoin, je vais devoir éditer l'accesseur `tvaEditable` au risque de casser le comportement pour les sources actuelles. À chaque fois que je rajoute une nouvelle source, je vais devoir revenir sur le code existant. Pour résoudre à ce problème, il faut faire appel à deux notions : héritage et polymorphisme.

Nous allons conserver une classe `Invoice`, qui sera abstraite, ainsi qu'une implémentation par source de facture.

```ts
export abstract class Invoice {
  constructor(
    public label: string,
    public amount: number,
    public tva: number,
    public currency: Currency
  ) {}

  public get labelEditable(): boolean {
    return true;
  }

  public get tvaEditable(): boolean {
    return false;
  }

  public get amountEditable(): boolean {
    return false;
  }

  public get currencyEditable(): boolean {
    return false;
  }
}

export class ImportInvoice extends Invoice {
  // Nothing to add (default behaviours)
}

export class ManualInvoice extends Invoice {
  override get tvaEditable(): boolean {
    return true;
  }

  override get amountEditable(): boolean {
    return true;
  }

  override get currencyEditable(): boolean {
    return true;
  }
}

export class TiersInvoice extends Invoice {
  override get tvaEditable(): boolean {
    return true;
  }
}
```

Au sein d'une application front, il y a de fortes chances que ces différents modèles soient instanciés par une API Back-End. L'utilisation du pattern Factory permet d'instancier la bonne classe en fonction de l'instance.

```ts
/**
 * Interface to represent invoice in backend model.
 */
export interface InvoiceDTO {
  label: string;
  amount: number;
  tva: number;
  currency: Currency;
  type: SourceInvoice;
}

export class InvoiceFactory {
  public create(invoice: InvoiceDTO): Invoice {
    switch (invoice.type) {
      case "import":
        return new ImportInvoice(
          invoice.label,
          invoice.amount,
          invoice.tva,
          invoice.currency
        );
      case "manual":
        return new ManualInvoice(
          invoice.label,
          invoice.amount,
          invoice.tva,
          invoice.currency
        );
      case "tiers":
        return new TiersInvoice(
          invoice.label,
          invoice.amount,
          invoice.tva,
          invoice.currency
        );
      default:
        throw new Error(`Unknown invoice type: ${invoice.type}`);
    }
  }
}
```

Cette factory ne semble pas respecter le principe Open/Close, mais elle est malheureusement incontournable. Toutefois, nous avons isolé la violation sur du code "simple", avec une responsabilité réduite. La modification de ce code n'est pas réellement un élément risqué. Il est à noter que certaines librairies de mapping, comme `class-transformer`, savent s'occuper de la transformation de Json vers des classes typées, y compris dans ce schéma d'héritage.

Vous remarquerez que dans cette factory, le type de retour est `Invoice`. Les classes utilisant ce code n'auront donc pas conscience d'avoir une `ImportInvoice`, une `ManualInvoice`, ou une `TiersInvoice`. Il s'agit du polymorphisme : une classe peut être remplacée de manière transparente par ses enfants.

## Open/Close sur les composants

Le principe s'applique au code TypeScript, mais il peut également s'appliquer aux composants en eux-mêmes avec la même logique : permettre à un composant d'être étendu pour répondre aux différents besoins que l'on pourra avoir avec le temps. En dehors de l'héritage, Angular fournit deux outils : ngContent et ngTemplate.

### Utiliser ngContent

Pour démontrer ses deux outils, prenons l'exemple suivant :

```html
<article class="card">
  <header>
    <h2>{{ invoice.title }}</h2>
  </header>

  <body>
    {{ invoice.description }}

    <b class="total">{{ invoice.amount }} {{ invoice.currency }}</b>
  </body>

  <footer>Crée le {{ invoice.createDate }}</footer>
</article>
```

Bien entendu, ce composant a aussi son lot de css pour donner le bon style à la carte. En l'état, ce composant est tout sauf flexible :

- Pour créer une nouvelle carte dans l'application, il me faudra soit modifier le code de ce composant, soit dupliquer pas mal de code.
- Même pour créer une variation de cette carte, il me faudra faire de même.

Commençons par créer un composant générique de carte, `app-carte` à l'aide de ngContent.

```html
<article>
  <header>
    <h2>{{ title }}</h2>
  </header>

  <body>
    <ng-content select="body"></ng-content>
  </body>

  <footer>
    <ng-content select="footer"></ng-content>
  </footer>
</article>
```

La carte représentant les factures sera réduite au html suivant :

```html
<app-card [title]="invoice.title">
  <body>
    {{ invoice.description }}

    <b class="total">{{ invoice.amount }} {{ invoice.currency }}</b>
  </body>

  <footer>Crée le {{ invoice.createDate }}</footer>
</app-card>
```

Dans ce même composant, je pourrais aussi ajouter différents ngContent pour prévoir des "points d'extensions" permettant de rajouter du comportement.

### Utiliser ngTemplate

ngContent permet d'ajouter du comportement, mais il ne permet pas de modifier le comportement déjà implémenté. C'est là que ngTemplate intervient. L'utilisation du composant précédent ressemblerait à ceci :

```html
<app-invoice-card [invoice]="invoice"></app-invoice-card>
```

Imaginons que dans ce composant, nous voulions rendre le footer modifiable. Nous pourrions modifier le composant ainsi :

```html
<ng-template #defaultTemplate let-invoice
  >Crée le {{ invoice.createDate }}</ng-template
>

<ng-container
  [ngTemplateOutlet]="footerTemplate || defaultTemplate"
  [ngTemplateOutletContext]="{ $implicit: invoice }"
>
</ng-container>
```

```ts
@ContentChild('footer') footerTemplate: TemplateRef<any>;
```

Et voilà, notre footer contient notre comportement par défaut, mais peut être surchargé à l'utilisation.

```html
<app-invoice-card [invoice]="invoice">
  <ng-template #footerTemplate let-invoice
    ><b>TVA : </b>{{ invoice.tva }}</ng-template
  >
</app-invoice-card>
```

La question de savoir quand privilégier ngTemplate sur ngContent est assez délicate. Pour ma part, ngTemplate doit être utilisé quand la surcharge est optionnelle, voir rare. Son utilisation est également incontournable quand on veut surcharger un élément qui va être répéter (comme les éléments d'une liste).

## Conclusion

Encore une fois, Angular fournit tous les outils nécessaires. Savoir quand mettre en œuvre ces outils est, par contre, un peu plus compliqué. A mon sens, il y a deux moments où il faut réfléchir :

- Quand on crée un composant d'UI "générique", par exemple ceux d'une librairie graphique. Il s'agit typiquement du genre de composant que l'on veut flexible.
- Au moment où l'on crée une variation dans un composant existant : gérer les variations à l'aide de ngIf est rarement une bonne idée. Complexité qui augmente avec le temps, risque de régression, etc.

_Relecture : Gregory BACH, merci à lui._
