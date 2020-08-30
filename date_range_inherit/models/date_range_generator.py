# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule
class DateRangeGenerator(models.TransientModel):
    _inherit = 'date.range.generator'

    name_suffix = fields.Char('Name Suffix')
    start_of_number = fields.Integer('Name Start')

    @api.multi
    def _compute_date_ranges(self):
        self.ensure_one()
        vals = rrule(freq=self.unit_of_time, interval=self.duration_count,
                     dtstart=self.date_start,
                     count=self.count+1)
        vals = list(vals)
        date_ranges = []
        count_digits = len(str(self.count))
        for idx, dt_start in enumerate(vals[:-1]):
            date_start = dt_start.date()
            # always remove 1 day for the date_end since range limits are
            # inclusive
            date_end = vals[idx+1].date() - relativedelta(days=1)
            name = '%s%0*d%s' % (
                    self.name_prefix, count_digits, idx + 1 + self.start_of_number, self.name_suffix)
            date_ranges.append({
                'name': name,
                'date_start': date_start,
                'date_end': date_end,
                'type_id': self.type_id.id,
                'company_id': self.company_id.id})
        return date_ranges

