// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Payroll Report"] = {
  filters: [
    {
      fieldname: "division",
      label: __("Division"),
      fieldtype: "Select",
      options: ["", "Head Office", "Branch"],
      width: "80",
    },
    {
      depends_on: "eval: doc.division == 'Branch'",
      fieldname: "branch",
      label: __("Branch"),
      fieldtype: "Link",
      options: "Kenema Branches",
      width: "80",
    },
    {
      fieldname: "salary_structure",
      label: __("Salary Structure"),
      fieldtype: "Link",
      options: "Monthly Salary Structure",
      width: "80",
    },
    {
      fieldname: "payroll_sheet",
      label: __("Prepare Payroll Sheet for Bank"),
      fieldtype: "Check",
      width: "80",
    },
  ],
};
