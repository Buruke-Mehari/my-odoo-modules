from odoo import models, fields, api

class VMSRequest(models.Model):
    _name = 'vms.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Vehicle Management Request'
    _order = 'create_date desc'
    _rec_name = 'request_category'

    # Ensure this name matches the XML field name
    request_category = fields.Selection([
        ('contract', 'Contract'),
        ('service', 'Service'),
        ('maintenance', 'Maintenance'),
        ('fuel','Fuel')
        
    ], string="Request Category", required=True, tracking=True)
    
    driver_id = fields.Many2one(
        'res.users', 
        string="Driver", 
        default=lambda self: self.env.user, 
        tracking=True,
        required=True
    )

    photo_ids = fields.One2many('vms.request.photo', 'request_id', string="Photos")

    state = fields.Selection([
        ('draft', 'Driver Initiation'),
        ('specification', 'Fleet Specification'),
    ], default='draft', tracking=True)

    def action_submit_to_fleet(self):
        for record in self:
            record.state = 'specification'
    
            
    def action_return_to_draft(self):
       for record in self:
        # Moves it back so the driver can edit again
          record.state = 'draft'      
     

class VMSRequestPhoto(models.Model):
    _name = 'vms.request.photo'
    _description = 'Vehicle Request Photo'

    request_id = fields.Many2one('vms.request', string="Request Reference", ondelete='cascade')
    image = fields.Binary(string="Photo", required=True, attachment=True) # Added attachment=True
    description = fields.Char(string="Photo Description")
    
class VMSRequest(models.Model):
    _inherit = 'vms.request' # Use this if adding to existing, or just add fields to the class

    # New Fleet Fields
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle", tracking=True)
    # For the money spent
    total_cost = fields.Float(string="Total Cost", tracking=True)

# For the volume of fuel
    fuel_qty = fields.Float(string="Litres", digits=(16, 2), tracking=True)
    
    # Specific Sub-types based on category
    contract_type = fields.Selection([
        ('insurance', 'Insurance'),
        ('bolo', 'Bolo')
    ], string="Contract Detail")

    service_type = fields.Selection([
        ('engine_oil', 'Engine Oil Change'),
        ('oil_filter', 'Oil Filter Replacement'),
        ('fuel_filter','Fuel Filter Replacement'),
        ('air_filter','Air Filter Service'),
        ('tire_rotation','Tire Rotation'),
        ('tire_replacement','Full Tire Replacement')
    ], string="Service Detail")

    maintenance_type = fields.Selection([
        ('broken_part', 'Broken Part Replacement'),
        ('other', 'Other Repair')
    ], string="Maintenance Detail")

    # State update for the new workflow
    state = fields.Selection([
        ('draft', 'Driver Initiation'),
        ('specification', 'Fleet Specification'),
        ('supervisor', 'Supervisor Approval'),
    ], default='draft', tracking=True)

    def action_submit_to_supervisor(self):
        for record in self:
            record.state = 'supervisor'
            
    def action_return_to_specification(self):
       for record in self:
        # Moves it back so the driver can edit again
          record.state = 'specification' 
    
    state = fields.Selection([
        ('draft', 'Driver Initiation'),
        ('specification', 'Fleet Specification'),
        ('supervisor', 'Supervisor Approval'),
        ('approval','Manger Approval')
    ], default='draft', tracking=True)
    
    def action_submit_to_approval(self):
        for record in self:
            record.state = 'approval'
            
    def action_return_to_supervisor(self):
       for record in self:
        # Moves it back so the driver can edit again
          record.state = 'supervisor'     
      
    state = fields.Selection([
        ('draft', 'Driver Initiation'),
        ('specification', 'Fleet Specification'),
        ('supervisor', 'Supervisor Approval'),
        ('approval','Manger Approval'),
        ('approved','Approved')
    ], default='draft', tracking=True)   
    
    def action_submit_to_approved(self):
        for record in self:
            record.state = 'approved'     