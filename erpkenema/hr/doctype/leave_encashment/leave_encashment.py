# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, rounded, flt
import math
import datetime

class LeaveEncashment(Document):
	def before_save(self):

		doc = frappe.new_doc("Leave History")
		doc.employee = self.employee
		doc.employee_id = self.employee
		doc.taken_leaves = self.encashment_days
		doc.date = self.date
		doc.left_leave = self.p
		doc.insert()



@frappe.whitelist()
def get_data(employee_id, date_of_joining, current_date):
	dct = {}
	try:
		employe_doc = frappe.db.sql(f"""SELECT * FROM `tabEmployee` WHERE name='{employee_id}'""",as_dict=True)

		last_doc = frappe.get_all("Leave History", filters={"employee_id": employee_id}, limit_page_length=1, order_by="modified desc")

		year_served = math.ceil(date_diff(current_date, date_of_joining)/365)
		encashment_days = 0
		p=17
		for year in range(1, year_served+1):
			if year==1 or year==2:
				pass
			else:
	   			if year%2!=0:
		   			p+=1

		if len(last_doc):
			last_doc = last_doc[0]
			docc = frappe.db.sql(f"""SELECT * FROM `tabLeave History` WHERE name='{last_doc.name}'""",as_dict=True)
			
			recent_year_date = str(docc[0].date)
			current_year_date = str(current_date)

			recent_year_on_lh = datetime.datetime.strptime(recent_year_date, "%Y-%m-%d").year
			current_year = datetime.datetime.strptime(current_year_date, "%Y-%m-%d").year

			if recent_year_on_lh == current_year:
				if docc[0].left_leave > p:
					encashment_days = docc[0].left_leave - p
				else:
					encashment_days = 0

			elif abs(current_year - recent_year_on_lh) > 1:
				if year_served==1:
					encashment_days = 0
				elif year_served > 1:
					if year_served%2!=0:
						encashment_days = p
					else:
						encashment_days = p-1
		else:
			if year_served==1:
				encashment_days = 0
			elif year_served > 1:
				if year_served%2!=0:
					encashment_days = p
				else:
					encashment_days = p-1
		
		dct = {
			'year_served': year_served,
			'encashment_days': encashment_days,
			'p': p,
			'salary': employe_doc[0].basic_salary
		}
	except:

		dct = {
			'year_served':'',
			'encashment_days': '',
			'p': '',
			'salary': ''
		}

	return dct
