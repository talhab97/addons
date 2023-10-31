from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"

    property_id = fields.Many2one('estate.property', 'Property')
    price = fields.Float('Price')
    status = fields.Selection([('accepted', 'Accepted'), ('reject', 'Rejected')], string='Status')
    partner_id = fields.Many2one('res.partner', 'Partner')
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='calculate_dl', inverse='_inverse_dl')

    @api.depends('validity')
    def calculate_dl(self):
        for rec in self:
            if rec.validity:
                rec.date_deadline = fields.Date.today() + timedelta(days=rec.validity)

    def _inverse_dl(self):
        for rec in self:
            if rec.date_deadline:
                rec.validity = int((rec.date_deadline - fields.Date.today()).days)

    def action_reject(self):
        for rec in self:
            rec.status = 'reject'
            rec.property_id.selling_price = False
            rec.property_id.buyer = False

    def action_accept(self):
        for rec in self:
            rec.property_id.selling_price = rec.price
            rec.status = 'accepted'
            rec.property_id.buyer = rec.partner_id.name

    @api.constrains('date_deadline')
    def _check_date_deadline(self):

        for record in self:

            if record.date_deadline and record.date_deadline < fields.Date.today():
                raise ValidationError("The deadline cannot be set in the past")

    @api.constrains('action_accept')
    def _check_selling_price(self):

        for rec in self:
            if rec.action_accept:
                if rec.property_id.selling_price < 90 % rec.property_id.expected_price:
                    raise ValidationError("Selling Price is too low")

    _sql_constraints = [
        ('check_price', 'check(price > 0)', 'Offer Price must be greater than zero.')
    ]
