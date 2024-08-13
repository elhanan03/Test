# Copyright (c) 2023, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PartyType(Document):
    pass


@frappe.whitelist()
def get_party_type(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
            """select name from `tabParty Type`
	""")
