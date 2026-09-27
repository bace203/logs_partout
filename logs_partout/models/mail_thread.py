# -*- coding: utf-8 -*-
from odoo import models

from .ir_model import UNTRACKABLE_TYPES


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _track_get_fields(self):
        """Safety net: an image or file field is never tracked, whatever the configuration
        (Posify cannot write it in the history and would block the save)."""
        names = super()._track_get_fields()
        if not names:
            return names
        return {name for name in names
                if name not in self._fields or self._fields[name].type not in UNTRACKABLE_TYPES}
