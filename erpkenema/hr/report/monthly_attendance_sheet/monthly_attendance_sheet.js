// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Attendance sheet"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": ("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.month_start(frappe.datetime.get_today()),
		},
		{
			"fieldname": "to_date",
			"label": ("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today(),
		}
	]
};
