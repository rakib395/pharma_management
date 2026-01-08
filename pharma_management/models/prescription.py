from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PharmaPrescription(models.Model):
    _name = 'pharma.prescription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Prescription'

    doctor_id = fields.Many2one('pharma.doctor', string='Doctor', required=True)
    representative_id = fields.Many2one('pharma.representative', string='Representative', required=True)
    prescription_date = fields.Date(string='Date', default=fields.Date.today, required=True)
    medicine_line_ids = fields.One2many('pharma.prescription.line', 'prescription_id', string='Medicines')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    @api.depends('medicine_line_ids.subtotal')
    def _compute_total(self):
        for record in self:
            record.total_amount = sum(record.medicine_line_ids.mapped('subtotal'))

    def action_confirm(self):
        """Confirm the prescription and reduce stock"""
        for record in self:
            if record.state != 'draft':
                continue
            
            for line in record.medicine_line_ids:
               
                if line.medicine_id.stock_qty < line.quantity:
                    raise ValidationError(f"{line.medicine_id.name} {line.medicine_id.stock_qty}")
                
                
                line.medicine_id.stock_qty -= line.quantity
            
           
            record.state = 'confirmed'
        return True

    def action_cancel(self):
        self.state = 'cancelled'

class PharmaPrescriptionLine(models.Model):
    _name = 'pharma.prescription.line'
    _description = 'Prescription Line'

    prescription_id = fields.Many2one('pharma.prescription')
    medicine_id = fields.Many2one('pharma.medicine', string='Medicine', required=True)
    quantity = fields.Integer(string='Quantity', default=1, required=True)
    price_unit = fields.Float(related='medicine_id.price', string='Unit Price', readonly=True)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit