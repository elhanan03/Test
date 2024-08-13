
import frappe
from frappe.utils import now_datetime, add_to_date
from erpkenema.inventory.doctype.inventory_area_store.inventory_area_store import InventoryAreaStore


def all():
    pass


def update_job_opening_status():
    # Get all job openings
    job_openings = frappe.get_all('Job Opening', filters={'status': 'Open'})
    # Iterate through each job opening
    for job_opening in job_openings:
        doc = frappe.get_doc('Job Opening', job_opening.name)

        # Check if the deadline date has passed
        if doc.deadline_date <= now_datetime().date():
            doc.status = 'Closed'
            doc.save()


def schedule_check_expiry():
    # Call the check_expiry method
    InventoryAreaStore.check_expiry()

