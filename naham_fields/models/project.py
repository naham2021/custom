from odoo import models, fields, api

class project_task(models.Model):
    _inherit = 'project.task'
    sale_order_project = fields.Many2one('sale.order')
    partner_project = fields.Many2many('res.partner')
    profit = fields.Integer()
    Collection_from_the_customer = fields.Integer()
    purchaseorder = fields.Many2one('purchase.order')
    completion_percentage = fields.Char()
    text = fields.Char()
    status_sale = fields.Many2one('status')
    type_sale = fields.Many2many('project.sale.type')
    task_sale = fields.Many2one('task.catogary')

class status(models.Model):
    _name = 'status'
    name = fields.Char(translate=True)
class type(models.Model):
    _name = 'project.sale.type'
    name = fields.Char(translate=True)
class taskcatogary(models.Model):
    _name = 'task.catogary'
    name = fields.Char(translate=True)


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
class project_project_inherit(models.Model):
    _inherit = 'project.project'

    user_id_task = fields.Many2many('res.users', compute='calc_user', store=True)
    @api.depends('task_ids.user_id')
    def calc_user(self):
        for rec in self:
            for u in rec.task_ids:
                print('------------------------------')
                print(u.user_id)
                rec.user_id_task = [(4, u.user_id.id)]





