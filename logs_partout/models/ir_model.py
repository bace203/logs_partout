# -*- coding: utf-8 -*-
"""Which screens keep the history of their changes (tracking_manager: all fields tracked in the chatter)."""
from odoo import _, api, fields, models
from odoo.osv import expression

# business screens tracked by default (only those installed are used)
DEFAULT_MODELS = [
    'product.template', 'product.product', 'product.category', 'pos.category', 'product.pricelist',
    'product.attribute', 'uom.uom',
    'res.partner', 'res.partner.category', 'res.users', 'res.company', 'hr.employee',
    'stock.warehouse', 'stock.location', 'stock.picking.type', 'stock.route', 'stock.picking', 'stock.lot',
    'pos.config', 'pos.payment.method',
    'loyalty.program', 'loyalty.card',
    'sale.order', 'purchase.order', 'account.move', 'account.tax', 'account.journal', 'account.payment.term',
    # own modules, when installed
    'loyalty.store', 'loyalty.tier.campaign', 'loyalty.segment', 'stock.smart.inventory',
]
# lines tracked on their parent (e.g. a rule of a pricelist is logged on the pricelist)
LINES = {
    'product.pricelist': ['item_ids'],
    # variant fields (barcode, reference…) are logged on the product the user looks at
    'product.template': ['seller_ids', 'attribute_line_ids', 'product_variant_ids'],
    'loyalty.program': ['rule_ids', 'reward_ids'],
    'sale.order': ['order_line'],
    'purchase.order': ['order_line'],
    'account.move': ['invoice_line_ids'],
    'stock.picking': ['move_ids_without_package'],
}
# written by Odoo itself all the time: tracking them would only add noise
NOISY_FIELDS = {'write_date', 'write_uid', '__last_update', 'message_main_attachment_id', 'activity_ids',
                'message_ids', 'message_follower_ids', 'website_message_ids', 'rating_ids'}


class IrModel(models.Model):
    _inherit = 'ir.model'

    is_logs_partout_default = fields.Boolean('Suivi par défaut', compute='_compute_is_logs_partout_default')

    def _compute_is_logs_partout_default(self):
        for model in self:
            model.is_logs_partout_default = model.model in DEFAULT_MODELS

    def _default_automatic_custom_tracking_domain_rules(self):
        rules = super()._default_automatic_custom_tracking_domain_rules()
        base = [('readonly', '=', False), ('name', 'not in', sorted(NOISY_FIELDS))]
        for model, lines in LINES.items():
            rules[model] = expression.AND([base, ['|', ('ttype', '!=', 'one2many'), ('name', 'in', lines)]])
        rules['default_automatic_rule'] = expression.AND([base, [('ttype', '!=', 'one2many')]])
        return rules

    def action_logs_partout_enable(self):
        """Keep the history of every field of these screens."""
        models = self.filtered(lambda m: m.is_mail_thread and m.model in self.env)
        models.write({'active_custom_tracking': True, 'automatic_custom_tracking': True})
        for model in models:
            # recomputed so that the rules above (lines, noisy fields) apply
            model._compute_automatic_custom_tracking_domain()
        models.update_custom_tracking()
        self.env.registry.clear_cache()
        return True

    def action_logs_partout_disable(self):
        self.write({'active_custom_tracking': False})
        self.env.registry.clear_cache()
        return True

    @api.model
    def _logs_partout_activate_defaults(self):
        models = self.sudo().search([('model', 'in', DEFAULT_MODELS)])
        models.action_logs_partout_enable()
        return models

    def action_logs_partout_open_history(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window', 'name': _('Historique : %s', self.name),
            'res_model': 'mail.tracking.value', 'view_mode': 'list',
            'domain': [('mail_message_id.model', '=', self.model)],
            'view_id': self.env.ref('logs_partout.mail_tracking_value_logs_partout_list').id,
            'search_view_id': self.env.ref('logs_partout.mail_tracking_value_logs_partout_search').id,
        }
