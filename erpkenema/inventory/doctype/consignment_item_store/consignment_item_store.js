// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Consignment Item Store", {
  unit_purchase_cost: function (frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    item.total_cost = item.quantity * item.unit_purchase_cost;
    frm.refresh_field("total_cost");
  },
  quantity: function (frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    item.total_cost = item.quantity * item.unit_purchase_cost;
    frm.refresh_field("total_cost");
  },
});
// cur_frm.cscript.custom_validate = function(doc) {
// 	if (doc.entry_date < get_today()) {
// 		msgprint("You can not select past date in From Date");
// 		validated = false;
// 	}
// }
