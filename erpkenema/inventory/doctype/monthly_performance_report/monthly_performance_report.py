# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MonthlyPerformanceReport(Document):
	def before_insert(self):
		doc = frappe.db.sql(
                f""" SELECT MAX(refno) as last_number FROM `tabMonthly Performance Report` """, as_dict=1)
		if not doc[0].last_number:
			self.refno = 1
		else:
			self.refno = doc[0].last_number + 1
	def before_save (self):
		total_sales, total_purchase, net_purchase, stock_available_for_sale, ending_stock, gross_margin = 0,0,0,0,0,0,
		for item in self.performance_list:
			if item.description == 'Cash Sales':
				total_sales+= item.performance
				gross_margin+=item.performance

			elif item.description =='Credit Sales':
				total_sales+= item.performance
				gross_margin+=item.performance

			elif item.description =='Beginning Stock':
				stock_available_for_sale+=item.performance
				ending_stock+=item.performance

			elif item.description == 'Cash Purchase':
				total_purchase+=item.performance
				net_purchase+=item.performance
				stock_available_for_sale+=item.performance
				ending_stock+=item.performance


			elif item.description == 'Credit Purchase':
				total_purchase+=item.performance
				net_purchase+=item.performance
				stock_available_for_sale+=item.performance
				ending_stock+=item.performance

			elif item.description == 'Purchase Return':
				net_purchase-=item.performance
				stock_available_for_sale-=item.performance
				ending_stock-=item.performance

			elif item.description =='Purchase Discount':
				net_purchase-=item.performance
				stock_available_for_sale-=item.performance
				ending_stock-=item.performance

			elif item.description =='Transfer In':
				stock_available_for_sale+=item.performance
				ending_stock+=item.performance

			elif item.description =='Consignment In':
				stock_available_for_sale+=item.performance
				ending_stock+=item.performance
				
			elif item.description =='Bonus':
				stock_available_for_sale+=item.performance
				ending_stock+=item.performance

			elif item.description == 'Stock Damaged': 
				ending_stock-=item.performance
			elif item.description =='Stock Expired':
				ending_stock-=item.performance

			elif item.description =='Transfer Out':
				ending_stock-=item.performance

			elif item.description =='Consignmnet Out':
				ending_stock-=item.performance
			
			elif item.description =='Cost of Pharmaceuticals Sold':
				ending_stock-=item.performance
				gross_margin-=item.performance
			
		self.total_sales = total_sales
		self.total_purchase = total_purchase
		self.net_purchase = net_purchase
		self.stock_available_for_sale = stock_available_for_sale
		self.ending_stock = ending_stock
		self.gross_margin = gross_margin
		



