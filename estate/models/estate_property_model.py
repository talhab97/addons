from odoo import api, fields, models
from odoo.exceptions import UserError
# from odoo.exceptions import ValidationError


class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Post Code')
    date_availability = fields.Date(string='Date Availability', default=fields.Date.context_today)
    expected_price = fields.Float(string='Expected Price')
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
                                          string='Garden Oreintation')
    properties_id = fields.Many2one("estate.property", string="Property Type")
    buyer = fields.Char(string='Buyer')
    salesman = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Float(string='Total Area', compute='area_sum')
    best_offer = fields.Char(string='Best Price', compute='get_max')
    state = fields.Char(string='Status')
    user_id = fields.Many2one('res.users', "User ID")

    @api.depends('living_area', 'garden_area')
    def area_sum(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def get_max(self):
        for rec in self:
            if rec.offer_ids:
                partners = max(rec.offer_ids.mapped('price'))
                rec.best_offer = partners
            else:
                rec.best_offer = False

    @api.onchange('garden')
    def _onchange_garden(self):
        for rec in self:
            if rec.garden == True:
                rec.garden_area = 10
            else:
                rec.garden_area = 0

    def action_cancel(self):
        for rec in self:
            if self.state == "This property is sold.":
                raise UserError("Sold Property Can be Canceled")
            else:
                rec.state = "Canceled"

    def action_sold(self):
        for rec in self:
            if self.state == "Canceled":
                raise UserError("Canceled Property Can be Sold")
            else:
                rec.state = "This property is sold."


    _sql_constraints = [
        ('check_expected_price', 'check(expected_price > 0)', 'Expected Price must be greater than zero.'),
        ('check_selling_price', 'check(selling_price >= 0)', 'Selling Price must be greater than zero.'),

    ]
