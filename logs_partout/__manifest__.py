# -*- coding: utf-8 -*-
{
    'name': 'Logs partout – historique des modifications',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Chaque modification (ancienne → nouvelle valeur, qui, quand) dans le fil de discussion de tous les '
               'écrans de gestion : articles, clients, stock, point de vente, fidélité, ventes, achats…',
    'description': """
Historique des modifications, à la manière standard d'Odoo (suivi dans le chatter) :
* tous les champs des écrans de gestion sont suivis (module OCA tracking_manager), lignes comprises
  (règles de liste de prix, fournisseurs d'un article, règles et récompenses d'un programme de fidélité) ;
* un chatter est ajouté aux écrans qui n'en ont pas (emplacements, entrepôts, catégories PdV, points de vente,
  moyens de paiement, programmes de fidélité, unités de mesure, étiquettes, attributs, conditions de paiement) ;
* activé à l'installation ; Paramètres › Technique › Historique des modifications pour choisir les écrans ;
* liste globale « qui a changé quoi, quand ».
""",
    'author': 'SRA',
    'license': 'AGPL-3',
    'depends': ['tracking_manager', 'mail', 'product', 'stock', 'point_of_sale', 'loyalty', 'account', 'uom'],
    'data': [
        'security/ir.model.access.csv',
        'views/logs_partout_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
}
