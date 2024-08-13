# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class JobOffer(Document):
    def before_insert(self):
        doc = frappe.db.sql(
            f""" SELECT MAX(refno) as last_number FROM `tabJob Offer` """, as_dict=1)
        if not doc[0].last_number:
            self.refno = 1
        else:
            self.refno = doc[0].last_number + 1
