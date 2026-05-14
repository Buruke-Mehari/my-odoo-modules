{
    'name': 'VMS Custom',
    'version': '1.0',
    'category': 'Logistics',
    'depends': ['base','hr','utm' ,'mail', 'fleet'],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/vms_request_view.xml',
        'views/vms_delay_report_view.xml',
        'data/ir_cron_data.xml',
    ],
    'installable': True,
    'application': True,
}