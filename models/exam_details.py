from odoo import models,fields,api

class ExamDetails(models.Model):
    _name = 'exam.details'
    name = fields.Char(string="Exam Name",compute = "_compute_name", store=True)
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
    student_results = fields.Many2many('student.result',string='Students',domain="[('student_id.batch','=',batch)]")
            
    @api.depends('date', 'exam_type', 'batch')
    def _compute_name(self):    
        for record in self:        
            date = fields.Date.from_string(
                record.date).strftime('%Y-%m-%d')
            exam_type = dict(self._fields['exam_type']._description_selection(self.env))[self.exam_type]
            record.name = str(record.batch.batch_name) + " " + str(exam_type) + str(date)