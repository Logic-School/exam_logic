{
    'name': "Exams",
    'author': 'Rizwaan',
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'logic_base','admission','faculty','web_widget_bokeh_chart'],
    'data': [
        'security/ir.model.access.csv',
        'views/exam_details.xml',
        'views/exam_result.xml',
        'views/question_paper.xml',
        'report/question_paper_report.xml',
    ],
    'demo': [],
    'summary': "Logic Exams",
    'description': "",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}