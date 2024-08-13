# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, rounded, flt
import math
import datetime



class EmployeeLeaveControl(Document):
    def before_insert(self):
            doc = frappe.db.sql(
                f""" SELECT MAX(refno) as last_number FROM `tabEmployee Leave Control` """, as_dict=1)
            if not doc[0].last_number:
                self.refno = 1
            else:
                self.refno = doc[0].last_number + 1

    def before_save(self):
        if self.leave_period > 30:
            frappe.throw("Leave more than 30 days not allowed")

        if self.leave_period > self.leave_balance:
            frappe.throw("Leave period can't be greater than Leave balance")
        else:
            doc = frappe.new_doc("Leave History")
            doc.employee = self.employee
            doc.employee_id = self.employee_id
            doc.taken_leaves = self.leave_period
            doc.date = self.current_date
            doc.left_leave = self.leave_balance - self.leave_period
            doc.insert()


@frappe.whitelist()
def get_data(date_of_joining, current_date, employee_id):
    dct = {}
    try:

        employee_doc = frappe.db.sql(f"""SELECT * FROM `tabEmployee` WHERE name='{employee_id}'""",as_dict=True)
        role = employee_doc[0].role
        
        role_list = frappe.db.sql(f""" SELECT role FROM `tabLeave not exceed 30 days`""", as_list=True)
    
        exist=False
        for valid_role in role_list:
            if role==valid_role[0]:
                exist=True
                break

        year_served = math.ceil(date_diff(current_date, date_of_joining)/365)
        total_leave_days = 0
        p=17
        for year in range(1, year_served+1):
            if year==1 or year==2:
                total_leave_days+=p
            else:
                if exist and (year > 28):
                    p=30
                    total_leave_days=60
                else:
                    if year%2!=0:
                        p+=1
                    total_leave_days+=1

        last_doc = frappe.get_all("Leave History", filters={"employee_id": employee_id}, limit_page_length=1, order_by="modified desc")
        leave_balance = 0

        if len(last_doc):
            last_doc = last_doc[0]
            docc = frappe.db.sql(f"""SELECT * FROM `tabLeave History` WHERE name='{last_doc.name}'""",as_dict=True)
            
            recent_year_date = str(docc[0].date)
            current_year_date = str(current_date)

            recent_year_on_lh = datetime.datetime.strptime(recent_year_date, "%Y-%m-%d").year
            current_year = datetime.datetime.strptime(current_year_date, "%Y-%m-%d").year

            if recent_year_on_lh == current_year:
                leave_balance = docc[0].left_leave
            else:
                if abs(current_year - recent_year_on_lh)==1:
                    if (exist==False) or (year_served < 29): # normal employee
                        if year_served%2!=0:	
                            if docc[0].left_leave > p-1:
                                leave_balance = p + p-1
                            else:
                                leave_balance = p + docc[0].left_leave
                        else:
                            if docc[0].left_leave  > p:
                                leave_balance = p + p
                            else:
                                leave_balance = p + docc[0].left_leave

                    elif (exist==True) and (year_served > 28): # head employee
                        if docc[0].left_leave > p:
                            leave_balance = p + p
                        else:
                            leave_balance = p + docc[0].left_leave 
            
                elif abs(current_year - recent_year_on_lh) > 1:
                    if (exist==False) or (year_served < 29):
                        if year_served%2!=0:
                            leave_balance = p + (p-1) # 2p-1
                        else:
                            leave_balance = p + p # 2p		
                    elif (exist==True) and (year_served > 28):
                        leave_balance = p + p # 60
        else:
            leave_balance = total_leave_days

        used_leave_days = total_leave_days - leave_balance

        dct = {
            'year_served': year_served,
            'total_leave_days': total_leave_days,
            'used_leave_days': used_leave_days,
            'leave_balance': leave_balance,
            'role':employee_doc[0].role,
        }
    except:

        dct = {
            'year_served': '',
            'total_leave_days': '',
            'used_leave_days': '',
            'leave_balance': '',
            'role': '',
        }

    return dct
