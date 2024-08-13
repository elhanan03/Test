# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_years, cint, getdate


class Employee(Document):
    def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(refno) as last_number FROM `tabEmployee` """, as_dict=1)
        if not doc[0].last_number:
            self.refno = 1
        else:
            self.refno = doc[0].last_number + 1


@frappe.whitelist()
def get_phone_number(doctype, docname):
    doc = frappe.get_doc(doctype, docname)
    return doc.phone


@frappe.whitelist()
def get_qualification(get_from_employee_onboarding):
	qualification = frappe.db.sql(
            f""" SELECT * FROM `tabOnboarding Qualification` WHERE parent = '{get_from_employee_onboarding}'""", as_dict=True)
	return qualification


@frappe.whitelist()
def get_basic_salary(salary_scale_name, level, scale):
    doc = frappe.db.sql(
        f"""SELECT * FROM `tabSalary Structure` WHERE name1= '{salary_scale_name}' and level= '{level}' and scale='{scale}' """, as_dict=True)
    if doc:
        return doc[0].amount
    else:
        return 0



@frappe.whitelist()
def get_retirement_date(birth_date=None):
    if birth_date:
        try:
            retirement_age = 65
            dt = add_years(getdate(birth_date), retirement_age)

            # Check if the calculated retirement date is later than the employee's 65th birthday
            if dt > add_years(getdate(birth_date), 65):
                dt = add_years(getdate(birth_date), 65)

            return dt.strftime("%Y-%m-%d")
        except ValueError:
            # invalid date
            return
