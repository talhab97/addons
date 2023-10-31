from odoo import fields, models


class EstateSettings(models.Model):
    _name = "estate.property.type"
    _description = "Model for Property Types"

    name = fields.Char(string='Name')
    properties_id = fields.Many2one("estate.property", string="Property Types")

    _sql_constraints = [
        ('unique_properties_id', 'unique(properties_id)', 'Property type  must have a unique name.')
    ]
