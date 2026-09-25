# -*- coding: utf-8 -*-
"""A chatter (standard mail.thread) on the business screens that do not have one, so that their changes are kept."""
from lxml import etree

from odoo import api, models


class LogsPartoutChatterMixin(models.AbstractModel):
    _name = 'logs.partout.chatter.mixin'
    _description = 'Chatter ajouté (historique des modifications)'

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        # added to whatever form is used (standard or customised), at the end, like <chatter/> in standard views
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type == 'form' and not arch.xpath('//chatter'):
            arch.append(etree.Element('chatter'))
        return arch, view


class StockLocation(models.Model):
    _name = 'stock.location'
    _inherit = ['stock.location', 'mail.thread', 'logs.partout.chatter.mixin']


class StockWarehouse(models.Model):
    _name = 'stock.warehouse'
    _inherit = ['stock.warehouse', 'mail.thread', 'logs.partout.chatter.mixin']


class StockPickingType(models.Model):
    _name = 'stock.picking.type'
    _inherit = ['stock.picking.type', 'mail.thread', 'logs.partout.chatter.mixin']


class StockRoute(models.Model):
    _name = 'stock.route'
    _inherit = ['stock.route', 'mail.thread', 'logs.partout.chatter.mixin']


class PosCategory(models.Model):
    _name = 'pos.category'
    _inherit = ['pos.category', 'mail.thread', 'logs.partout.chatter.mixin']


class PosConfig(models.Model):
    _name = 'pos.config'
    _inherit = ['pos.config', 'mail.thread', 'logs.partout.chatter.mixin']


class PosPaymentMethod(models.Model):
    _name = 'pos.payment.method'
    _inherit = ['pos.payment.method', 'mail.thread', 'logs.partout.chatter.mixin']


class LoyaltyProgram(models.Model):
    _name = 'loyalty.program'
    _inherit = ['loyalty.program', 'mail.thread', 'logs.partout.chatter.mixin']


class UomUom(models.Model):
    _name = 'uom.uom'
    _inherit = ['uom.uom', 'mail.thread', 'logs.partout.chatter.mixin']


class ResPartnerCategory(models.Model):
    _name = 'res.partner.category'
    _inherit = ['res.partner.category', 'mail.thread', 'logs.partout.chatter.mixin']


class AccountPaymentTerm(models.Model):
    _name = 'account.payment.term'
    _inherit = ['account.payment.term', 'mail.thread', 'logs.partout.chatter.mixin']


class ProductAttribute(models.Model):
    _name = 'product.attribute'
    _inherit = ['product.attribute', 'mail.thread', 'logs.partout.chatter.mixin']
