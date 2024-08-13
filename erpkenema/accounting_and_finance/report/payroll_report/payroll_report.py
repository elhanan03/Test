# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []

	if filters.get("payroll_sheet"):
		colm_list = [
			{
				'fieldname': 'full_name',
				'label': "Full Name",
				'fieldtype': 'Data',
				'width': '150'
			},
			{
				'fieldname': 'total_pay',
				'label': "Total Pay",
				'fieldtype': 'Float',
				'width': '150'
			},
			{
				'fieldname': 'account_number',
				'label': "Account Number",
				'fieldtype': 'Data',
				'width': '150'
			},
			
		]
		columns = get_columns(colm_list)
		salary_slip_data = get_salary_slip(filters)

		if not salary_slip_data:
			frappe.msgprint('No records found')
			return columns, salary_slip_data

		for d in salary_slip_data:
			row = frappe._dict({
				'full_name': d.full_name,
				'total_pay': d.total_pay,
				'account_number': d.account_number
			})
			data.append(row)

	else:
		
		colm_list = [
			{
				'fieldname': 'full_name',
				'label': "Full Name",
				'fieldtype': 'Data',
				'width': '150'
			},
		]

		if filters.get("salary_structure"):
			listt = frappe.db.sql(f"""select name1, type from `tabSalary Detail` where parent='{filters["salary_structure"]}'""",as_list=True)
		else:
			listt = []

		
		# earning component
		for element in listt:
			if element[1]=='Earning':
				colm_list.append(
					{
					'fieldname': element[0].lower().replace(" ", "_"),
					'label': element[0],
					'fieldtype': 'Float',
					'width': '150',
				})

		
		colm_list.extend(
			[
			{
				'fieldname': 'taxable_income',
				'label': "Taxable Income",
				'fieldtype': 'Float',
				'width': '150'
			},
			{
				'fieldname': 'total_earning',
				'label': "Total",
				'fieldtype': 'Float',
				'width': '150'
			},
			]
		)

		# deduction component
		for element in listt:
			if element[1]=='Deduction':
				colm_list.append(
					{
					'fieldname': element[0].lower().replace(" ", "_"),
					'label': element[0],
					'fieldtype': 'Float',
					'width': '150',
				})

		colm_list.extend(
			[
			{
				'fieldname': 'total_deduction',
				'label': "Total Deduction",
				'fieldtype': 'Float',
				'width': '150'
			},
			{
				'fieldname': 'net_pay',
				'label': "Net Pay",
				'fieldtype': 'Float',
				'width': '150'
			},
			{
				'fieldname': 'return_income_tax',
				'label': "Ret.Income Tax",
				'fieldtype': 'Float',
				'width': '150'
			},
			{
				'fieldname': 'total_pay',
				'label': "Total Pay",
				'fieldtype': 'Float',
				'width': '150'
			},
			]
		)

		columns = get_columns(colm_list)
		salary_slip_data = get_salary_slip(filters)

		if not salary_slip_data:
			frappe.msgprint('No records found')
			return columns, salary_slip_data
		
		for d in salary_slip_data:
			dct={
				'full_name': d.full_name,
				'total_earning': d.total_earning,
				'total_deduction': d.total_deduction,
				'net_pay': d.net_pay,
				'return_income_tax': d.return_income_tax,
				'total_pay': d.total_pay,
			}
			doc = frappe.db.sql(f"""select name1, amount from `tabSelected Salary Detail` where parent='{d.name}'""",as_list=True)
			for element in doc:
				key=element[0].lower().replace(" ", "_")
				value=element[1]
				dct[key]=value

			row = frappe._dict(dct)

			data.append(row)


	return columns, data


def get_columns(colm_list):
	return colm_list


def get_conditions(filters):
	conditions = ""

	if filters.get("division"):

		if filters['division']=='Branch':
			conditions += "division = '%s'" % filters["division"]
			if filters.get('branch'):
				conditions += "and branch = '%s'" % filters["branch"]

		if filters['division']=='Head Office':
			conditions += "division = '%s'" % filters["division"]
	
	if filters.get("salary_structure"):
		conditions += "and sal_str = '%s'" % filters["salary_structure"]
		
	return conditions


def get_salary_slip(filters):
	conditions = get_conditions(filters)
	if filters.get("division"):
		if filters['division']=='Branch':

			return frappe.db.sql(
				f"""SELECT *
				FROM `tabSalary Slip`
				WHERE %s"""
				% conditions,
				as_dict=1,
			)	
		elif filters['division']=='Head Office':
			return frappe.db.sql(
				f"""SELECT *
				FROM `tabSalary Slip`
				WHERE %s"""
				% conditions,
				as_dict=1,
			)
	else:
		return frappe.db.sql(
			f"""SELECT *
			FROM `tabSalary Slip`""",
			as_dict=1,
		)