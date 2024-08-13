# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, rounded, getdate

class SalarySlip(Document):
    def before_save(self):
        total_earning, total_deduction, net_pay, total_pay, taxable_income = 0.0, 0.0, 0.0, 0.0, 0.0
        for component in self.earning:
            if not component.do_not_include_in_total:
                total_earning += flt(component.amount)
            if component.is_tax_applicable:
                taxable_income += flt(component.amount)
        
        for component in self.deduction:
            if not component.do_not_include_in_total:
                total_deduction += flt(component.amount)

        self.total_earning = rounded(total_earning, precision=2)
        self.total_deduction = rounded(total_deduction, precision=2)
        self.taxable_income = rounded(taxable_income, precision=2)
        self.net_pay = rounded(total_earning - total_deduction, precision=2)
        self.return_income_tax = rounded(self.return_income_tax, precision=2)
        self.total_pay = rounded(flt(self.return_income_tax) + self.net_pay, precision=2)

    def before_submit(self):
        doc = frappe.get_doc('Loan management', self.loan)
        if doc:
            if doc.paid_amount < doc.total_requested:
                doc.paid_amount += doc.monthly_payment
                doc.save()
            else:
                frappe.msgprint('Loan fully paid!')

@frappe.whitelist()
def get_salary_structure(salary_structure):
    sal_st = frappe.db.sql(f"""SELECT * FROM `tabSSA_Child_Table` WHERE parent='{salary_structure}'""", as_dict=True)
    return sal_st

@frappe.whitelist()
def get_component_amount(formula, basic_salary, amount):
    if formula:
        formula = formula.strip().replace("\n", " ")
        basic_salary = float(basic_salary)
        amount = eval(formula, {"base": basic_salary})
    return amount

@frappe.whitelist()
def get_allowance_amount(allowance_type, role):
    doc = frappe.get_doc(allowance_type, role)
    allowance_amount = doc.amount
    return allowance_amount

@frappe.whitelist()
def get_income_tax_amount(taxable_income, basic_salary):
    doc2 = frappe.db.sql(f"""SELECT * FROM `tabIncome Tax` WHERE frombs < {basic_salary} and tobs > {basic_salary} """, as_dict=True)
    income_tax_amount = flt(taxable_income) * flt(doc2[0].rate) - flt(doc2[0].deduction)
    return income_tax_amount

# @frappe.whitelist()
# def get_pp_amount(net_income):
#     doc2 = frappe.db.sql(f"""SELECT * FROM `tabPP Rate` WHERE frompp <= {net_income} and topp >= {net_income} """, as_dict=True)
#     pp_amount = flt(net_income) * flt(doc2[0].rate)
#     return pp_amount

@frappe.whitelist()
def get_pp_amount(net_income):
    # Query to get the rate based on the provided net_income
    doc2 = frappe.db.sql(f"""
        SELECT rate 
        FROM `tabPP Rate` 
        WHERE frompp <= {net_income} AND topp >= {net_income}
    """, as_dict=True)
    
    # Check if doc2 is not empty
    if doc2:
        pp_amount = flt(net_income) * flt(doc2[0].rate)
    else:
        pp_amount = 0  # Default value if no matching records are found
    
    return pp_amount

@frappe.whitelist()
def get_overtime_amount(overtime):
    doc2 = frappe.db.sql(f"""SELECT * FROM `tabOver Time` WHERE name = '{overtime}'""", as_dict=True)
    overtime_amount = doc2[0].total_payment
    return overtime_amount

@frappe.whitelist()
def get_loan_amount(loan):
    doc = frappe.db.sql(f"""SELECT * FROM `tabLoan management` WHERE name = '{loan}'""", as_dict=True)
    loan_amount = 0
    if doc[0].paid_amount < doc[0].total_requested:
        loan_amount = doc[0].monthly_payment
    return loan_amount

@frappe.whitelist()
def get_over_time(employee=None):
    filters = {}
    if employee:
        filters["employee"] = employee

    over_time_records = frappe.get_list("Over Time", filters=filters, fields=["name", "employee"])
    return over_time_records

@frappe.whitelist()
def get_absent_days(employee, start_date, end_date):
    start_date = frappe.utils.getdate(start_date)
    end_date = frappe.utils.getdate(end_date)
    
    # Fetch attendance records for the employee within the date range where status is Absent
    attendance_records = frappe.db.get_list("Attendance", 
                                            filters={
                                                'employee': employee,
                                                'date': ['between', [start_date, end_date]],
                                                'status': 'Absent'
                                            },
                                            fields=['status'])

    # Count the number of records where status is 'Absent'
    absent_days_count = len(attendance_records)

    return {
        'absent_days': absent_days_count
    }