@frappe.whitelist()
def get_performance(from_date, to_date, shop_number, description):
		performance_amount = 0
		if description == 'Cash Sales' or description == 'Credit Sales' or 	description == 'Cash Sales Handling (Cash Collected)':
			if description == 'Cash Sales Handling (Cash Collected)':
				description = 'Cash Sales'
				
			doc = frappe.db.sql(f"""SELECT SUM(total_inc_vat) as total FROM `tabSales Attachment` where workflow_state = 'Paid' and sales_type='{description}' and branch_number = '{shop_number}' and date >= '{from_date}' and date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total

		elif description == 'Credit Purchase' or description == 'Cash Purchase' or description == 'Consignment In' or description == 'Bonus' or description == 'Discount':	

			doc = frappe.db.sql(f"""SELECT SUM(total) as total FROM `tabGood Receiving Voucher` where purchase_type='{description}' and branch_number = '{shop_number}' and date >= '{from_date}' and date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total
		
		elif description == 'Consignment Out':	

			doc = frappe.db.sql(f"""SELECT SUM(total) as total FROM `tabGood Return Note` where return_type='{description}' and branch = '{shop_number}' and date >= '{from_date}' and date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total 

		elif description == 'Transfer In':

			doc = frappe.db.sql(f"""SELECT SUM(total_purchase_cost) as total FROM `tabInventory Area Store` where purchase_type='{description}' and kenema_pharmacy_drug_shop_number = '{shop_number}' and date >= '{from_date}' and date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total

		elif description == 'Transfer Out':

			doc = frappe.db.sql(f"""SELECT SUM(total) as total FROM `tabStock Transfer Memo` where  from_branch = '{shop_number}' and date >= '{from_date}' and date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total
		
		elif description == 'Stock Expired':
			
			doc = frappe.db.sql(f"""SELECT SUM(total_cost) as total FROM `tabOut of service items` where  branch_number = '{shop_number}' and exp_date >= '{from_date}' and exp_date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total
		
		elif description == 'Stock Damaged':
			
			doc = frappe.db.sql(f"""SELECT SUM(total_cost) as total FROM `tabOut of service items` where  branch_number = '{shop_number}' and damaged_date >= '{from_date}' and damaged_date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total

		elif description == 'Purchase Return':
			
			doc = frappe.db.sql(f"""SELECT SUM(total) as total FROM `tabGood Return Note` where  branch = '{shop_number}' and date >= '{from_date}' and date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total

		elif description == 'Customer Served(Credit)' or description == 'Customer Served(Cash)':
			if description == 'Customer Served(Credit)':
				description='Credit Sales'
			else:
				description='Cash Sales'

			doc = frappe.db.sql(f"""SELECT COUNT(name) as total FROM `tabSales Attachment` where  branch_number = '{shop_number}' and sales_type='{description}' and date >= '{from_date}' and date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total
		
		elif description == 'Cost of Pharmaceuticals Sold':	
			doc = frappe.db.sql(f"""SELECT SUM(total_purchase_cost) as total FROM `tabSales Attachment` where  branch_number = '{shop_number}' and date >= '{from_date}' and date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total

		elif description == 'Beginning Stock':
			try:
				last_doc = frappe.get_last_doc('Monthly Performance Report',filters={'drug_store_number': shop_number})
				performance_amount = last_doc.ending_stock
			except:
				performance_amount = 0
				frappe.msgprint('Ending Stock of previous month not found !!!')

		elif description == 'Pharmaceuticals Sold At Cost(Insulin)':	
			doc = frappe.db.sql(f"""SELECT SUM(total_purchase_cost) as total FROM `tabPurchased Medicine` where parent in (SELECT name FROM `tabSales Attachment` where branch_number = '{shop_number}' and date >= '{from_date}' and date <= '{to_date}') and profit_margin =0.0""",as_dict=True)
			performance_amount = doc[0].total


		elif description == 'Pharmaceuticals Sold At Cost(Pts Served)':	
			doc = frappe.db.sql(f"""SELECT * FROM `tabPurchased Medicine` where parent in (SELECT name FROM `tabSales Attachment` where branch_number = '{shop_number}' and date >= '{from_date}' and date <= '{to_date}') and profit_margin = 0.0 and description = 'Insulin' group by parent""",as_dict=True)
			performance_amount = len(doc)

		
		elif description == 'Petty Cash Disbursement':	
			doc = frappe.db.sql(f"""SELECT SUM(payable_amounts_in_figure) as total FROM `tabPetty Cash Payment  Voucher` where workflow_state = 'Paid' and branch = '{shop_number}' and date >= '{from_date}' and date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total
			
		elif description == 'Cash Sales Handling (Cash Short)':	

			doc = frappe.db.sql(f"""SELECT SUM(total_cash_short) as total FROM `tabDaily Cash sales Summary` where branch = '{shop_number}' and sales_date >= '{from_date}' and sales_date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total
		
		elif description == 'Cash Sales Handling (Cash Over)':	
			
			doc = frappe.db.sql(f"""SELECT SUM(total_cash_over) as total FROM `tabDaily Cash sales Summary` where branch = '{shop_number}' and sales_date >= '{from_date}' and sales_date <= '{to_date}'""",as_dict=True)
			performance_amount = doc[0].total

		return performance_amount



@frappe.whitelist()
def get_data():
	dct = {}
	try:
		logged_user_email = frappe.session.user
		branch_accountant_doc = frappe.db.sql(f"""SELECT * FROM `tabBranch Accountant` WHERE name = '{logged_user_email}' and status = 'Active' """, as_dict=1)	
					
		branch_manager_doc = frappe.db.sql(f"""SELECT * FROM `tabBranch Manager` WHERE branch = '{branch_accountant_doc[0].branch}' and status = 'Active' """, as_dict=1)

		operation_manager_doc = frappe.db.sql(f"""SELECT * FROM `tabOperation Manager` WHERE status = 'Active' """, as_dict=1)
		
		finance_head_doc = frappe.db.sql(f"""SELECT * FROM `tabFinance` WHERE status = 'Active' """, as_dict=1)

		dct = {
			'drug_store_number': branch_accountant_doc[0].branch,
			'prepared_by': branch_accountant_doc[0].full_name,
			'approved_by': branch_manager_doc[0].full_name,
			'authorized_by': operation_manager_doc[0].full_name,
			'checked_by': finance_head_doc[0].full_name,
			'prepared_by_email': branch_accountant_doc[0].name,
			'approved_by_email': branch_manager_doc[0].name,
			'authorized_by_email': operation_manager_doc[0].name,
			'checked_by_email': finance_head_doc[0].name
		}

	except:

		dct = {
			'drug_store_number': '',
			'prepared_by': '',
			'approved_by': '',
			'authorized_by': '',
			'checked_by': '',
			'prepared_by_email': '',
			'approved_by_email': '',
			'authorized_by_email': '',
			'checked_by_email': ''
		}

	return dct


@frappe.whitelist()
def get_action_plan(action_plan):
    action_plan = frappe.db.sql(
        f""" SELECT * FROM `tabAction plan child` WHERE parent='{action_plan}'""", as_dict=True)
    return action_plan


@frappe.whitelist()
def get_from_to_date(action_plan):
	dct = {}
	try:
		from_to = frappe.db.sql(
			f""" SELECT * FROM `tabAction Plan` WHERE name='{action_plan}'""", as_dict=True)
		dct['from_date'] = from_to[0].from_date
		dct['to_date'] = from_to[0].to_date
	except:
		pass

	return dct
