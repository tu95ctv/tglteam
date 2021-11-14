odoo.define('web_favorites_to_tabview.list_view', function (require) {
"use strict";

var rpc = require('web.rpc');
var FavoriteMenu = require('web.FavoriteMenu');
var AbstractController = require('web.AbstractController')
var core = require('web.core');
var _t = core._t;
var qweb = core.qweb;


FavoriteMenu.include({
    events: _.extend({}, FavoriteMenu.prototype.events, {
        'click .tgl_action_filter_list_view button': 'tgl_action_filter_list_view',
    }),
    tgl_action_filter_list_view: function() {
        this.do_action({
            name:'Filter',
            type: 'ir.actions.act_window',
            domain: [['action_id', '=', this.action.id]],
            res_model: 'ir.filters',
            views: [[false, 'list']],
            target: 'current'
        }); 
    },
    append_filter: function (filter) {
        this._super(filter);
        this.$filters[this.key_for(filter)].addClass('tgl-config-tab tgl_config_tab_'+filter.id);
    },
    toggle_filter: function (filter, preventSearch){
        this._super(filter, preventSearch);
        var selected = $('.tgl-config-tab.tgl_config_tab_'+filter.id+' .dropdown-item');
        if(selected.hasClass('selected')){
            $('li.tgl-display-tab').removeClass('active');
            $('li.tgl-display-tab.tgl_display_tab_'+filter.id).addClass('active');
        }else{
            $('li.tgl-display-tab').removeClass('active');
            $('li.tgl-display-tab.tgl_display_tab_0').addClass('active');
        }
    },

    remove_filter: function (filter, $filter, key){
        this._super(filter, $filter, key);
        $('li.tgl-display-tab.tgl_config_tab_'+filter.id).remove();
        if($('li.tgl-display-tab').length === 1){
            $('li.tgl-display-tab.tgl_display_tab_0').remove();
        }
    }
});

var AddButtons = {
    buttons: function(viewInfo){     
        var action_id = _.last(_.pluck(viewInfo.getParent().actions, 'id'));
        rpc.query({
            model: 'ir.filters',
            method: 'search_read',
            args: [[['show_in_tab', '=', 1], ['model_id', '=', viewInfo.modelName], ['action_id', '=', action_id]], ['name', 'id']],
        })
        .then(function (filters) {
            $('.tgl_ul_tabs').remove();
            if(filters.length === 0) return;
            var parentview = $('.o_control_panel');

            parentview.append("<ul class='nav nav-tabs tgl_ul_tabs'></ul>");
            var ul = parentview.find('.tgl_ul_tabs');
            var li_all = "<li class='tgl-display-tab tgl_display_tab_0'><a>Tất cả</a></li>";
            ul.append(li_all);
            var li_on_click_0 = $('li.tgl-display-tab.tgl_display_tab_0');

            li_on_click_0.on('click', function(){
                _.each(filters, function(filter){
                    var selected = $('.tgl-config-tab.tgl_config_tab_'+filter.id+' .dropdown-item');
                    if (selected.hasClass('selected')) selected.click();// cấu trúc lạ
                });
            });

            _.each(filters, function(filter){
                var selected = $('.tgl-config-tab.tgl_config_tab_'+filter.id);
                ul.append("<li class='tgl-display-tab tgl_display_tab_"+filter.id+"'><a>"+filter.name+"</a></li>");
                var li_on_click = $('li.tgl-display-tab.tgl_display_tab_'+filter.id);

                li_on_click.on('click', function(){
                    selected.click();
                })
            });

            var filter_selected = {}
            _.each(filters, function(filter){
                var selected = $('.tgl-config-tab.tgl_config_tab_'+filter.id+' .dropdown-item');
                if(selected.hasClass('selected')) {
                    filter_selected = filter;
                }
            });

            if (filter_selected.id) {
                $('li.tgl-display-tab').removeClass('active');
                $('li.tgl-display-tab.tgl_display_tab_'+filter_selected.id).addClass('active');
            }else{
                $('li.tgl-display-tab').removeClass('active');
                $('li.tgl-display-tab.tgl_display_tab_0').addClass('active');
            }
        })
    },
};

AbstractController.include({
    _update: function (state) {
        if ((state.viewType === "kanban") || (state.viewType === "list"))
            AddButtons.buttons(this);
        else 
            $('.tgl_ul_tabs').remove();
        return this._super.apply(this, arguments);
    },
});

});