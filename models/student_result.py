from odoo import models,api,fields

class StudentExamResult(models.Model):
    _name= "student.result"
    student_id = fields.Many2one("student.details",string="Student")
    name = fields.Char(related="student_id.name")
    marks = fields.Integer(string="Marks")
    present = fields.Boolean(string="Attendance")

    # @api.onchange("student_id")    
    # def onchange_student_id(self):
    #     if self.student_id:    
    #         self.name = self.student_id.name
