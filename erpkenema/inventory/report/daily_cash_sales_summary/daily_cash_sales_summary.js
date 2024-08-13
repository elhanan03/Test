// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Cash sales Summary"] = {
	"filters": [
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "branch",
			"fieldtype": "Link",
			"label": __("Branch"),
			"options": "Kenema Branches",
			"width": "80",
		},

	]
};
