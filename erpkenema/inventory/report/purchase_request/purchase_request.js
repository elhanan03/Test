// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchase Request"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			width: "80",
			default: frappe.datetime.month_start(frappe.datetime.get_today()),
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			width: "80",
			default: frappe.datetime.get_today(),
		},

	]
};
