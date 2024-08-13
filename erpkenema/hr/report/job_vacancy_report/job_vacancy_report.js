// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Job Vacancy Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "120",
			"default": frappe.datetime.month_start(frappe.datetime.get_today()),
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "120",
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "branch",
			"fieldtype": "Link",
			"label": __("Branch"),
			"options": "Kenema Branches",
			"width": "120",
		},
		{
			"fieldname": "department",
			"fieldtype": "Link",
			"label": __("Department"),
			"options": "Department",
			"width": "120",
		},
		{
			"fieldname": "position",
			"fieldtype": "Link",
			"label": __("Position"),
			"options": "Designation",
			"width": "120",
		},

	]
};
