// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Over Time Report"] = {
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
			"fieldname": "division",
			"label": __("Division"),
			"fieldtype": "Select",
			"options": ["", "Head Office", "Branch"],
			"width": "200",
		},
		{
			"depends_on": "eval: doc.division == 'Branch'",
			"fieldname": "branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Kenema Branches",
			"width": "200",
		},
		{
			"fieldname": "designation",
			"fieldtype": "Link",
			"label": __("Position"),
			"options": "Designation",
			"width": "120",
		},

	]
};
