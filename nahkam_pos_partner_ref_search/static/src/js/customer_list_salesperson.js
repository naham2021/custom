odoo.define('nahkam_pos_partner_ref_search.ClientSalesperson', function (require) {
    "use strict";
    var Models = require('point_of_sale.models')

    Models.load_fields('res.partner',['salesperson_name','partner_credit','partner_debit','area_id','area_name'])
    Models.load_fields('res.users',['area_ids'])
    Models.load_models({
        model:  'partner.area',
        fields: ['name'],
        domain: function(self) {return [['id', '=', self.user.area_ids]];},
        loaded: function(self,areas){
            self.areas = areas;
        },
    })

    return Models
});