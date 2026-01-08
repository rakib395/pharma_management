from odoo import models, fields, api

class PharmaWizardPrescription(models.TransientModel):
    _name = 'pharma.wizard.prescription'
    _description = 'Prescription Creation Assistant'

    doctor_ids = fields.Many2many('pharma.doctor', string='Doctors', required=True)
    representative_id = fields.Many2one('pharma.representative', string='Representative', required=True)
    prescription_date = fields.Date(string='Date', default=fields.Date.today)
    medicine_id = fields.Many2one('pharma.medicine', string='Medicine', required=True)
    quantity = fields.Integer(string='Quantity', default=1, required=True)

    def action_generate_prescriptions(self):
        prescription_obj = self.env['pharma.prescription']
        for doctor in self.doctor_ids:
            prescription_obj.create({
                'doctor_id': doctor.id,
                'representative_id': self.representative_id.id,
                'prescription_date': self.prescription_date,
                'medicine_line_ids': [(0, 0, {
                    'medicine_id': self.medicine_id.id,
                    'quantity': self.quantity,
                })]
            })
        return {'type': 'ir.actions.act_window_close'}