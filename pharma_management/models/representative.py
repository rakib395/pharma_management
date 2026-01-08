from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PharmaRepresentative(models.Model):
    _name = 'pharma.representative'
    _description = 'Medical Representative'

    name = fields.Char(string='Name', required=True)
    employee_id = fields.Char(string='Employee ID', required=True, copy=False)
    region = fields.Char(string='Region')
    phone = fields.Char(string='Phone')
    target_value = fields.Float(string='Target Value', default=0.0)
    total_sales = fields.Float(string='Total Sales', compute='_compute_sales')
    achievement_rate = fields.Float(string='Achievement Rate (%)', compute='_compute_sales')
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active')

    _sql_constraints = [
        ('unique_employee_id', 'unique(employee_id)', 'Employee ID must be unique!')
    ]

    @api.constrains('target_value')
    def _check_target_value(self):
        for record in self:
            if record.target_value < 0:
                raise ValidationError("Target value cannot be negative!")

    def _compute_sales(self):
        for record in self:
            prescriptions = self.env['pharma.prescription'].search([
                ('representative_id', '=', record.id),
                ('state', '=', 'confirmed')
            ])
            total = sum(prescriptions.mapped('total_amount'))
            record.total_sales = total
            record.achievement_rate = (total / record.target_value * 100) if record.target_value > 0 else 0