odoo.define('web_tree_group_header.ListRenderer', function (require) {
"use strict";

var ListRenderer = require('web.ListRenderer');

ListRenderer.include({

    _renderHeaderTreeMerge: function (group_name) {
        if (!_.find(this.columns, function(column){ return column.attrs.modifiers[group_name]})) { 
            return '';
        }
        var $tr_mg = $('<tr>'),
            count_title_mg = 0,
            count_colpan = 0,
            title_mg = this.columns[0].attrs.modifiers[group_name];
        var th_tag = '<th class="o_list_record_selector" ></th>'
        // $tr_mg.append(th_tag);
        _.each(this.columns, function(column) {
            if (column.attrs.modifiers[group_name] !== title_mg) {
                th_tag = `<th class="text-center" colspan="${count_title_mg}">${title_mg || ''}</th>`;
                $tr_mg.append(th_tag);
                count_colpan += count_title_mg
                count_title_mg = 1;
                title_mg = column.attrs.modifiers[group_name];
            } else {
                count_title_mg++;
            }    
        });
        th_tag = `<th class="text-center" colspan="${count_title_mg}">${title_mg || ''}</th>`;
        count_colpan += count_title_mg;
        $tr_mg.count_colpan = count_colpan;

        return $tr_mg.append(th_tag);
    },

    _renderHeader: function () {
        var $thead = $('<thead>'),
            count_empty = 0,
            i = 0,
            $merge_group3 = this._renderHeaderTreeMerge('merge_group3'),
            $merge_group2 = this._renderHeaderTreeMerge('merge_group2'),
            $merge_group1 = this._renderHeaderTreeMerge('merge_group1')

        var $tr = $('<tr>')
            .append(_.map(this.columns, this._renderHeaderCell.bind(this)));
        if (this.hasSelectors) {
            $tr.prepend(this._renderSelector('th'));
            if ($merge_group3 != '') $merge_group3.prepend('<th>')
            if ($merge_group2 != '') $merge_group2.prepend('<th>')
            if ($merge_group1 != '') $merge_group1.prepend('<th>')
        }
        if ($merge_group3 != '') {
            count_empty = $tr.find('th').length - $merge_group3.count_colpan
            for (i=0; i < count_empty; i++) {
                $merge_group3.prepend($('<th>'));
            }
        }
        if ($merge_group2 != '') {
            count_empty = $tr.find('th').length - $merge_group2.count_colpan
            for (i=0; i < count_empty; i++) {
                $merge_group2.prepend($('<th>'));
            }
        }
        if ($merge_group1 != '') {
            count_empty = $tr.find('th').length - $merge_group1.count_colpan
            for (i=0; i < count_empty; i++) {
                $merge_group1.prepend($('<th>'));
            }
        }

        $thead.append($merge_group3)
        $thead.append($merge_group2)
        $thead.append($merge_group1)

        return $thead.append($tr);
    },

});

});