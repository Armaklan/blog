Title: Partagez des fonctionnalités grâce aux slots en VueJS
Date: 2019-01-25 8:00
Tags: Javascript, FrontEnd, VueJs
Category: Programmation

Slot est une "api de diffusion de contenu". Plus couramment, il s'agit de la possibilité pour un composant, de laisser une partie de son contenu être défini par le composant appelant (en général par l'intermédiaire du contenu de la balise). Ce mécanisme assez classique est aussi appelé transclude dans d'autre framework.

Ce qui est assez peu connu toutefois, c'est que les slots Vue offre la possibilité de "transmettre" des données, méthodes, etc, depuis le composant définissant le slot, vers le composant utilisant celui-ci. Cette fonctionnalité très pratique permet de faire aisément des "renderless composants" (composants sans rendu) portant des fonctionnalités, qui seront utilisé par des composants réels. C'est l'une des implémentations qui permet de satisfaire le besoin de "High Order Composant". 

Détaillons un peu l'implémentation.

Du coté du renderless composant
-------------------------------------

Le renderless composant est donc un composant qui n'a pas de template et retourne uniquement un slot exploitable. Pour cela, nous utiliserons ainsi la fonction "render" permettant de définir programmatiquement le rendu d'un composant :

```js
  render() {
    return this.$scopedSlots.default({
      items: this.items,
      selectItem: this.selectItem
    });
  }
```

Dans cet exemple, items et addItem sont des éléments que je mets à disposition à l'intérieur du scoped. Dans mon cas, items est un tableau d’élément, et addItem une fonction. 

Du côté de l'utilisateur
-------------------------

Nous avons un composant 'MyRenderComponent' qui veut utiliser mon renderless component. Dans le template de MyRenderComponent, je vais donc déclarer ceci : 

```html
<MyRenderlessComponent>
  <div slot-scope="{ items, addItem }">
    <div
      v-for="item in items"
      :key="item.id"
      @click="selectItem($event)">
	{{ item.nom }}
    </div>
  </div>
</MyRenderlessComponent>
```

J'ajoute donc dans mon template le renderless component. Je définit ensuite comme contenu un slot scopé, et je récupère les éléments transmis par le slot via la décomposition. Ensuite, je peux les utiliser comme toute variable ou méthode de mon application.

Quel objectif ?
----------------

Comme vous avez pu le constater, l'opération n'est pas compliqué, mais a quoi sert-elle concrètement ? Pour ma part, je vois deux cas d'utilisation :

- Découpler la logique d'affichage, et la logique métier en deux composants. Le renderless component jouant un peu le rôle des "services" d'angular.
- Capitaliser les comportements communs s'appliquant sur des types de données variées. 

J'ai tiré les exemples de cet article (en simplifiant beaucoup) d'un renderless component destinée à gérer les interactions standard sur les listes d'objets, où en général, je veux toujours : 

- Récupérer le listing au chargement de la page
- Permettre la suppression, la mise à jour, et l'ajout d'un élément