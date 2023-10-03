from odoo import fields,api,models
import requests
import base64
from pdf2docx import parse
from odoo.exceptions import UserError

class ExamQuestion(models.Model):
    _name="exam.question"
    _order="sequence"
    name = fields.Char(string="Name")
    index = fields.Integer()
    question = fields.Html(string="Question")
    question_type = fields.Selection(selection=[('mcq','MCQ'),('other','Other')], string="Question Type", default='mcq')
    mcq_answer = fields.Selection(selection=[('A','A'),('B','B'),('C','C'),('D','D')], string="MCQ Answer",default="A")
    option_a = fields.Char(string="MCQ Option A")
    option_b = fields.Char(string="MCQ Option B")
    option_c = fields.Char(string="MCQ Option C")
    option_d = fields.Char(string="MCQ Option D")
    sequence = fields.Integer(string='Sequence', default=10)
    def make_copy(self):
        question = self
        name = question.name
        i=0
        for i in range(20):
            self.env['exam.question'].create({
                'name' : name+"cpy"+str(i),
                'question': question.question,
                'question_type': question.question_type,
                'mcq_answer': question.mcq_answer,
                'option_a' : question.option_a,
                'option_b' : question.option_b,
                'option_c' : question.option_c,
                'option_d' : question.option_d,
            })


class ExamPaper(models.Model):
    _name="exam.paper"
    name = fields.Char(string="Paper Name")
    course = fields.Many2one('logic.base.courses',string="Course")
    questions = fields.Many2many('exam.question',string="Questions")
    questions_html = fields.Html()
    docx_qpaper = fields.Binary()
    docx_answer_key = fields.Binary()
    filename = fields.Char(default="exam_paper")


    def get_answers_list(self):
        i=1
        answers = []
        for question in self.questions:
            if question.question_type =='mcq' and question.mcq_answer:
                answers.append(str(i)+") "+question.mcq_answer)
            i+=1
        length=len(answers)
        rem = length%3
        divs = length//3
        if rem==1:
            col1_lim = divs+1
            col2_lim = col1_lim + divs
        elif rem==2:
            col1_lim = divs+1
            col2_lim = col1_lim + divs + 1
        else:
            col1_lim = divs
            col2_lim = col1_lim + divs
        col3_lim = col2_lim + divs

        col1_values = answers[0:col1_lim]
        col2_values = answers[col1_lim:col2_lim]
        col3_values = answers[col2_lim:col3_lim]

        answers_final=[]
        for i in range(col1_lim):
            vals = []
            vals.append(col1_values[i])
            try:
                vals.append(col2_values[i])
            except:
                vals.append(' ')
            try:
                vals.append(col3_values[i])
            except:
                vals.append(' ')
            answers_final.append(vals)
        return answers_final

    def download_paper_docx(self):
        record = self.env['exam.paper'].browse(self.id)

        i=1
        #add index to html field (remove after downloading docx)
        for question in record.questions:
            try:
                question.question = question.question[0:3] + str(i)+") " + question.question[3:]
            except:
                pass
            i+=1

        template = self.env.ref('exam_logic.action_question_paper_report')
        html_content = template._render_qweb_pdf([record.id])[0]
        outfile = open('/tmp/temp.pdf','wb')
        outfile.write(html_content)
        outfile.close()

        #remove indexes from html fields (questions)
        for question in record.questions:
            try:
                question.question = question.question[0:3] + question.question[6:]
            except:
                pass

        open('/tmp/temp.docx','w')
        
        parse('/tmp/temp.pdf', '/tmp/temp.docx')


        self.docx_qpaper = base64.b64encode(open('/tmp/temp.docx','rb').read())
        return {
            'name': 'Download Paper',
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=exam.paper&id={}&field=docx_qpaper&filename_field=filename&download=true'.format(
                self.id
            ),
            'target': 'self',
        }
    
    def download_answer_key_docx(self):
        record = self.env['exam.paper'].browse(self.id)
        template = self.env.ref('exam_logic.action_answer_key_report')
        html_content = template._render_qweb_pdf([record.id])[0]
        outfile = open('/tmp/temp.pdf','wb')
        outfile.write(html_content)
        outfile.close()

        open('/tmp/temp.docx','w')
        
        parse('/tmp/temp.pdf', '/tmp/temp.docx')
        self.docx_answer_key = base64.b64encode(open('/tmp/temp.docx','rb').read())
        return {
            'name': 'Download Answer Key',
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=exam.paper&id={}&field=docx_answer_key&filename_field=filename&download=true'.format(
                self.id
            ),
            'target': 'self',
        }
    
