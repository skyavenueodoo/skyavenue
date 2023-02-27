from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move.line'

    phase = fields.Char(string='Phase',store=True)
    co_per = fields.Float(string='Percentage',store=True)
    project_amount = fields.Float(string='Rental Price',store=True)
    name = fields.Char(string='Label', tracking=True, default="/")

    @api.onchange('co_per', 'project_amount')
    def _onchange_field_name(self):
        if self.co_per and self.project_amount :
            self.price_unit = self.co_per * self.project_amount / 100
