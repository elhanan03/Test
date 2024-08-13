# from erpkenema import check_expiry
# from apscheduler.schedulers.background import BackgroundScheduler
# from frappe import *
# from frappe.ui.form import Form




app_name = "erpkenema"
app_title = "Erpkenema"
app_publisher = "TechEthio IT Solution plc"
app_description = "ERP System for kenema Pharmacies Enterprise"
app_email = "dev@techethio.com"
app_license = "MIT"


# override_whitelisted_methods = {
#     "frappe.www.login.post_login": "erpkenema.www.login.post_login"
# }


# def set_sidebar_hidden(form):
#     form.meta.sidebar = 1

# def hide_sidebar_globally():
#     Form.set_onload(set_sidebar_hidden)

# hide_sidebar_globally()

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/erpkenema/css/erpkenema.css"
# app_include_js = "/assets/erpkenema/js/erpkenema.js"

# include js, css files in header of web template
# web_include_css = "/assets/erpkenema/css/erpkenema.css"
# web_include_js = "/assets/erpkenema/js/erpkenema.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "erpkenema/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "erpkenema.utils.jinja_methods",
# 	"filters": "erpkenema.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "erpkenema.install.before_install"
# after_install = "erpkenema.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "erpkenema.uninstall.before_uninstall"
# after_uninstall = "erpkenema.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "erpkenema.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Inventory Area Store": "erpkenema.permissions.inventory_area_store_query",
    "Sales Area Store": "erpkenema.permissions.sales_area_store_query",
    "Employee": "erpkenema.permissions.employee_query",
    "Good Receiving Voucher": "erpkenema.permissions.good_receiving_voucher_query",
    "Store Issue Voucher": "erpkenema.permissions.store_issue_voucher_query",
    "Sales Attachment": "erpkenema.permissions.sales_attachment_query",
    "Daily Cash sales Summary": "erpkenema.permissions.daily_cash_sales_summary_query",
    "Stock Transfer Memo": "erpkenema.permissions.stock_transfer_memo_query",
    "Purchase request for drug and medical supplies": "erpkenema.permissions.purchase_request_query",
    "Good Return Note": "erpkenema.permissions.good_return_note_query",
    "Store Return Note": "erpkenema.permissions.store_return_note_query",
    "Out of service items": "erpkenema.permissions.out_of_service_query",
    "Petty Cash Payment  Voucher": "erpkenema.permissions.petty_query",
    "Leave Application": "erpkenema.permissions.leave_application_query",
    "Employee Leave Control": "erpkenema.permissions.leave_control_query"
}

has_permission = {
	"Event": "frappe.desk.doctype.event.event.has_permission",
}

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    'all': [
        'erpkenema.tasks.update_job_opening_status',
        "erpkenema.tasks.schedule_check_expiry"
    ],
    # 'daily': [
    #     'erpkenema.tasks.daily'
    #     "erpkenema.tasks.schedule_check_expiry"
    # ],
    # 'hourly': [
    #     'erpkenema.tasks.hourly'
    # ],
    # 'weekly': [
    #     'erpkenema.tasks.weekly'
    # ],
}


# Cron Jobs
# ---------
 
cron_jobs = [
    {
        'cron_string': '* * * * *',
        'method': 'erpkenema.tasks.update_job_opening_status',
        'method': 'erpkenema.tasks.schedule_check_expiry'
    },
#     {
#         'cron_string': '0 0 * * *',
#         'method': 'erpkenema.tasks.daily'
#     },
#     {
#         'cron_string': '0 * * * *',
#         'method': 'erpkenema.tasks.hourly'
#     },
#     {
#         'cron_string': '0 0 * * 0',
#         'method': 'erpkenema.tasks.weekly'
#     }
]
# Testing
# -------

# before_tests = "erpkenema.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "erpkenema.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "erpkenema.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"erpkenema.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []

fixtures = [
    "Workflow State",
    "Workflow Action Master",
    "Workflow",
    "UOM",
    "Inventory Items",
    "Address-Kpe",
    "Kenema Branches",
    "Role",
    "Role Profile",
    "Module Profile",
    "Pharmacological Category",
    "Salary Scale Name",
    "Level",
    "Scale",
    "Salary Structure",
    "Salary Component",
    "Holiday List",
    "Workspace",
    "Account Type",
    "Chart Of Accounts",
    "Custom DocPerm",
    "Income Tax",
    "Leave Type",
    "Working Time Name",
    "Designation",
    "Department",
    "Shift Type",
    "PP Rate",
    "Mobile Allowance",
    "Website Settings"



]