// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */

	const currentYear = frappe.datetime.get_today().slice(0, 4);
	// Create a new datetime object for July of the previous year
	const previousYearJuly = frappe.datetime.add_months(`${currentYear}-01-01`, -6);
	// Create a new datetime object for June of the current year
	const currentYearJune = frappe.datetime.add_months(`${currentYear}-01-01`, 5);
  
frappe.query_reports["Annual Credit Sales Summary"] = {

	"filters": [
		  {
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			width: "80",
			read_only: 1,
			default: previousYearJuly,
		  },
		  {
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			width: "80",
			read_only: 1,
			default: currentYearJune,
		  },
	]
};
