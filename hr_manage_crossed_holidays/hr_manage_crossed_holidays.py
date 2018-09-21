# -*- coding: utf-8 -*-
######################################################################################
#
#    Manage crossed holidays
#    Copyright (C) 2018 Mohamed ARRIOUACH.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#    
######################################################################################

from openerp import models, fields, api
import datetime
from openerp.tools.translate import _

from openerp.osv import  osv

_days_week_names = [(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'),
                    (5, 'Saturday'), (6, 'Sunday')]

_month_names = [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'),
                 (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')]


class hr_manage_crossed_holidays(models.Model):
    _name = 'hr.manage.crossed.holidays'
    _inherit = ['mail.thread']
        
    name = fields.Char('Name', required=True)
    weekend = fields.Boolean('Weekend')
#    color_name = fields.Selection([('red', 'Red'),('blue','Blue'), ('lightgreen', 'Light Green'), ('lightblue','Light Blue'), ('lightyellow', 'Light Yellow'), ('magenta', 'Magenta'),('lightcyan', 'Light Cyan'),('black', 'Black'),('lightpink', 'Light Pink'),('brown', 'Brown'),('violet', 'Violet'),('lightcoral', 'Light Coral'),('lightsalmon', 'Light Salmon'),('lavender', 'Lavender'),('wheat', 'Wheat'),('ivory', 'Ivory')],'Color in Report', required=True, help='This color will be used in the leaves summary located in Reporting\Leaves by Department.'),
    day = fields.Integer('Day', default=lambda self: 1,)
    month = fields.Selection(_month_names, string='Month')
    nbr_days = fields.Integer('Number of days', default=lambda self: 1,)
    active = fields.Boolean('Active', default=lambda self: True,)
    paid = fields.Boolean('Paid', default=lambda self: True,)
    w_day = fields.Selection(_days_week_names, string='Week-day',)
    date_from_gen = fields.Date(compute='_generate_date_from', string='Date from')
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.user.company_id.id)
    # date_from = fields.Function(_compute_number_of_days, string='Number of Days', store=True),

    @api.multi
    def _generate_date_from(self):
        for rec in self:
            val = False
            if not rec.weekend:
                now = datetime.datetime.now()
                val = datetime.datetime(now.year, rec.month, rec.day)

            rec.date_from_gen = val   
    
    @api.model
    def create(self, values):
        
        if not values['weekend']:
            now = datetime.datetime.now()
            str_date_from = "{}-{}-{}".format(str(now.year), values['month'], values['day'])
            res = self._validate_date(str_date_from, '%Y-%m-%d')
            if not res:
                raise osv.except_osv(_("Warning!"), _("Date inserted is incorrect."))
            
            if  values['nbr_days'] == 0:
                raise osv.except_osv(_("Warning!"), _("Number day must be greater than 0."))
        else:
            values['paid'] = True
         
        return super(hr_manage_crossed_holidays, self).create(values)
    
    @api.one
    def write (self, values):
        obj = self.pool[self._name].browse(self.env.cr, self.env.uid, self.ids[0], self._context)
         
        if 'weekend' in values:
            _weekend = values['weekend']
            if _weekend:
                values['paid'] = True
        else:  _weekend = obj.weekend
           
        if 'nbr_days' in values:
            _nbr_days = values['nbr_days']
        else: _nbr_days = obj.nbr_days
            
        if not _weekend and _nbr_days == 0:
            raise osv.except_osv(_("Warning!"), _("\"Number of days\" must be greater than 0."))
        
        if 'day' in values or 'month' in values:
            if not _weekend:
                _day = False
                _month = False
                if 'month' in values:
                    _month = values['month']
                else:  _month = obj.month
                if  'day' in values:
                    _day = values['day']
                else: _day = obj.day                                          
                        
                now = datetime.datetime.now()
                str_date_from = "{}-{}-{}".format(str(now.year), _month, _day)
                res = self._validate_date(str_date_from, '%Y-%m-%d')
                if not res:
                    raise osv.except_osv(_("Warning!"), _("Date inserted is incorrect."))
                 
        return super(hr_manage_crossed_holidays, self).write(values)
    
    @api.onchange('weekend')
    def onchange_weekend(self):
        if self.weekend:
            self.month = False
            self.day = 1
            self.nbr_days = 1
        else: self.w_day = False  

    def _validate_date(self, date_text, pattern):
        try:            
            datetime.datetime.strptime(date_text, pattern)
        except ValueError:
            # raise ValueError("Date inserted is incorrect")
            return False
        return True

    
class hr_manage_crossed_holidays_hr_holidays(models.Model):
    _name = 'hr_manage_crossed_holidays.hr_holidays'
    _inherit = ['mail.thread']
    
    holidays_id = fields.Many2one('hr.holidays', string='Holidays', ondelete='cascade')
    standard_holidays_id = fields.Many2one('hr.manage.crossed.holidays', string='Holidays', ondelete='cascade')
    quant = fields.Integer('Quantity')

    weekend = fields.Boolean('Weekend')
    nbr_days = fields.Integer('Number of days', default=lambda self: 1,)
    paid = fields.Boolean('Paid', default=lambda self: True,)
    w_day = fields.Selection(_days_week_names, string='Week-day',)
    date_from = fields.Date(string='Date from')
    cross_weekend = fields.Boolean('Cross weekend')
    
    
