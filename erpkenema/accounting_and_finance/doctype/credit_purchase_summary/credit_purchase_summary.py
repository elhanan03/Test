# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CreditPurchaseSummary(Document):
    pass


@frappe.whitelist()
def get_items(doc):
    items = frappe.db.sql(
        f"""select supplier_name, GROUP_CONCAT(purchase_invoice_number) as fs_number, sum(credit) as credit from `tabCredit Purchase Register Child` where parent='{doc}' group by supplier_name  """, as_dict=True)
    return items
