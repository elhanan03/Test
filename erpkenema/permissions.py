import frappe


def get_employee_data(user):
    doc = frappe.db.sql(
        f"""SELECT * FROM `tabEmployee` WHERE user_id='{user}' and status='Active' """, as_dict=True)
    return doc

def employee_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabEmployee`.branch = '{branch}')".format(branch=doc[0].branch)
        else:
            return "(`tabEmployee`)"

def inventory_area_store_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabInventory Area Store`.quantity > {value} and `tabInventory Area Store`.kenema_pharmacy_drug_shop_number = '{branch}')".format(value=0, branch=doc[0].branch)
        else:
            return "(`tabInventory Area Store`.quantity > {value})".format(value=0)

def sales_area_store_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabSales Area Store`.quantity > {value} and `tabSales Area Store`.kenema_pharmacy_drug_shop_number = '{branch}')".format(value=0, branch=doc[0].branch)
        else:
            return "(`tabSales Area Store`.quantity > {value})".format(value=0)

def good_receiving_voucher_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:

        division = doc[0].division
        if division == 'Branch':
            return "(`tabGood Receiving Voucher`.branch_number = '{branch}')".format(branch=doc[0].branch)
        else:
            return "(`tabGood Receiving Voucher`)"

def store_issue_voucher_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:

        division = doc[0].division
        if division == 'Branch':
            return "(`tabStore Issue Voucher`.branch_number = '{branch}')".format(branch=doc[0].branch)
        else:
            return "(`tabStore Issue Voucher`)"

def sales_attachment_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabSales Attachment`.total_inc_vat > {value} and `tabSales Attachment`.branch_number = '{branch}')".format(value=0, branch=doc[0].branch)
        else:
            return "(`tabSales Attachment`.total_inc_vat > {value})".format(value=0)

def daily_cash_sales_summary_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabDaily Cash sales Summary`.sales_ticket_amount > {value} and `tabDaily Cash sales Summary`.branch='{branch}')".format(value=0, branch=doc[0].branch)
        else:
            return "(`tabDaily Cash sales Summary`.sales_ticket_amount > {value})".format(value=0)

def stock_transfer_memo_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabStock Transfer Memo`.total > {value} and `tabStock Transfer Memo`.from_branch='{branch}')".format(value=0, branch=doc[0].branch)
        else:
            return "(`tabStock Transfer Memo`.total > {value})".format(value=0)
        
def purchase_request_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabPurchase request for drug and medical supplies`.branch='{branch}')".format(branch=doc[0].branch)
        else:
            return "(`tabPurchase request for drug and medical supplies`)"

def good_return_note_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabGood Return Note`.branch='{branch}')".format(branch=doc[0].branch)
        else:
            return "(`tabGood Return Note`)"

def store_return_note_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabStore Return Note`.branch_number='{branch}')".format(branch=doc[0].branch)
        else:
            return "(`tabStore Return Note`)"


def out_of_service_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabOut of service items`.branch_number='{branch}')".format(branch=doc[0].branch)
        else:
            return "(`tabOut of service items`)"


def petty_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabPetty Cash Payment  Voucher`.amount_on_allocated_budget > {value} and `tabPetty Cash Payment  Voucher`.branch='{branch}')".format(value=0, branch=doc[0].branch)
        else:
            return "(`tabPetty Cash Payment  Voucher`.amount_on_allocated_budget > {value})".format(value=0)


def leave_application_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabLeave Application`.branch='{branch}')".format(branch=doc[0].branch)
        else:
            return "(`tabLeave Application`)"


def leave_control_query(user):
    if not user:
        user = frappe.session.user

    doc = get_employee_data(user)

    if doc:
        division = doc[0].division
        if division == 'Branch':
            return "(`tabEmployee Leave Control`.branch='{branch}')".format(branch=doc[0].branch)
        else:
            return "(`tabEmployee Leave Control`)"
