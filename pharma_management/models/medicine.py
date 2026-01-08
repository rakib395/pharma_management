from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PharmaMedicine(models.Model):
    _name = 'pharma.medicine'
    _description = 'Medicine Catalog'

    name = fields.Char(string='Medicine Name', required=True)
    code = fields.Char(string='Code', required=True, copy=False)
    category = fields.Selection([
        ('tablet', 'Tablet'), ('syrup', 'Syrup'), 
        ('injection', 'Injection'), ('capsule', 'Capsule'), ('other', 'Other')
    ], string='Category', default='tablet')
    price = fields.Float(string='Price', required=True)
    stock_qty = fields.Integer(string='Stock Quantity', default=0)
    is_low_stock = fields.Boolean(string='Low Stock', compute='_compute_low_stock')

    _sql_constraints = [('unique_code', 'unique(code)', 'Medicine code must be unique!')]

    @api.depends('stock_qty')
    def _compute_low_stock(self):
        for record in self:
            record.is_low_stock = record.stock_qty < 10

    @api.constrains('stock_qty')
    def _check_stock(self):
        for record in self:
            if record.stock_qty < 0:
                raise ValidationError("Stock cannot be negative!")