# Logs partout — historique des modifications (Odoo 18)

Chaque modification, sur tous les écrans de gestion, est gardée dans le **fil de discussion (chatter)** de la
fiche, à la manière standard d'Odoo : **ancienne valeur → nouvelle valeur, qui, quand**.

Dossier d'addons contenant deux modules :

| Module | Rôle |
|---|---|
| `logs_partout` | Active le suivi de **tous les champs** sur les écrans de gestion, ajoute un chatter aux écrans qui n'en ont pas, liste globale « qui a changé quoi ». |
| `tracking_manager` | Module OCA (server-tools 18.0, AGPL-3, Akretion) sur lequel il s'appuie : suivi de tous les champs, y compris les lignes (one2many) et many2many. Copié ici tel quel pour n'avoir qu'un dépôt à installer. |

## Installation

```bash
git clone https://github.com/bace203/logs_partout.git /tmp/logs_partout
sudo cp -r /tmp/logs_partout/logs_partout /tmp/logs_partout/tracking_manager /home/Administrateur/addons/
sudo chown -R odoo: /home/Administrateur/addons/logs_partout /home/Administrateur/addons/tracking_manager
sudo systemctl stop odoo
sudo -u odoo odoo -c /etc/odoo/odoo.conf -d <base> -i logs_partout --stop-after-init
sudo systemctl start odoo
```

Dépend de : `mail`, `product`, `stock`, `point_of_sale`, `loyalty`, `account`, `uom` (+ `tracking_manager`).

## Ce qui est suivi dès l'installation

* **Articles** (modèle et variantes — le code-barres d'une variante apparaît aussi sur l'article), catégories
  d'articles, **catégories du point de vente**, listes de prix (**et leurs règles**), attributs, unités de mesure.
* **Contacts / clients**, étiquettes, utilisateurs, sociétés, employés.
* **Stock** : entrepôts, **emplacements**, types d'opération, routes, transferts (et leurs lignes), lots.
* **Point de vente** : points de vente, moyens de paiement.
* **Fidélité** : programmes (**règles et récompenses**), cartes.
* Ventes, achats, factures (et leurs lignes), taxes, journaux, conditions de paiement.
* Modules maison s'ils sont installés : magasins et campagnes Fidélité & CRM, segments, inventaires Smart.

Les champs calculés, en lecture seule ou techniques (date de modification…) ne sont pas suivis.
Les **commandes et sessions du point de vente** ne sont pas suivies par défaut : la clôture d'une session met à
jour toutes ses commandes, cela ferait des milliers de messages. Elles peuvent être activées.

**Écrans sans chatter dans Odoo** : un chatter standard (`mail.thread`) leur est ajouté — emplacements, entrepôts,
types d'opération, routes, catégories PdV, points de vente, moyens de paiement, programmes de fidélité, unités de
mesure, étiquettes, attributs, conditions de paiement. Il est ajouté au formulaire utilisé, même personnalisé.

## Où voir l'historique

* Dans chaque fiche, en bas : le chatter (« Prix de vente 17,35 → 19,90 »).
* **Paramètres › Historique des modifications › Qui a changé quoi** : toutes les modifications, filtrables et
  groupables par personne, écran, champ, jour ; bouton pour ouvrir la fiche.
* **Paramètres › Historique des modifications › Écrans suivis** : activer / arrêter le suivi d'un écran
  (« Suivre tous les champs »), nombre de champs suivis, historique de l'écran. Le détail champ par champ reste
  disponible en mode développeur (Paramètres › Technique › Modèles, bouton « Tracked Fields » de tracking_manager).

## Tests

`odoo-bin -d <db> -i logs_partout --test-tags /logs_partout` : article (tous les champs, code-barres de la
variante), emplacement (chatter ajouté), règle de liste de prix sur la liste de prix, programme de fidélité,
écran de paramétrage, liste globale.
