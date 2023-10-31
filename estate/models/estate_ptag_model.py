from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = " Property Tags"

    name = fields.Char(string='Tags')

    _sql_constraints = [
        ('unique_tag_ids', 'unique(tag_ids)', 'Tag must be unique.')

    ]
