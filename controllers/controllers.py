# -*- coding: utf-8 -*-
# from odoo import http


# class AttendanceModificationRequest(http.Controller):
#     @http.route('/attendance_modification_request/attendance_modification_request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/attendance_modification_request/attendance_modification_request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('attendance_modification_request.listing', {
#             'root': '/attendance_modification_request/attendance_modification_request',
#             'objects': http.request.env['attendance_modification_request.attendance_modification_request'].search([]),
#         })

#     @http.route('/attendance_modification_request/attendance_modification_request/objects/<model("attendance_modification_request.attendance_modification_request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('attendance_modification_request.object', {
#             'object': obj
#         })
