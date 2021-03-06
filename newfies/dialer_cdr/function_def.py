#
# Newfies-Dialer License
# http://www.newfies-dialer.org
#
# This Source Code Form is subject to the terms of the Mozilla Public 
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2012 Star2Billing S.L.
# 
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#

from dialer_cdr.models import *
from datetime import *
from random import *
from dialer_campaign.function_def import validate_days
from dialer_cdr.models import VOIPCALL_DISPOSITION


def pass_gen():
    """Unique password generator"""
    char_length = 2
    digit_length = 6
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digit = "1234567890"
    pass_str_char = ''.join([choice(chars) for i in range(char_length)])
    pass_str_digit = ''.join([choice(digit) for i in range(digit_length)])
    return pass_str_char + pass_str_digit


def variable_value(request, field_name):
    """Variables are checked with request & return field value"""
    if request.method == 'GET':
        if field_name in request.GET:
            field_name = request.GET[field_name]
        else:
            field_name = ''

    if request.method == 'POST':
        if field_name in request.POST:
            field_name = request.POST[field_name]
        else:
            field_name = ''

    return field_name


def is_number(s):
    """Check digit is int or float"""
    try:
        if float(s):
            return True
        elif int(s):
            return True
        else:
            return False
    except ValueError:
        return False


def is_int_no(no):
    """Check digit is int"""
    if int(no):
        return True
    else:
        return False


def is_float_no(no):
    """Check Float Value"""
    if float(no):
        return True
    else:
        return False


def rate_range():
    """Filter range symbol"""
    LIST = (('', 'All'),
            ('gte', '>='),
            ('gt', '>'),
            ('eq', '='),
            ('lt', '<'),
            ('lte', '<='))
    return LIST


def voipcall_record_common_fun(request):
    """Return Form with Initial data or Array (kwargs) for Voipcall_Report
    Changelist_view"""
    start_date = ''
    end_date = ''
    if request.POST.get('from_date'):
        from_date = request.POST.get('from_date')
        start_date = datetime(int(from_date[0:4]), int(from_date[5:7]),
                              int(from_date[8:10]), 0, 0, 0, 0)
    if request.POST.get('to_date'):
        to_date = request.POST.get('to_date')
        end_date = datetime(int(to_date[0:4]), int(to_date[5:7]),
                            int(to_date[8:10]), 23, 59, 59, 999999)

    # Assign form field value to local variable
    disposition = variable_value(request, 'status')

    # Patch code for persist search
    if request.method != 'POST':

        if  request.session.get('from_date'):
            from_date = request.session['from_date']
            start_date = datetime(int(from_date[0:4]), int(from_date[5:7]),
                                  int(from_date[8:10]), 0, 0, 0, 0)

        if  request.session.get('to_date'):
            to_date = request.session['to_date']
            end_date = datetime(int(to_date[0:4]), int(to_date[5:7]),
                                int(to_date[8:10]), 23, 59, 59, 999999)

        if request.session.get('status'):
            disposition = request.session['status']

    kwargs = {}
    if start_date and end_date:
        kwargs['starting_date__range'] = (start_date, end_date)
    if start_date and end_date == '':
        kwargs['starting_date__gte'] = start_date
    if start_date == '' and end_date:
        kwargs['starting_date__lte'] = end_date
    
    if disposition:
        if disposition != 'all':
            kwargs['disposition__exact'] = disposition

    if len(kwargs) == 0:
        tday = datetime.today()
        kwargs['starting_date__gte'] = datetime(tday.year,
                                                tday.month,
                                                tday.day, 0, 0, 0, 0)
    return kwargs


def return_query_string(query_string, para):
    if query_string:
        query_string += '&' + para
    else:
        query_string = para
    return query_string


def voipcall_search_admin_form_fun(request):
    """Return query string for Voipcall_Report Changelist_view"""
    start_date = ''
    end_date = ''
    if request.POST.get('from_date'):
        start_date = request.POST.get('from_date')

    if request.POST.get('to_date'):
        end_date = request.POST.get('to_date')

    # Assign form field value to local variable
    disposition = variable_value(request, 'status')
    query_string = ''

    if start_date and end_date:
        date_string = 'starting_date__gte=' + start_date + '&starting_date__lte=' + end_date + '+23%3A59%3A59'
        query_string = return_query_string(query_string, date_string)

    if start_date and end_date == '':
        date_string = 'starting_date__gte=' + start_date
        query_string = return_query_string(query_string, date_string)

    if start_date == '' and end_date:
        date_string = 'starting_date__lte=' + end_date
        query_string = return_query_string(query_string, date_string)

    if disposition:
        if disposition != 'all':
            disposition_string = 'disposition__exact=' + disposition
            query_string = return_query_string(query_string, disposition_string)

    return query_string


def get_disposition_id(name):
    """To get id from voip_call_disposition_list"""
    for i in VOIPCALL_DISPOSITION:
        if i[1] == name:
            return i[0]


def get_disposition_name(id):
    """To get name from voip_call_disposition_list"""
    for i in VOIPCALL_DISPOSITION:
        if i[0] == id:
            return i[1]