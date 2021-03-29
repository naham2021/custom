
from odoo import models, fields, api


class saleorder(models.Model):
    _inherit = 'sale.order'
    payment_sale = fields.Many2one('payment')
    payment_way_sale = fields.Many2many('payment.way')
    installation_sale = fields.Many2one('installation')
    valid_untill_sale = fields.Date('valid.untill')
    Delivery_sale = fields.Many2one('delivery.sale')
    operation_requirment_sale = fields.Many2many('operation.requirment')
    Travel_civil_work_sale = fields.Many2one('travel.civil.work')
    warranty_sale = fields.Many2many('warranty')
    warranty_location_sale = fields.Many2one('warranty.location')
    duration_of_technical_support_sale = fields.Many2one('duration.of.technical.support')
    training_sale = fields.Many2one('training')
    Software_sale = fields.Many2one('software')
    delivery_place_sale = fields.Many2one('delivery.place')
    Quote_type = fields.Many2one('quote.type')
    Quote_stage = fields.Many2one('quote.stage')
    sale_probability = fields.Float('')
    profit = fields.Integer()
    buyfromus = fields.Integer()



class payment(models.Model):
    _name = 'payment'
    _rec_name = 'payment'
    payment = fields.Char(translate=True)

class payment_way(models.Model):
    _name = 'payment.way'
    name = fields.Char(translate=True)
class Installation(models.Model):
    _name = 'installation'
    name = fields.Char(translate=True)
class Delivery(models.Model):
    _name = 'delivery.sale'
    name = fields.Char(translate=True)
class Operation_Requirment(models.Model):
    _name = 'operation.requirment'
    name = fields.Char(translate=True)
class Travel_civil_work(models.Model):
    _name = 'travel.civil.work'
    name = fields.Char(translate=True)
class Warranty(models.Model):
    _name = 'warranty'
    name = fields.Char(translate=True)
class Warranty_Location(models.Model):
    _name = 'warranty.location'
    name = fields.Char(translate=True)
class Duration_of_technical_support(models.Model):
    _name = 'duration.of.technical.support'
    name = fields.Char(translate=True)
class Training(models.Model):
    _name = 'training'
    name = fields.Char(translate=True)
class Software(models.Model):
    _name = 'software'
    name = fields.Char(translate=True)
class Delivery_Place(models.Model):
    _name = 'delivery.place'
    name = fields.Char(translate=True)

class Quote_type(models.Model):
    _name = 'quote.type'
    name = fields.Char(translate=True)
class Quote_stage(models.Model):
    _name = 'quote.stage'
    name = fields.Char(translate=True)

