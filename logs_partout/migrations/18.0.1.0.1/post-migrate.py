# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Image / file fields were tracked by the first version: untrack them."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.model']._logs_partout_untrack_unsupported()
