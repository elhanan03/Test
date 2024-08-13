# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SalaryStructureAssignment(Document):
	pass


@frappe.whitelist()
def get_monthly_salary_structure(salary_structure):
		sal_st = frappe.db.sql(f""" SELECT * FROM `tabSalary Detail` WHERE parent='{salary_structure}'""", as_dict=True)
		return sal_st	


@frappe.whitelist()
def assign_salary_structure_bulk(salary_structure):
    active_employees = frappe.get_all("Employee", filters={"status": "Active"}, pluck="name")
    for employee in active_employees:
        assign_salary_structure_to_employee(salary_structure, employee)

def assign_salary_structure_to_employee(salary_structure, employee):
    # Fetch monthly salary structure details
    earnings, deductions = get_monthly_salary_structure_details(salary_structure)
    
    # Create Salary Structure Assignment
    salary_structure_assignment = frappe.new_doc("Salary Structure Assignment")
    salary_structure_assignment.employee = employee
    salary_structure_assignment.salary_structure = salary_structure
    
    # Populate earnings
    for earning in earnings:
        salary_structure_assignment.append('earning', {
            'name1': earning.name1,
            'type': earning.type,
            'amount': earning.amount,
            'formula': earning.formula,
            'is_tax_applicable': earning.is_tax_applicable,
            'do_not_include_in_total': earning.do_not_include_in_total,
            'earning_category': earning.earning_category,
            'allowance_type': earning.allowance_type,
            'deduction_category': earning.deduction_category,
        })
    
    # Populate deductions
    for deduction in deductions:
        salary_structure_assignment.append('deduction', {
            'name1': deduction.name1,
            'type': deduction.type,
            'amount': deduction.amount,
            'formula': deduction.formula,
            'is_tax_applicable': deduction.is_tax_applicable,
            'do_not_include_in_total': deduction.do_not_include_in_total,
            'earning_category': deduction.earning_category,
            'allowance_type': deduction.allowance_type,
            'deduction_category': deduction.deduction_category,
        })
    
    salary_structure_assignment.save()
    salary_structure_assignment.submit()

def get_monthly_salary_structure_details(salary_structure):
    earnings = frappe.get_all("Salary Detail", filters={
        "parent": salary_structure, "parentfield": "earnings"
    }, fields=["name1", "type", "amount", "formula", "is_tax_applicable", "do_not_include_in_total", "earning_category", "allowance_type", "deduction_category"])
    
    deductions = frappe.get_all("Salary Detail", filters={
        "parent": salary_structure, "parentfield": "deductions"
    }, fields=["name1", "type", "amount", "formula", "is_tax_applicable", "do_not_include_in_total", "earning_category", "allowance_type", "deduction_category"])
    
    return earnings, deductions