from odoo import models,fields,api

class ExamDetails(models.Model):
    _name = 'exam.details'
    date = fields.Date(string="Exam Date")
    exam_type = fields.Selection([('quarterly', 'Quarterly Exam'), ('topic', 'Topic wise Exam')],
                                        string='Exam Type')
    batch = fields.Many2one('logic.batches',string="Batch")
    classroom = fields.Many2one('class.room',string="Class Room")
    faculty = fields.Many2one()
    student_attended = fields.Integer(compute='',string='Attended Students')
    pass_percentage = fields.Integer(compute='',string="Pass Percentage")
    fail_percentage = fields.Integer(compute='', string="Fail Percentage")
    faculty = fields.Many2one('faculty.details',string="Faculty")
    class_teacher = fields.Many2one('hr.employee',string="Class Teacher")
