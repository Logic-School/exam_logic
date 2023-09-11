from odoo import http
from odoo.http import request
from odoo.exceptions import UserError

class HtmlReportController(http.Controller):
    @http.route('/exam_logic/html_report/<int:record_id>',type='http', auth='user')
    def download_html_report(self,record_id):
        record = request.env['exam.paper'].browse(record_id)
        template = request.env.ref('exam_logic.action_question_paper_report')
        # qweb = request.env['ir.qweb']
        html_content = template._render_qweb_html([record.id])[0]
        file = open('/tmp/test1.html','w')
        record.write({'docx_file':html_content})
        record.ret_field()
        # raise UserError(html_content.decode('utf-8'))
        # file.write(html_content)
        return request.make_response(
            html_content,
            headers=[('Content-Type', 'text/html')],
        )
