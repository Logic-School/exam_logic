{
    'name': "Exams",
    'author': 'Rizwaan',
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'logic_base','web_widget_bokeh_chart'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
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