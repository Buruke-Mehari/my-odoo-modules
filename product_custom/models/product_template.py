from odoo import models, fields, api

class ProductCustomFieldDefinition(models.Model):
    _name = 'product.custom.field.definition'
    _description = 'Custom Field Definition'

    name = fields.Char(string="Field Name", required=True)
    field_type = fields.Selection([
        ('char', 'Text'),
        ('date', 'Date'),
        ('selection', 'Selection')
    ], string="Field Type", default='char', required=True)
    
    selection_options = fields.Text(string="Options", help="Comma-separated values for Selection type")

class ProductCustomFieldValue(models.Model):
    _name = 'product.custom.field.value'
    _description = 'Product Custom Field Value'

    product_tmpl_id = fields.Many2one('product.template', string="Product", ondelete='cascade')
    
    field_definition_id = fields.Many2one('product.custom.field.definition', string="Field", required=True)
    
    value_selection_id = fields.Many2one(
        'product.custom.field.option', 
        string="Selected Option"
    )
    field_type = fields.Selection(related='field_definition_id.field_type', string="Field Type", store=True)

    value_text = fields.Char(string="Text Value")
    value_date = fields.Date(string="Date Value")
    # Storage fields
    value_char = fields.Char(string="Text Value")
    value_date = fields.Date(string="Date Value")
  
class ProductCustomFieldOption(models.Model):
    _name = 'product.custom.field.option' # THIS MUST MATCH THE Many2one ABOVE
    _description = 'Value Options'
    
    name = fields.Char(string="Option Value", required=True)
    field_definition_id = fields.Many2one('product.custom.field.definition', string="Field Definition")  

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    custom_field_line_ids = fields.One2many(
        'product.custom.field.value', 
        'product_tmpl_id', 
        string="Custom Specifications"
    )