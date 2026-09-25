# -*- coding: utf-8 -*-
"""Global list « qui a changé quoi, quand » over all the tracked screens."""
from odoo import fields, models


class MailTrackingValue(models.Model):
    _inherit = 'mail.tracking.value'

    lp_date = fields.Datetime('Date', related='mail_message_id.date', store=True, index=True)
    lp_author_id = fields.Many2one('res.partner', 'Modifié par', related='mail_message_id.author_id', store=True,
                                   index=True)
    lp_model = fields.Char('Modèle', related='mail_message_id.model', store=True, index=True)
    lp_res_id = fields.Many2oneReference('ID', related='mail_message_id.res_id', model_field='lp_model')
    lp_record_name = fields.Char('Fiche', compute='_compute_lp_display')
    lp_model_name = fields.Char('Écran', compute='_compute_lp_display')
    lp_field_name = fields.Char('Champ', compute='_compute_lp_display')
    lp_old = fields.Char('Ancienne valeur', compute='_compute_lp_display')
    lp_new = fields.Char('Nouvelle valeur', compute='_compute_lp_display')

    def _compute_lp_display(self):
        names = {m.model: m.name for m in self.env['ir.model'].sudo().search([('model', 'in', self.mapped('lp_model'))])}
        for tracking in self:
            field_type = tracking.field_id.ttype or (tracking.field_info or {}).get('type') or 'char'
            tracking.lp_model_name = names.get(tracking.lp_model, tracking.lp_model)
            tracking.lp_field_name = tracking.field_id.field_description or (tracking.field_info or {}).get('desc')
            old = tracking._format_display_value(field_type, new=False)[0]
            new = tracking._format_display_value(field_type, new=True)[0]
            tracking.lp_old = '' if old in (None, False) else str(old)
            tracking.lp_new = '' if new in (None, False) else str(new)
            record_name = tracking.mail_message_id.record_name
            if not record_name and tracking.lp_model in self.env and tracking.lp_res_id:
                record = self.env[tracking.lp_model].sudo().browse(tracking.lp_res_id).exists()
                record_name = record.display_name if record else ''
            tracking.lp_record_name = record_name

    def action_lp_open_record(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window', 'res_model': self.lp_model, 'res_id': self.lp_res_id,
                'view_mode': 'form'}
