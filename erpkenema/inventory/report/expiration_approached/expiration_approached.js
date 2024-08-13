// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Expiration Approached"] = {
  filters: [
    {
      fieldname: "store",
      label: __("Store"),
      fieldtype: "Select",
      width: "80",
      options: ["Inventory Area Store", "Sales Area Store"],
      default: "Inventory Area Store",
    },
    {
      fieldname: "from_date",
      label: __("From Date"),
      fieldtype: "Date",
      width: "80",
      read_only: 0,
      default: frappe.datetime.get_today(),
    },
    {
      fieldname: "to_date",
      label: __("To Date"),
      fieldtype: "Date",
      width: "80",
      read_only: 1,
      default: frappe.datetime.add_days(
        frappe.datetime.get_today(),
        (days = 180)
      ),
    },
  ],
};
