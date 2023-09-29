from odoo import models,fields,api
from odoo.exceptions import UserError
import math  
from . import pie_chart

class ExamDetails(models.Model):
    _name = 'exam.details'
    name = fields.Char(string="Exam Name", store=True)
    date = fields.Date(string="Exam Date")
    exam_type = fields.Selection([('quarterly', 'Quarterly Exam'), ('topic', 'Topic wise Exam'),('half_model','Half Model'),('model_exam','Model Exam')],string='Exam Type')
    topic = fields.Char(string="Topic")
    quart_percent = fields.Selection([('25','25%'), ('50', '50%'), ('75', '75%'), ('100', '100%')], string='Quarterly Percent')
    batch = fields.Many2one('logic.base.batch',string="Batch")
    classroom = fields.Many2one('logic.base.class',string="Class",domain="[('batch_id','=',batch)]")
    def get_coordinator_domain(self):
        return [('id', 'in', self.env.ref('exam_logic.group_exam_coordinator').users.ids)]
    coordinator = fields.Many2one('res.users',default=lambda self: self.env.user.id, domain=get_coordinator_domain)
    pass_percentage = fields.Float(string="Pass Percentage", compute="_compute_pass_fail_percentage",default=0)
    fail_percentage = fields.Float(string="Fail Percentage", compute="_compute_pass_fail_percentage",default=0)
    faculty = fields.Many2many('res.users',string="Faculty", domain=[('faculty_check','=',True)])
    class_teacher = fields.Many2one('hr.employee',string="Class Teacher")
    student_results = fields.One2many('logic.student.result','exam_id', string='Students',store=True)
    pass_mark = fields.Integer(string="Pass Mark")
    total_marks = fields.Integer(string="Total Marks", default=100)
    present_students = fields.Integer(string="Attended Students",compute="_compute_total_attendance")        
    average_marks = fields.Float(string="Average Marks", compute="_compute_average_marks")
    bokeh_chart = fields.Text(string="Result Chart",compute = "_compute_bokeh_chart")
    students_added = fields.Boolean(string="Students Added", default=False, help="To identify if students result records are added to the form")
    
    def create_student_results(self):
        # for record in self:
            # if not record.student_results:
        if not self.classroom:
            raise UserError("You have to assign a class before adding students!")
        class_allocated_stud_ids = []
        for stud_line in self.classroom.line_base_ids:
            class_allocated_stud_ids.append(stud_line.student_id.id)
        students = self.env['logic.students'].search([
                ('id', 'in', class_allocated_stud_ids)])
        if not students:
            raise UserError("Selected class does not have any students allocated!")
        self.env['logic.student.result'].search([('exam_id','=',self.id)]).unlink()
        for student in students:
            student_result = self.env['logic.student.result'].create({
                'student_id': student.id,
                'marks':0,
                'exam_id': self.id,
                'present': True,
            })
        # self.student_results = self.env['logic.student.result'].search([('exam_id','=',self.id)])
        self.students_added = True
    def reset_student_results(self):
        # for record in self:
        # self.env['logic.student.result'].search([('exam_id','=',self.id)]).unlink()
        for result in self.student_results:
            result.unlink()
        self.students_added = False
    @api.depends('present_students')
    def _compute_bokeh_chart(self):
        for record in self:
            # Design your bokeh figure:
            record.bokeh_chart = pie_chart.get_chart_component(record)

    @api.depends('present_students')
    def _compute_pass_fail_percentage(self):
        for record in self:
            pass_count = 0
            fail_count = 0
            for result in record.student_results:
                if result.present:
                    if result.marks >= record.pass_mark:
                        pass_count+=1
                    else:
                        fail_count+=1
                else:
                    continue
            if record.present_students > 0:
                record.pass_percentage = round((pass_count/record.present_students)*100, 1)
                record.fail_percentage = round(100-record.pass_percentage,1)
            else:
                record.pass_percentage=0
                record.fail_percentage=0

    @api.depends('student_results')
    def _compute_total_attendance(self):
        for record in self:
            total=0
            for result in record.student_results:
                if result.present:
                    total+=1
            record.present_students = total

    @api.depends('student_results')
    def _compute_average_marks(self):
        for record in self:
            total=0
            for result in record.student_results:
                total += result.marks
            if record.present_students > 0:
                record.average_marks = total/record.present_students
            else:
                record.average_marks=0
            
    # @api.depends('date', 'exam_type', 'batch')
    # def _compute_name(self):    
    #     for record in self:    
    #         if not record.date:
    #             raise UserError("A date must be set for the exam before saving!")       
    #         date = fields.Date.from_string(
    #             record.date).strftime('%Y/%m/%d')
    #         # exam_type = dict(self._fields['exam_type']._description_selection(self.env))[self.exam_type]
    #         if record.exam_type=="quarterly":
    #             exam_type="Q"+record.quart_percent
    #         else:
    #             exam_type="T"
    #         record.name = str(record.batch.name) + "-" + str(exam_type) + "-" + str(date)
    
    # @api.onchange('student_results')
    # def _compute_students(self):    
    #     for record in self:
    #         record.total_students=len(record.student_results)

