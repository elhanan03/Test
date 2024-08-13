// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Available Drugs and Medical Supplies", {
  quantity: function (frm) {
    frm.doc.total_purchase_cost = frm.doc.quantity * frm.doc.unit_purchase_cost;
    refresh_field("total_purchase_cost");
  },
  unit_purchase_cost: function (frm) {
    frm.doc.total_purchase_cost = frm.doc.quantity * frm.doc.unit_purchase_cost;
    refresh_field("total_purchase_cost");
  },
});
