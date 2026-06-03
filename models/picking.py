from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # New fields based on the ABI picking list
    driver_name = fields.Char(string="Driver No")
    truck_no = fields.Char(string="Truck No")
    delivery_via = fields.Char(string="Delivery Via")
    builty_no = fields.Char(string="Builty No")
    seal_no = fields.Char(string="Seal No")
    x_deliver_to_id = fields.Many2one('res.partner', string="Deliver To")

    # Storage location 3151 mapping
    storage_location_code = fields.Char(string="Storage Location", default="3151")
    po_no = fields.Char(string="PO No/Date")


class StockMove(models.Model):
    _inherit = 'stock.move'

    # Short text for Gate Pass line description
    short_text = fields.Char(string="Short Text")

    # Breakdown quantities for the table
    qty_pak = fields.Float(string="Qty (PAK)", compute="_compute_breakdown_qtys", store=True)
    qty_ctn = fields.Float(string="Qty (CTN)", compute="_compute_breakdown_qtys", store=True)
    qty_pcs = fields.Float(string="Qty (PCS)", compute="_compute_breakdown_qtys", store=True)

    @api.depends('product_uom_qty', 'product_id', 'product_id.packaging_ids')
    def _compute_breakdown_qtys(self):
        for move in self:
            # qty_pcs = raw delivery qty (as-is)
            move.qty_pcs = move.product_uom_qty
            
            # Find packaging for CTN (carton)
            ctn_packaging = move.product_id.packaging_ids.filtered(
                lambda p: 'ctn' in p.name.lower() or 'carton' in p.name.lower()
            )
            move.qty_ctn = move.product_uom_qty / ctn_packaging.qty if ctn_packaging and ctn_packaging.qty else 0.0
            
            # Find packaging for PAK (pack)
            pak_packaging = move.product_id.packaging_ids.filtered(
                lambda p: 'pak' in p.name.lower() or 'pack' in p.name.lower()
            )
            move.qty_pak = move.product_uom_qty / pak_packaging.qty if pak_packaging and pak_packaging.qty else 0.0