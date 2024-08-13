// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Information page"] = {
	"filters": [
		{
			fieldname: "division",
			label: __("Division"),
			fieldtype: "Select",
			options: ["", "Head Office", "Branch"],
			width: "200",
		},
		{
			depends_on: "eval: doc.division == 'Branch'",
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "Kenema Branches",
			width: "200",
		},


	]
};
