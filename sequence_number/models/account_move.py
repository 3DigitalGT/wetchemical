# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveInherit(models.Model):
    _description = 'Modulo heredado de account.move para obtener la secuencia'
    _inherit = 'account.move'

    adenda_sequence = fields.Integer(string='CI adenda', compute='_get_adenda_sequence')

    @api.onchange('journal_id')
    def _get_adenda_sequence(self):
        if self.journal_id:
            self. adenda_sequence = self.journal_id.sequence_number_next
