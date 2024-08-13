// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Credit Sales Attachment", {
  sales_type: function (frm) {
    frm.doc.to = null;
    frm.doc.full_name = null;
    frm.doc.tin_no = null;
    frm.doc.organization = null;
    frm.doc.credit_limit = null;
    frm.doc.customer_subcity = null;
    frm.doc.customer_woreda = null;
    frm.doc.customer_house_number = null;
    refresh_many([
      "to",
      "full_name",
      "tin_no",
      "organization",
      "credit_limit",
      "customer_subcity",
      "customer_woreda",
      "customer_house_number",
    ]);
    if (frm.doc.sales_type == "Credit Sales") {
      frm.set_query("to", function () {
        return {
          filters: {
            customer_type: "Credit Customer",
          },
        };
      });
    } else {
      frm.set_query("to", function () {
        return {
          filters: {
            customer_type: "Cash Customer",
          },
        };
      });
    }
  },

  setup: function (frm) {
    frm.set_query("to", function () {
      return {
        filters: {
          customer_type: "Credit Customer",
        },
      };
    });

    frm.set_query("item_code", "purchased_medicine", function (doc, cdt, cdn) {
      var row = locals[cdt][cdn];
      return {
        filters: [
          [
            "exp_date",
            ">=",
            frappe.datetime.add_days(frappe.datetime.get_today(), 180),
          ],
          ["description", "like", row.description],
          ["unit", "like", row.unit],
        ],
      };
    });
  },
});

frappe.ui.form.on("Purchased Medicine", "quantity", function (frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  if (item.quantity > item.stock_quantity) {
    frappe.throw("quantity can not be greater than stock quantity");
  } else {
    item.total_price = item.quantity * item.unit_price;
    frm.refresh_field("purchased_medicine");
  }
});
// cur_frm.cscript.custom_validate = function (doc) {
//   if (doc.date < get_today()) {
//     msgprint("You can not select past date in From Date");
//     validated = false;
//   }
// };
