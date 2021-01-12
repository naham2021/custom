# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class PickingInherit(models.Model):
    _inherit = 'stock.picking'

    def copy(self, default=None):
        if self.env.user.has_group('naham_group_transfer.naham_picking_duplicate_group'):
            return super(PickingInherit, self).copy(default)
        raise exceptions.UserError("You do not have permission to duplicate.")

    def unlink(self):
        if self.env.user.has_group('naham_group_transfer.naham_picking_delete_group'):
            return super(PickingInherit, self).unlink()
        raise exceptions.UserError("You do not have permission to delete.")
