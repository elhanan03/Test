// // Copyright (c) 2023, TechEthio IT Solution plc and contributors
// // For license information, please see license.txt
// /* eslint-disable */

// frappe.query_reports["Fast Sold Items"] = {
// 	"filters": [
// 		{
// 			fieldname: "from_date",
// 			label: __("From Date"),
// 			fieldtype: "Date",
// 			width: "80",
// 			default: frappe.datetime.month_start(frappe.datetime.get_today()),
// 		  },
// 		  {
// 			fieldname: "to_date",
// 			label: __("To Date"),
// 			fieldtype: "Date",
// 			width: "80",
// 			default: frappe.datetime.get_today(),
// 		  },
// 	]
// };


// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Fast Sold Items"] = {
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
        {
            fieldname: "abc_category",
            label: __("ABC Category"),
            fieldtype: "Select",
            options: ["A", "B", "C"],
            width: "80",
        },
    ]
};
