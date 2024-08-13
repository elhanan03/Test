// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["List Of Customer Organization"] = {
	"filters": [
		{
			fieldname: "organization_type",
			label: __("Organization Type"),
			fieldtype: "Select",
			options: ["","Federal health insurance beneficiaries", "Addis Ababa health insurance beneficiaries", "Organization beneficiaries", "Others"],
			width: "200",
		},
	
	

	]
};
