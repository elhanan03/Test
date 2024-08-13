import frappe

@frappe.whitelist()
def get_employee_data():
    user = frappe.session.user
    doc = frappe.db.sql(
        f"""SELECT * FROM `tabEmployee` WHERE user_id='{user}' and status='Active' """, as_dict=True)
    return doc