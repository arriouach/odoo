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

import datetime
from openerp.osv import fields, osv
from openerp.tools.translate import _
 
  
class hr_holidays(osv.osv):
    _name = "hr.holidays"
    _inherit = "hr.holidays"
    
    _columns = {
        'standard_holidays_ids' : fields.one2many('hr_manage_crossed_holidays.hr_holidays', 'holidays_id', string='Standard Holidays'),
    }
    
    def onchange_date_to(self, cr, uid, ids, date_to, date_from, context=None):
        result = super(hr_holidays, self).onchange_date_to(cr, uid, ids, date_to, date_from)
        
        # Get the number_of_days_temp before change.
        nbr_days = result['value']['number_of_days_temp']

        res = self._cal_standard_holidays(cr, uid, ids , date_to, date_from, context)
        if res != False:
            result['value']['number_of_days_temp'] = nbr_days - res['my_holidays']
            result['value']['standard_holidays_ids'] = res['ids']
        
        return result  
    
    def onchange_date_from(self, cr, uid, ids, date_to, date_from, context=None):
        result = super(hr_holidays, self).onchange_date_from(cr, uid, ids, date_to, date_from)
        
        # Get the number_of_days_temp before change.
        nbr_days = result['value']['number_of_days_temp']

        # Elimination the crossed holidays from number_of_days_temp 
        res = self._cal_standard_holidays(cr, uid, ids , date_to, date_from, context)
        if res != False:
            result['value']['number_of_days_temp'] = nbr_days - res['my_holidays']
            result['value']['standard_holidays_ids'] = res['ids']
        return result

    def _cal_standard_holidays(self, cr, uid, ids , date_to, date_from, context=None): 
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        if date_from == False or date_to == False:
            return False
        
        #-------------------------------------------------------------------------
        # Get the company record for the current employee.  
        #-------------------------------------------------------------------------
        empl_id = False
        if len(ids) == 0:
            id = self._employee_get(cr, uid, context)
            empl_id = self.pool.get('hr.employee').browse(cr, uid, id)
        else:
            empl_id = self.pool.get('hr.holidays').browse(cr, uid, ids)[0].employee_id
        
        company_id = empl_id.resource_id.company_id.id
        #-------------------------------------------------------------------------
  
        from_dt = datetime.datetime.strptime(date_from, DATETIME_FORMAT)
        to_dt = datetime.datetime.strptime(date_to, DATETIME_FORMAT)
        
        # Get diff datetime days.
        dif = to_dt - from_dt
       
        hol_obj = self.pool.get('hr.manage.crossed.holidays')
        hol_ids = hol_obj.search(cr, uid, [('company_id', '=', company_id)])  # Filter holidays by employee company.

        ids = []
        my_holidays = 0;
        
        # Get days total of weekend those are exist between date_from and date_to.
        for i in range(dif.days):
            dt = from_dt + datetime.timedelta(days=i)
            h_ids = hol_obj.search(cr, uid, ['&', '&', ('w_day', '=', dt.weekday()), ('weekend', '=', True),
                                           ('company_id', '=', company_id)])
            if len(h_ids) != 0:
                tmp_obj = hol_obj.browse(cr, uid, h_ids[0])
                ids.append({'standard_holidays_id':h_ids[0],
                                        'weekend':tmp_obj.weekend,
                                        'nbr_days': tmp_obj.nbr_days * (tmp_obj.paid and -1 or 0),
                                        'paid':tmp_obj.paid,
                                        'w_day':tmp_obj.w_day,
                                        'date_from':dt, })
                if tmp_obj.paid:
                    my_holidays += 1
        
        # Get crossed holidays those are exist between date_from and date_to.
        hol_recs = hol_obj.browse(cr, uid, hol_ids)
        for rec in hol_recs:
            if rec.weekend == False:
                cnt_weekend_cross = 0
                for nbr in range(rec.nbr_days):
                    now = datetime.datetime.now()
                    date_hol = datetime.datetime(now.year, rec.month, rec.day) + datetime.timedelta(days=nbr)
                    if from_dt.date() <= date_hol.date() and to_dt.date() >= date_hol.date():
                        wdays = date_hol.weekday()
                        ho_ids = hol_obj.search(cr, uid, ['&', '&', ('w_day', '=', wdays), ('weekend', '=', True), ('company_id', '=', company_id)])

                        if len(ho_ids) == 0:
                            if rec.paid:
                                my_holidays += 1                                
                        else:
                            if rec.paid:
                                cnt_weekend_cross += 1
                        if nbr + 1 == rec.nbr_days:
                            ids.append({'standard_holidays_id':rec.id,
                                        'weekend':rec.weekend,
                                        'nbr_days':(rec.nbr_days * (rec.paid and -1 or 0)) + cnt_weekend_cross,
                                        'paid':rec.paid,
                                        'w_day':rec.w_day,
                                        'date_from':rec.date_from_gen,
                                        'cross_weekend':cnt_weekend_cross > 0, })
               
        return {'my_holidays':my_holidays, 'ids':ids}   
