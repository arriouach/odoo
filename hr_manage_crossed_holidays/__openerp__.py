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
{
    'name': "Manage crossed holidays",
    'summary': """
        Manage crossed holidays.
        """,

    'description': """
Manage crossed holidays
===========================

This extension allow to manage the crossed holidays (weekend, national holidays, religious holidays, ...) with employee leave.

Features:
---------
    * Manage the official holidays (weekend, national holidays, religious holidays, ...).
    * Calculate the number of days for leave without crossed holidays.
    * Saving the crossed holidays within leave request.

Translation:
------------
    * Arabic.
    * English.

Installation:
-------------
    * After Installed the extension you can access to the official holidays by going to menu : Human Resources/Configuration/Holidays.
    * Give user that has the authorization to access the official holidays by active the "Holidays Access" group.
    """,

    'author': "Mohamed ARRIOUACH",
    'website': "",
    'price': 9.00,
    'currency': 'USD',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_holidays'],

    # always loaded
    'data': [
        'security/hr_manage_crossed_holidays_security.xml',
        'security/ir.model.access.csv',
        'hr_manage_crossed_holidays_view.xml',
        'hr_holidays_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],
    'license': 'AGPL-3',
    'auto_install': False,
    'installable': True,
    'images' : ['images/holidays_list_view_screenshot.png', 'images/holidays_form_view_weekend.png',
                 'images/holidays_form_view.png','images/holidays_list_view.png',
                 'images/leave_request.png', 'images/menu_holidays.png',
                 'images/set_holidays_group_access.png'],
}
