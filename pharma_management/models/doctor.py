from odoo import models, fields, api

class PharmaDoctor(models.Model):
    _name = 'pharma.doctor'
    _description = 'Doctor Management'

    name = fields.Char(string='Name', required=True)
    specialization = fields.Char(string='Specialization')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    city = fields.Char(string='City')
    
    prescription_count = fields.Integer(string='Total Prescriptions', compute='_compute_prescription_count')

    def _compute_prescription_count(self):
        for record in self:
            record.prescription_count = self.env['pharma.prescription'].search_count([('doctor_id', '=', record.id)])