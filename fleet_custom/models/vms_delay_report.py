from odoo import models, fields, api, _
from odoo.exceptions import UserError

class VmsDelay_Report(models.Model):
    _name = 'vms.delay_report'
    _description = 'VMS Delay Report'

    request_id = fields.Many2one(
        'vms.request', 
        string="Driver Request", 
        required=True,
       domain="[('state', 'in', ['draft', 'specification', 'supervisor','approval'])]"
    )
    
    date_reported = fields.Datetime(
        string="Date Reported", 
        default=fields.Datetime.now, # Automatically sets the current time
        readonly=True
    )
    
    driver_id = fields.Many2one(
        related='request_id.driver_id', 
        string="Driver", 
        store=True, 
        readonly=True
    )
    
    site_engineer_id = fields.Many2one(
        'res.users', 
        string="Site Engineer", 
        default=lambda self: self.env.user, 
        readonly=True
    )
    
    # The actual file data
    attachment_file = fields.Binary(string="Signed Request File")
    
    # Stores the name of the file (required for the filename attribute in XML)
    attachment_name = fields.Char(string="Attachment Name")
    
    # The text area for escalation reasons
    notes = fields.Text(string="Escalation Notes")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Waiting Manager'),
        ('reported', 'Alarm Active (GM Review)'),
        ('approved', 'Approved (Alarm Stopped)'),
    ], default='draft', string="Status")

    # --- NEW METHODS TO FIX THE ERROR ---

    def action_submit(self):
        """ Triggered by 'Submit for Review' button """
        for record in self:
            record.state = 'submitted'
        return True

    def action_return(self):
        """ NEW: Triggered by 'Return to Engineer' button """
        for record in self:
            record.state = 'draft'
        return True

    def action_continue(self):
        """ Triggered by 'Escalate to GM' button """
        for record in self:
            record.state = 'reported'
        return True

    def action_gm_approve(self):
        for record in self:
            if record.request_id:
                record.request_id.action_approve() 
            record.state = 'approved'
        return True