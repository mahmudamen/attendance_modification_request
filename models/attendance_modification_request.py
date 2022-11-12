from odoo import fields, models, api, _
from datetime import datetime, date



class AttendanceModificationRequest(models.Model):
    _name = 'attendance.modification.request'
    _rec_name = 'name'
    _inherit = 'mail.thread'

    name = fields.Char(string='name',readonly=True)
    employee = fields.Many2one('hr.employee' ,string='employee')
    create_on = fields.Date(string='Date',default=datetime.today())
    type = fields.Selection([('checkin', 'Checkin'),('checkout', 'Checkout'),('both', 'Both')])
    reason = fields.Text('Reason')
    action_to_do = fields.Selection([('new record', 'New Record'),('modification', 'Modification')])
    attendance = fields.Many2one('hr.attendance',string='Attendance',stored=True)

    @api.onchange('employee')
    def _onchangeemployee(self):
        for rec in self:
            return {'domain':{'attendance':[('employee_id','=',rec.employee.id)]}}

    check_in = fields.Datetime(string="Check In")
    check_out = fields.Datetime(string="Check Out")

    @api.onchange('attendance')
    def _checkin_checkout(self):

        for rec in self:
            self.check_in = self.attendance.check_in
            self.check_out = self.attendance.check_out

    state = fields.Selection([('draft', 'draft'),
                              ('wait for approve', 'wait for approve'),
                              ('approve', 'approve'),('reject','reject')],
                             string="State",default='draft',stored=True)

    def confirm(self):
        if self.state == 'draft':
            self.name = self.env['ir.sequence'].next_by_code('attendance_modification_request_seq')
            self.state = 'wait for approve'
            # find user id for employee Manager first
            manager_id = self.env['hr.employee'].search([('id','=',self.employee.id)])
            if manager_id.parent_id.id:
                user_id = self.env['res.users'].sudo().search([('employee_id','=',manager_id.parent_id.id)])
                # create messages for manager
                message_id = self.env['mail.message'].create({'message_type': "notification",
                                                 'body': self.employee.name + ' - ' + str(self.attendance.check_in) + ' - ' + str(self.attendance.check_out),
                                                 'subject': self.name + ' / ' + str(self.create_on),
                                                 'model': 'attendance.modification.request',
                                                 'record_name':self.name,
                                                 'parent_id': user_id.partner_id.id,
                                                 'res_id': self.id,
                                                 'needaction':True,
                                                 'subtype_id': 1,
                                                 'date': date.today().strftime('%Y-%m-%d'),
                                                 })
                if self.employee.parent_id.id:
                    # create notification for manager
                    notification = {
                        'mail_message_id': message_id.id,
                        'is_read': False,
                        'res_partner_id': user_id.partner_id.id,
                        'notification_type': 'inbox',
                        'notification_status': 'sent',
                    }
                    self.env['mail.notification'].create(notification)

    def approve(self):
        if self.state == 'wait for approve':
            self.state = 'approve'

    def reject(self):
        if self.state == 'wait for approve':
            self.state = 'reject'
            return {
                'name': 'reason rejection',
                'view_mode': 'form',
                'view_id': self.env.ref('attendance_modification_request.hr_rejected_form_view').id,
                'res_model': 'hr.rejected',
                'domain': [],
                'context': {'default_request_id':self.id},
                'type': 'ir.actions.act_window',
                'target': 'new',
            }


    @api.onchange('check_in','check_out')
    def onchangecheckinout(self):
        if self.attendance:
            checkinout = self.env['hr.attendance'].sudo().search([('id','=',self.attendance.id)])
            checkinout.write({'check_in': self.check_in})
            checkinout.write({'check_out':self.check_out})


class rejected(models.Model):
    _name = 'hr.rejected'

    request_id = fields.Many2one('attendance.modification.request')
    reason = fields.Char(string='reason')


