from odoo import fields, models, api, _


class ResUsersExt(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'user_id', domain=[('state', '=', 'This property is sold.')])
