# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    credit_debit = fields.Selection(
        [
            ("Credito", "Credito"),
            ("Debito    ", "Debito")
        ],
        string="Condicion",
        default='credit'
    )