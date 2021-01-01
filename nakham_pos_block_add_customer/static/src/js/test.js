//alert("Loading");
//console.log("Loading again")
odoo.define("nakham_pos_block_add_customer.add_customer_blocked",function (require){
    "use strict";
    var chrome = require('point_of_sale.chrome');
    var pos = require('point_of_sale.models');
    var gui = require('point_of_sale.gui');
    var popup = require('point_of_sale.popups');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;
    var Screens = require('point_of_sale.screens');
//    console.log("Welcome OdOO JS ",pos)
    console.log("Screens",Screens)

Screens.ClientListScreenWidget.include({
        show: function(){
        var self = this;
        this._super();

        this.renderElement();
        this.details_visible = false;
        this.old_client = this.pos.get_order().get_client();

        this.$('.back').click(function(){
            self.gui.back();
        });

        this.$('.next').click(function(){
            self.save_changes();
            self.gui.back();    // FIXME HUH ?
        });

        this.$('.new-customer').click(function(){
            console.log("new-custome")
            self.display_client_details('edit',{
                'country_id': self.pos.company.country_id,
                'state_id': self.pos.company.state_id,
            });
        });

        var partners = this.pos.db.get_partners_sorted(1000);
        this.render_list(partners);

        this.reload_partners();

        if( this.old_client ){
            this.display_client_details('show',this.old_client,0);
        }

        this.$('.client-list-contents').on('click', '.client-line', function(event){
            self.line_select(event,$(this),parseInt($(this).data('id')));
        });

        var search_timeout = null;

        if(this.pos.config.iface_vkeyboard && this.chrome.widget.keyboard){
            this.chrome.widget.keyboard.connect(this.$('.searchbox input'));
        }

        this.$('.searchbox input').on('keypress',function(event){
            clearTimeout(search_timeout);

            var searchbox = this;

            search_timeout = setTimeout(function(){
                self.perform_search(searchbox.value, event.which === 13);
            },70);
        });

        this.$('.searchbox .search-clear').click(function(){
            self.clear_search();
        });
    },

});



});