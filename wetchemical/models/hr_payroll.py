# -*- coding: utf-8 -*-
import time
import babel
from odoo.tools import float_round, date_utils
from odoo.tools.misc import format_date
from odoo import models, fields, api, tools, _
from datetime import datetime


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    loan_line_id = fields.Many2one('hr.loan.line', string="Loan Installment", help="Loan installment")

class HrPayslipInputType(models.Model):
    _inherit = "hr.payslip.input.type"

    default_value = fields.Float(default=0.0,string="Default Value")
    default = fields.Boolean(default=False,string="Add by Default")

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.onchange('employee_id', 'struct_id', 'contract_id', 'date_from', 'date_to')
    def _onchange_employee(self):
        super(HrPayslip,self)._onchange_employee()
        input_lines = self.input_line_ids.browse([])
        res = self._get_input_lines()
        for r in res:
            input_lines |= input_lines.new(r)
        self.input_line_ids = input_lines

    def action_payslip_done(self):
        for line in self.input_line_ids:
            if line.loan_line_id:
                line.loan_line_id.paid = True
                line.loan_line_id.loan_id._compute_loan_amount()
        return super(HrPayslip, self).action_payslip_done()
    
    # @api.model
    # def create(self, vals):
    #     res = super(HrPayslip, self).create(vals)
    #     it_obj = res.env['hr.payslip.input.type'].search([('code','=','LO')])
    #     lon_obj = res.env['hr.loan'].search([('employee_id', '=', res.employee_id.id), ('state', '=', 'approve')])
    #     if res.date_from and res.date_to and res.employee_id.id and res.struct_id:
    #         for loan in lon_obj:
    #             for loan_line in loan.loan_lines:
    #                 if res.date_from <= loan_line.date <= res.date_to and not loan_line.paid:
    #                     r = res.input_line_ids.search([('code','=','LO')])
    #                     if not r:
    #                         #res.write({'input_line_ids':[(0,0,{'input_type_id': res[0],'amount': loan_line.amount,'loan_line_id': loan_line.id,'code':'LO'})]})
    #                         new_line = [(0,0,{'input_type_id': it_obj[0].id,'amount': loan_line.amount,'loan_line_id': loan_line.id,'code':'LO'})]
    #                         # if res.input_line_ids:
    #                         #     res.input_line_ids += new_line
    #                         # else:
    #                         res.input_line_ids = new_line
    #
    #                     # for result in res:
    #                     #     if result.get('code') == 'LO':
    #                     #         result['amount'] = loan_line.amount
    #                     #         result['loan_line_id'] = loan_line.id

    def _get_input_lines(self):
        """

        :return:
        """
        res = []
        self.ensure_one()
        input_type_obj = self.env['hr.payslip.input.type'].search([('code', '=', 'LO')])
        lon_obj = self.env['hr.loan'].search([('employee_id', '=', self.employee_id.id), ('state', '=', 'approve')])
        for loan in lon_obj:
            for loan_line in loan.loan_lines:
                if self.date_from <= loan_line.date <= self.date_to and not loan_line.paid:
                    input_line = {
                        'input_type_id': input_type_obj[0].id,
                        'amount': loan_line.amount,
                        'loan_line_id': loan_line.id,
                        'code':'LO'
                    }
                    if input_line not in res:
                        res.append(input_line)
        input_type_obj = self.env['hr.payslip.input.type'].search([('default', '=', True)])
        if self.struct_id:
            for i in input_type_obj:
                if self.struct_id.id in i.struct_ids.ids:
                    input_line = {
                        'input_type_id': i.id,
                        'amount': i.default_value,
                        'code': i.code
                    }
                    res.append(input_line)
        return res
