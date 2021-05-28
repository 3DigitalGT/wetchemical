# -*- coding: utf-8 -*-
import time
import babel
from odoo.tools import float_round, date_utils
from odoo.tools.misc import format_date
from odoo import models, fields, api, tools, SUPERUSER_ID
from odoo.tools.safe_eval import safe_eval
from datetime import datetime



class Stage(models.Model):
    """ Model for case stages. This models the main stages of a document
        management flow. Main CRM objects (leads, opportunities, project
        issues, ...) will now use only stages, instead of state and stages.
        Stages are for example used to display the kanban view of records.
    """
    _inherit = "crm.stage"

    tipo = fields.Selection([
        ('A','Clientes Actuales'),
        ('N', 'Clientes Nuevos'),
    ], string="Tipo Etapa")

class Team(models.Model):
    _inherit = 'crm.team'

    #TODO JEM : refactor this stuff with xml action, proper customization,
    @api.model
    def action_your_pipeline_wet(self):
        t = self.env.context.get('team')
        if t == 1:
            action = self.env.ref('crm.crm_lead_action_pipeline').read()[0]
        else:
            action = self.env.ref('wetchemical.crm_lead_action_pipeline_5').read()[0]
        user_team_id = t

        action_context = safe_eval(action['context'], {'uid': self.env.uid})
        if user_team_id:
            action_context['default_team_id'] = user_team_id

        action['context'] = action_context
        return action

class Lead(models.Model):
    _inherit = "crm.lead"

    tipo = fields.Selection(related='stage_id.tipo',store=True)

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        # retrieve team_id from the context and write the domain
        # - ('id', 'in', stages.ids): add columns that should be present
        # - OR ('fold', '=', False): add default columns that are not folded
        # - OR ('team_ids', '=', team_id), ('fold', '=', False) if team_id: add team columns that are not folded
        # tipo = self._context.get('tipo','A')
        tipo = self._context.get('default_tipo')
        # if team_id == 5:
        #     search_domain = [('tipo','=', 'N')]
        # else:
        #     search_domain = [('tipo','=', 'A')]
        search_domain = [('tipo', '=', tipo)]
        stgs = self.env['crm.stage'].search([])
        # perform search
        stage_ids = stgs._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def _default_team_id(self, user_id):
        # domain = [('use_leads', '=', True)] if self._context.get('default_type') == "lead" or self.type == 'lead' else [('use_opportunities', '=', True)]
        return self._context.get('default_team_id')