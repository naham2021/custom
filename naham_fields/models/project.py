from odoo import models, fields, api

class project_task(models.Model):
    _inherit = 'project.task'
    sale_order_project = fields.Many2one('sale.order')
    partner_project = fields.Many2many('res.partner')

class partner(models.Model):
    _inherit = 'res.partner'
    tasks_count = fields.Integer(string='Tasks', compute='get_count_task')

    def get_count_task(self):
        for r in self:
            count = r.env['project.task'].search_count([('partner_project', '=', r.id)])
            r.tasks_count = count
    def project_button(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'open_project',
            'view_mode': 'tree,form',
            'res_model': 'project.task',
            'domain': [('partner_project', '=', self.id)],

        }




