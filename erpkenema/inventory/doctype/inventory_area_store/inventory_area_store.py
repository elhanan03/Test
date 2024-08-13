# Copyright (c) 2022, TechEthio IT Solution plc and contributors
# For license information, please see license.txt

from frappe.utils import nowdate, add_days
import frappe
from frappe.model.document import Document


class InventoryAreaStore(Document):
    def check_expiry():
        # Get all items with expiry date less than or equal to today
        items = frappe.get_list("Inventory Area Store", filters={"exp_date": (
            "<=", nowdate())}, fields=["name", "exp_date"])

        # Create a list of expired item names and their expiry dates, with links to the item detail page
        expired_items = []
        for item in items:
            item_link = f'<a href="/desk#/Form/Erpkenema/Inventory Area Store/{item.name}"> {item.name}</a>'

            expired_item = f"{item_link} (expiry date: {item.exp_date})"
            expired_items.append(expired_item)

        if expired_items:
            # If there are expired items, create a notification message with links to the item detail pages
            message = "The following items have expired:\n" + \
                "\n".join(expired_items)

            # Create a popup notification with the message
            frappe.msgprint(message, title="Expired Items",
                            indicator="red")


    check_expiry()
