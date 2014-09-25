Title: Aggrandissez votre VM
Date: 2014-09-26 02:00
Tags: Linux, Cli, Tips
Category: Linux

Il est presque midi. Depuis votre arrivé au boulot ce matin, vous avez préparez soigneusement une machine virtuelle. Tout y est : votre IDE, le serveur apache, le navigateur, les librairies... Tout est enfin prêt, il ne vous reste plus qu'une étape : montez votre dump de base de données ! Et là... C'est le drame ! Burnout comme dirait certain, votre disque est plein. C'est un échec. Votre VM est inutilisable.

Vous avez déjà vécu cette situation ? Moi oui ! Et il m'a fallu un peu de temps pour trouver comment aggrandir ce ***** de disque ! Du coup, histoire de pas rechercher la prochaine fois, je me suis dit qu'un petit blog ne fera pas de mal !

Le Contexte
-----------

L'enchaînement de commande dont je parle ici ne convient probablement pas à toutes les situations. Voilà le cas dans lequel je me trouve et où les commandes fonctionnent nickel !

- Machine virtuelle Virtual Box (important pour la première étape).
- Système invité Linux.
- Partitions sous LVM.
- Deux disques VDI :
-- Le premier contient le swap et la racine (/dev/sda)
-- Le second contient le home (/dev/sdb)

Dans l'histoire des deux disques, le point important, c'est que je cherche à étendre ma racine. Du coup, la partition se trouve à la "fin" du disque virtuel de ma VM. Là, ça aurait marché aussi pour étendre home, mais pas pour étendre la swap.

Etendre le disque VDI
---------------------

VirtualBox fourni un petit outil permettant d'étendre le disque VDI, c'est-à-dire le fichier correspondant au disque, assez simplement.

```SH
VBoxManage.exe modifyhd mydisk.vdi --resize 10000;
```

Je traduit : hey Virtual Box, modifie la taille de mon disque mydisk.vdi jusqu'à 10 Go.

Une fois la commande exécuté, on a un disque qui fait virtuellement 10 Go. Bon tant que Linux ne l'utilise pas, ça ne sert à rien... Mais virtuellement, l'espace disque existe ! ;)

Aggrandir la partition Linux
----------------------------

Une fois le disque étendu, on démarre la VM et on va essayé de faire comprendre au système qu'il peut s'étaler un peu plus. S'en suit une série de commande barbare pour :

- Etendre la partition primaire qui héberge le LVM
- Etendre le `physical volume`
- Etendre le `logical volume`
- Etendre le filesystem

Bon concrètement si quelqu'un est capable de m'expliquer les rôles du `Volume Group`, `Physical Volume`, et `Logical Volume`, je prend ! En gros, j'ai comprit qu'ils étaient emboité comme des poupées russes et qu'il fallait évité d'étendre le volume logique sans avoir aggrandit le volume physique ;)

Bon, commençons les commandes barbares avec fdisk. Le procédé est simple : je détruit ma partition, et je la recrée en plus grand ! Quoi, vous hésitez ? Mais non, vous n'allez rien perde ! Normalement...

```SH
fdisk /dev/sda
d
2
```

Je lançe l'outil fdisk sur sda, je supprime (delete) la partition numéro 2, soit `/dev/sda2` qui correspond à mon root.

```SH
n
p
2
(enter)
(enter)
w
```

Je continue l'outil disk. Je crée (new) une partition primaire (p), qui occupera le numéro 2 (sda2). Là je valide le début et la fin proposé par l'outil qui est suffisament intelligent pour vouloir occuper tout l'espace restant. Pour j'enregistre (write).

Et hop, Linux râle en disant que je vient de tout casser à chaud ! Ok, pas de soucis, je redémarre la bête et me lance enfin dans les commandes restants.

```SH
pvresize /dev/sda2
lvextend /dev/vg_devdomain/lv_root
resize2fs /dev/vg_devdomain/lv_root
```

Dans les commandes ci-dessous, vous devez demandez à quoi correspond `vg_devdomain/lv_root`. Là, nous somme dans les particularité du LVM avec un groupe et un volume. Un simple `df -h` vous affichera cette information à coté de votre partition root.

Une fois ces étapes terminés, tout est terminé ! Un petit redémarrage pour la forme, mais votre espace est disponible.
