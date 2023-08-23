from odoo import fields,api,models
import requests
import base64
from pdf2docx import parse
from odoo.exceptions import UserError

class ExamQuestion(models.Model):
    _name="exam.question"
    name = fields.Char(string="Name")
    index = fields.Integer()
    question = fields.Html(string="Question")
    question_type = fields.Selection(selection=[('mcq','MCQ'),('other','Other')], string="Question Type", default='mcq')
    mcq_answer = fields.Selection(selection=[('A','A'),('B','B'),('C','C'),('D','D')], string="MCQ Answer")
    option_a = fields.Char(string="MCQ Option A")
    option_b = fields.Char(string="MCQ Option B")
    option_c = fields.Char(string="MCQ Option C")
    option_d = fields.Char(string="MCQ Option D")

class ExamPaper(models.Model):
    _name="exam.paper"
    name = fields.Char(string="Paper Name")
    questions = fields.Many2many('exam.question',string="Questions")
    questions_html = fields.Html()
    docx_file = fields.Binary()
    filename = fields.Char(default="exam_paper")


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


        self.docx_file = base64.b64encode(open('/tmp/temp.docx','rb').read())
        return {
            'name': 'Download Paper',
            'type': 'ir.actions.act_url',
            'url': '/web/content/?model=exam.paper&id={}&field=docx_file&filename_field=filename&download=true'.format(
                self.id
            ),
            'target': 'self',
        }


