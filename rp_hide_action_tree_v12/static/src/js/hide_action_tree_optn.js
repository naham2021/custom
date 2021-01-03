odoo.define('rp_hide_action_tree_v12.hide_action_tree_optn', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var session = require('web.session');
    var core = require('web.core');
    var _t = core._t;

    ListController.include({

        willStart: function () {
            var self = this;
            var def = this._super.apply(this, arguments)
            var def1 = this.getSession().user_has_group('rp_hide_action_tree_v12.group_tree_archive_access').then(function (has_archive_group) {
                self.has_archive_group = has_archive_group;
            });
            var def2 = this.getSession().user_has_group('rp_hide_action_tree_v12.group_tree_delete_access').then(function (has_delete_group) {
                self.has_delete_group = has_delete_group;
            });
            var def3 = this.getSession().user_has_group('rp_hide_action_tree_v12.group_tree_export_access').then(function (has_export_group) {
                self.has_export_group = has_export_group;
            });
            return $.when(def, def1, def2, def3);;
        },

        /**
         * Display the sidebar (the 'action' menu in the control panel) if we have
         * some selected records.
         */
        _toggleSidebar: function () {
            var self = this
            this._super.apply(this, arguments);
            if (this.sidebar && this.mode === 'readonly') {
                if (!this.has_archive_group) {
                    this.sidebar.items.other = _.reject(this.sidebar.items.other, function (item) {
                        return item.label === 'Archive';
                    });
                    this.sidebar.items.other = _.reject(this.sidebar.items.other, function (item) {
                        return item.label === 'Unarchive';
                    });
                }
                if (!this.has_delete_group) {
                    this.sidebar.items.other = _.reject(this.sidebar.items.other, function (item) {
                        return item.label === 'Delete';
                    });
                }
                if (!this.has_export_group) {
                    this.sidebar.items.other = _.reject(this.sidebar.items.other, function (item) {
                        return item.label === 'Export';
                    });
                }
                this.sidebar.items.other;
            }
        },
    });
});
