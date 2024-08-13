// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer"] = {
	"filters": [
		{
			fieldname: "customer_type",
			label: __("Customer Type"),
			fieldtype: "Select",
			options: ["", "Credit Customer", "Cash Customer"],
			width: "200",
		},
		{
			depends_on: "eval: doc.customer_type == 'Credit Customer'",
			fieldname: "organization",
			label: __("Organization"),
			fieldtype: "Link",
			options: "Organization",
			width: "200",
		},

	]
};
