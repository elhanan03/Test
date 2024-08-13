// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Consignment Sales Payment Confirmation Form", {
  setup: function (frm) {
    frm.set_query("reference_number", function () {
      return {
        filters: {
          purchase_type: "Consignment In",
        },
      };
    });
  },

  reference_number: function (frm) {
    let ref_num = frm.doc.reference_number;
    if (ref_num) {
      frappe
        .call({
          method:
            "erpkenema.inventory.doctype.consignment_sales_payment_confirmation_form.consignment_sales_payment_confirmation_form.get_consignment_items",
          args: { branch_number: frm.doc.branch, ref_num: ref_num },
        })
        .done((r) => {
          frm.doc.reciept = [];
          $.each(r.message, function (i, e) {
            let item = frm.add_child("reciept");
            // item.item_code = e.branch_number,
            // item.cons_no = e.consignment_number
            // item.grv_no = e.name
            // item.description = e.
          });
          refresh_many(["reciept"]);
        });
    }
  },
});
// frappe.ui.form.on(
//   "Consignment Return sales",
//   "sold_quantity",
//   function (frm, cdt, cdn) {
//     let item = locals[cdt][cdn];
//     item.left_quantity = item.quantity_received - item.sold_quantity;
//     frm.refresh_field("return_sales");
//   }
// );

// frappe.ui.form.on(
//   "Consignment Return sales",
//   "unit_cost",
//   function (frm, cdt, cdn) {
//     let item = locals[cdt][cdn];
//     item.total_cost = item.sold_quantity * item.unit_cost;
//     frm.refresh_field("return_sales");
//   }
// );

// frappe.ui.form.on(
//   "Consignment Return sales",
//   "unit_cost",
//   function (frm, cdt, cdn) {
//     let item = locals[cdt][cdn];
//     item.balance = item.left_quantity * item.unit_cost;
//     frm.refresh_field("return_sales");
//   }
// );

// frappe.ui.form.on("Consignment Reciept", "unit_cost", function (frm, cdt, cdn) {
//   let item = locals[cdt][cdn];
//   item.total_cost = item.quantity * item.unit_cost;
//   frm.refresh_field("reciept");
// });

// frappe.ui.form.on(
//   "Consignment Reciept",
//   "unit_selling_price",
//   function (frm, cdt, cdn) {
//     let item = locals[cdt][cdn];
//     item.total_selling_price = item.quantity * item.unit_selling_price;
//     frm.refresh_field("reciept");
//   }
// );
// cur_frm.cscript.custom_validate = function (doc) {
//   if (doc.date < get_today()) {
//     msgprint("You can not select past date in From Date");
//     validated = false;
//   }
// };
