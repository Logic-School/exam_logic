from odoo import models,api,fields

class StudentExamResult(models.Model):
    _name= "logic.student.result"
    student_id = fields.Many2one("logic.students",string="Student")
    # name = fields.Char(related="student_id.name")

    def _get_default_exam_id(self):
        active_id = self.env.context.get('active_id')
        return active_id
    exam_id = fields.Many2one("exam.details", string="Exam", domain="[('company_id', '=', current_company_id)]")
    marks = fields.Integer(string="Marks")
    present = fields.Boolean(string="Attendance")

    # @api.onchange("student_id")    
    # def onchange_student_id(self):
    #     if self.student_id:    
    #         self.name = self.student_id.name
