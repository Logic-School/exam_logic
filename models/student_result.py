from odoo import models,api,fields

class StudentExamResult(models.Model):
    _name= "logic.student.result"
    student_id = fields.Many2one("logic.students",string="Student")
    # name = fields.Char(related="student_id.name")

    def _get_default_exam_id(self):
        active_id = self.env.context.get('active_id')
        return active_id
    exam_id = fields.Many2one("exam.details", string="Exam",)
    marks = fields.Integer(string="Marks")
    present = fields.Boolean(string="Attendance")
