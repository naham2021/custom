odoo.define('nakham_pos_no_add_product.no_add_product', function (require) {
"use strict";

var module = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var core = require('web.core');
var QWeb = core.qweb;
var _t = core._t;
var models = module.PosModel.prototype.models;

screens.ProductCategoriesWidget.include({

    perform_search: function(category, query, buy_result){
        var products;
        if(query){
            products = this.pos.db.search_product_in_category(category.id,query);
            if(buy_result && products.length === 1){
//                    this.pos.get_order().add_product(products[0]);
                    this.clear_search();
            }else{
                this.product_list_widget.set_product_list(products);
            }
        }else{
            products = this.pos.db.get_product_by_category(this.category.id);
            this.product_list_widget.set_product_list(products);
        }
    },
//    perform_search: function(category, query, buy_result){
////        console.log("perform_search by Thomas")
//        var products;
//        if(query){
//            products = this.pos.db.search_product_in_category(category.id,query);
//            if(buy_result && products.length === 1){
////                    this.pos.get_order().add_product(products[0]);
//                    this.clear_search();
//            }else{
//                this.product_list_widget.set_product_list(products, query);
//            }
//        }else{
//            products = this.pos.db.get_product_by_category(this.category.id);
//            this.product_list_widget.set_product_list(products, query);
//        }
//    },

});
});