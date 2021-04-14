# -*- coding: utf-8 -*-

from odoo import models, fields, api

class NewModule(models.Model):
    _inherit = 'project.project'

    stage_id = fields.Many2one(comodel_name="project.task.type", string="Stage", required=False, )