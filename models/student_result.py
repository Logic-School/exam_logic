from odoo import models,api,fields

class StudentExamResult(models.Model):
    _name= "logic.student.result"
    def _compute_name(self):
        for record in self:
            record.name = record.student_id.name  + " - " + record.exam_id.name
    name = fields.Char(string="Name",compute="_compute_name")
    student_id = fields.Many2one("logic.students",string="Student", required=True)
    # name = fields.Char(related="student_id.name")

    def _get_default_exam_id(self):
        parent_id = self.env.context.get('parent_id') 
        parent_model = self.env.context.get('parent_model')       
        if parent_id and parent_model:
            parent_obj = self.env[parent_model].browse(parent_id)
            return parent_obj.id
    
    exam_id = fields.Many2one("exam.details", ondelete='cascade',required=True, string="Exam",default=_get_default_exam_id)
    total_marks = fields.Integer(string="Total Marks",related="exam_id.total_marks")
    marks = fields.Integer(string="Scored Marks")
    present = fields.Boolean(string="Attendance")
