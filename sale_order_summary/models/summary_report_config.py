# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.safe_eval import safe_eval as safe_eval
from odoo.tools.misc import formatLang
from odoo.tools import date_utils, float_utils
from dateutil.relativedelta import relativedelta

    
DATE_RANGE_TYPES = [
    ('today', 'Today'),
    ('yesterday', 'Yesterday'),
    ('this_month', 'This month'),
    ('last_month', 'Last_month'),
    ('this_year', 'This Year'),
    ('last_year', 'Last Year'),
]

class SummaryReportConfigLine(models.Model):
    _name = 'summary.report.config.line'
    _order = 'sequence'

    summary_report_config_id = fields.Many2one('summary.report.config')
    domain = fields.Char()
    name = fields.Char()
    model_id = fields.Many2one('ir.model', required=True)
    model_name = fields.Char(related='model_id.model')
    field_id = fields.Many2one('ir.model.fields', domain="[('model_id','=',model_id)]", required=True, string='Aggregate Field')
    method = fields.Selection([('sum','Sum'), ('min','Min'), ('max','Max'), ('avg','Average')], default='sum', required=True)
    value = fields.Float(compute= '_compute_value')
    count = fields.Integer(compute= '_compute_value')
    value_char = fields.Char(compute= '_compute_value', string="Value")
    digits = fields.Integer(default=2)
    currency_id = fields.Many2one('res.currency')
    sequence = fields.Integer()
    
    date_range_field_id = fields.Many2one('ir.model.fields')
    date_range_type = fields.Selection(selection=DATE_RANGE_TYPES)
    date_domain = fields.Char(compute='_compute_date_domain_line')

    

    @api.depends('date_range_field_id','date_range_type')
    def _compute_date_domain_line(self):
        for r in self:
            compute_date_domain(r)
    

    # @api.onchange('model_id')
    # def _onchange_model_id(self):
    #     self.field_id = False
        

    @api.onchange('field_id')
    def _onchange_currency_id(self):
        if self.model_id and self.field_id:
            aggregate_field = self.env[self.model_id.model]._fields[self.field_id.name]
            if aggregate_field.type == 'monetary':
                self.currency_id = self.env.user.company_id.currency_id

    @api.depends('model_id', 'field_id', 'currency_id', 'method','domain', 'summary_report_config_id.domain', 'date_domain','summary_report_config_id.date_domain')
    def _compute_value(self):
        for r in self:
            sub_domain = safe_eval(r.domain or '[]')
            sub_date_domain = safe_eval(r.date_domain or '[]')
            if r.model_id == r.summary_report_config_id.model_id:
                parent_domain = safe_eval(r.summary_report_config_id.domain or '[]')
                parent_date_domain = safe_eval(r.summary_report_config_id.date_domain or '[]')
                domain = parent_domain + parent_date_domain + sub_domain + sub_date_domain
            else:
                domain = sub_domain + sub_date_domain

            if r.field_id.name in self.env[r.model_id.model]._fields:
                res_fields = ['{fn}:{method}({fn})'.format(fn=r.field_id.name, method=r.method)]
                read_group_datas = self.env[r.model_id.model].read_group(domain, res_fields,[])
                read_group_data_0 = read_group_datas[0]
                if r.field_id.name in read_group_data_0:
                    r.value = read_group_data_0[r.field_id.name]
                    r.count = read_group_data_0['__count']
                    r.value_char = formatLang(self.env, r.value, digits=r.digits, currency_obj=r.currency_id)
    


class SummaryReportConfig(models.Model):
    _name = 'summary.report.config'

    name = fields.Char(translate=True)
    active = fields.Boolean(default=True)
    model_id = fields.Many2one('ir.model', required=True)
    model_name = fields.Char(related='model_id.model')
    domain = fields.Char()
    priority = fields.Integer()
    icon = fields.Char()
    bg_option = fields.Selection([('color','Color'),('image','Image')])
    bg_color = fields.Char()
    bg_image = fields.Binary()
    col_size = fields.Integer(help='value from 1 to 12')
    max_height = fields.Float()
    line_ids = fields.One2many('summary.report.config.line', 'summary_report_config_id', copy=True)
    template_id = fields.Many2one('ir.ui.view')
    table_html = fields.Html(compute='_compute_html_table')
    
    date_range_field_id = fields.Many2one('ir.model.fields')
    date_range_type = fields.Selection(selection=DATE_RANGE_TYPES)
    date_domain = fields.Char(compute='_compute_date_domain')

    user_ids = fields.Many2many(
        'res.users', 'summary_report_config_rel', 'summary_report_config_id', 'user_id',
        )
    # @api.onchange('model_id')
    # def _onchange_model_id(self):
    #     self.domain = False
    #     self.date_domain = False


    @api.depends('date_range_field_id','date_range_type')
    def _compute_date_domain(self):
        for r in self:
            compute_date_domain(r)
       
    @api.depends('template_id')
    def _compute_html_table(self):
        for r in self:
            summary_report_config = r
            if summary_report_config.template_id:
                template_id = summary_report_config.template_id
            else:
                template_id = self.env.ref('sale_order_summary.main_table_data')
            table_html = template_id.render({
                'config':summary_report_config
            })
            summary_report_config.table_html = table_html


def compute_date_domain(r):
    date_range_type = r.date_range_type
    fn = r.date_range_field_id.name
    domain = []
    if fn and date_range_type:
        start = None
        end = None
        today = fields.Date.today()
        if date_range_type == 'late':
            domain = [(fn, '<', today.strftime('%Y-%m-%d'))]
        elif date_range_type == 'today':
            # domain = [(fn, '=', today.strftime('%Y-%m-%d'))]
            start = today
            end = today + relativedelta(days=1)

        elif date_range_type == 'yesterday':
            start = today + relativedelta(days=-1)
            end =  today
        elif date_range_type == 'this_week':
            start = date_utils.start_of(today, 'week')
            end = start + relativedelta(days=7)
        elif date_range_type == 'last_week':
            start_this_week = date_utils.start_of(today, 'week')
            start = start_this_week  - relativedelta(days=7)
            end = start_this_week
        elif date_range_type == 'this_month':
            start = date_utils.start_of(today, 'month')
            end  = start + relativedelta(months=1)
        elif date_range_type == 'last_month':
            start_this_month = date_utils.start_of(today, 'month')
            start = start_this_month - relativedelta(months=1)
            end = start_this_month
        elif date_range_type == 'this_year':
            start = date_utils.start_of(today, 'year')
            end = start + relativedelta(years=1)
        elif date_range_type == 'last_year':
            start_this_year = date_utils.start_of(today, 'year')
            start = start_this_year - relativedelta(years=1)
            end = start_this_year
        if not domain  :
            if start:
                domain = [
                    (fn, '>=', start.strftime('%Y-%m-%d')),
                ]
            if end:
                domain.append((fn, '<', end.strftime('%Y-%m-%d')))
    r.date_domain = domain 
