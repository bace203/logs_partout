# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestLogsPartout(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env['ir.model']._logs_partout_activate_defaults()

    def _flush_tracking(self):
        # the chatter tracking is written when the transaction is committed (like Posify's own mail tests)
        self.env.flush_all()
        self.env.cr.precommit.run()
        self.env.flush_all()

    def _changes(self, record):
        """{field name: (old, new)} of the tracking values posted on the record."""
        messages = self.env['mail.message'].search([('model', '=', record._name), ('res_id', '=', record.id)])
        result = {}
        for tracking in messages.tracking_value_ids:
            result[tracking.field_id.name] = (tracking.lp_old, tracking.lp_new)
        return result

    def test_product_every_field(self):
        product = self.env['product.template'].create({'name': 'Daurade', 'list_price': 28.49,
                                                       'default_code': 'LP1'})
        self._flush_tracking()          # (a record created in the same transaction is not tracked)
        product.write({'list_price': 30.0, 'default_code': 'LP2', 'barcode': '2413501000000',
                       'description_sale': 'Fraîche'})
        self._flush_tracking()
        changes = self._changes(product)
        self.assertEqual(changes['default_code'], ('LP1', 'LP2'))
        self.assertIn('list_price', changes)
        # the barcode belongs to the variant: its change is logged on the product too
        bodies = ' '.join(self.env['mail.message'].search(
            [('model', '=', 'product.template'), ('res_id', '=', product.id)]).mapped('body'))
        self.assertIn('2413501000000', bodies)
        self.assertIn('description_sale', changes)

    def test_image_change_does_not_block(self):
        """An image is not tracked: changing it must not raise (was: 'Unsupported tracking on field image_1920')."""
        png = ('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==')
        partner = self.env['res.partner'].create({'name': 'Photo'})
        product = self.env['product.template'].create({'name': 'Photo'})
        self._flush_tracking()
        tracked = self.env['ir.model.fields'].search([('custom_tracking', '=', True), ('ttype', '=', 'binary')])
        self.assertFalse(tracked)
        partner.write({'image_1920': png, 'phone': '22513690'})
        product.write({'image_1920': png})
        self._flush_tracking()
        self.assertIn('phone', self._changes(partner))
        self.assertNotIn('image_1920', self._changes(partner))

    def test_screen_without_chatter_gets_one(self):
        location = self.env['stock.location'].create({'name': 'Réserve', 'usage': 'internal'})
        self._flush_tracking()
        arch = self.env['stock.location'].get_view(view_type='form')['arch']
        self.assertIn('chatter', arch)
        location.write({'name': 'Réserve B'})
        self._flush_tracking()
        self.assertEqual(self._changes(location)['name'], ('Réserve', 'Réserve B'))
        for model in ('pos.category', 'pos.config', 'loyalty.program', 'stock.warehouse', 'uom.uom'):
            self.assertIn('message_ids', self.env[model]._fields, model)

    def test_lines_logged_on_parent(self):
        pricelist = self.env['product.pricelist'].create({'name': 'Promo LP'})
        self._flush_tracking()
        pricelist.write({'item_ids': [(0, 0, {'compute_price': 'fixed', 'fixed_price': 9.5,
                                               'applied_on': '3_global'})]})
        self._flush_tracking()
        messages = self.env['mail.message'].search([('model', '=', 'product.pricelist'), ('res_id', '=', pricelist.id)])
        self.assertTrue(messages.filtered(lambda m: m.tracking_value_ids or 'Règle' in (m.body or '')
                                          or m.body), 'the new pricelist rule is logged on the pricelist')

    def test_loyalty_program(self):
        program = self.env['loyalty.program'].create({'name': 'Fidélité LP', 'program_type': 'loyalty'})
        self._flush_tracking()
        program.write({'name': 'Fidélité LP 2'})
        self._flush_tracking()
        self.assertEqual(self._changes(program)['name'], ('Fidélité LP', 'Fidélité LP 2'))

    def test_settings_screen(self):
        IrModel = self.env['ir.model']
        product = IrModel._get('product.template')
        self.assertTrue(product.active_custom_tracking)
        self.assertGreater(product.tracked_field_count, 20)
        pos_order = IrModel._get('pos.order')
        self.assertFalse(pos_order.active_custom_tracking)          # high volume: off by default
        pos_order.action_logs_partout_enable()
        self.assertTrue(pos_order.active_custom_tracking)
        pos_order.action_logs_partout_disable()
        self.assertFalse(pos_order.active_custom_tracking)
        self.assertNotIn('write_date', product.field_id.filtered('custom_tracking').mapped('name'))

    def test_global_history(self):
        partner = self.env['res.partner'].create({'name': 'Client LP'})
        self._flush_tracking()
        partner.write({'phone': '71000000'})
        self._flush_tracking()
        history = self.env['mail.tracking.value'].search([('lp_model', '=', 'res.partner'),
                                                          ('mail_message_id.res_id', '=', partner.id)])
        phone = history.filtered(lambda t: t.field_id.name == 'phone')
        self.assertEqual((phone.lp_new, phone.lp_record_name, phone.lp_model_name), ('71000000', 'Client LP',
                                                                                    'Contact'))
        self.assertEqual(phone.lp_author_id, self.env.user.partner_id)
