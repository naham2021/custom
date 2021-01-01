odoo.define('nahkam_pos_partner_ref_search.HighlitedInvoice', function (require) {
    "use strict";

    var models = require('point_of_sale.models');

    //this code make the invoice button in the payment screen highlited by default

    var _super = models.Order;
    models.Order = models.Order.extend({
        initialize: function(attributes,options){
            var sup_val= _super.prototype.initialize.call(this, attributes, options);
            this.to_invoice  = true;
            return sup_val;
        }
    });

    return models;
});
odoo.define('nahkam_pos_partner_ref_search.disableInvoice', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');

    //this code make the invoice button in the payment screen disabled


    screens.PaymentScreenWidget.include({
      click_invoice: function(){
        var order = this.pos.get_order();
//        order.set_to_invoice(!order.is_to_invoice());
        console.log(order.is_to_invoice())
        if (order.is_to_invoice()) {
            this.$('.js_invoice').addClass('highlight');

        } else {
            this.$('.js_invoice').removeClass('highlight');
        }
    },
    });

    return screens;
});