{
    'name': "Logic Exam",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'logic_base','admission','Faculty','web_widget_bokeh_chart'],
    'data': [
        'security/ir.model.access.csv',
        'views/exam_details.xml',
        'views/exam_result.xml',

    ],
    'demo': [],
    'summary': "Logic Exam",
    'description': "",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': True
}