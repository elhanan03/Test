# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LeaveAllocation(Document):
    def before_insert(self):
            doc = frappe.db.sql(
                f""" SELECT MAX(refno) as last_number FROM `tabLeave Allocation` """, as_dict=1)
            if not doc[0].last_number:
                self.refno = 1
            else:
                self.refno = doc[0].last_number + 1


@frappe.whitelist()
def get_data(holiday_list, total_leave_days, from_date, to_date):
    dct = {}
    try:
        doc = frappe.db.sql(f""" SELECT * FROM `tabHoliday` WHERE holiday_date>='{from_date}' and holiday_date<='{to_date}' and parent= '{holiday_list}' """,as_dict=True)
        actual_leave_days = int(total_leave_days) - len(doc)
        
        dct = {
            'actual_leave_days': actual_leave_days,
        }
    except:

        dct = {
            'actual_leave_days': '',
        }

    return dct
