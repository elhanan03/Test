// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Store Issue Voucher", {
  setup: function (frm) {
    frm.set_query("item_code", "siv", function (doc, cdt, cdn) {
      var row = locals[cdt][cdn];
      var filters = [
        ["quantity", ">", 0],
    ];

      var today = frappe.datetime.get_today();
      var purchase_type = row.purchase_type; // Assuming 'purchase_type' is the field name representing the purchase type

      if (purchase_type === "Consignment In") {
        filters.push(["exp_date", ">=", frappe.datetime.add_days(today, 1)]);
        filters.push(["kenema_pharmacy_drug_shop_number", "=", frm.doc.branch_number]);
        filters.push(["purchase_type", "=", "Consignment In"]);
      } else {
        filters.push(["exp_date", ">=", frappe.datetime.add_months(today, 6)]);
        filters.push(["kenema_pharmacy_drug_shop_number", "=", frm.doc.branch_number]);

      }

      return {
        filters: filters,
        get_query: function () {
          var sort_direction = (purchase_type === "Consignment") ? "ASC" : "DESC";
          return {
            query: `SELECT item_code, exp_date FROM \`tabInventory Area Store\`
                        WHERE quantity > 0 AND exp_date >= '${frappe.datetime.str_to_user(today)}'
                        ORDER BY ABS(DATEDIFF(exp_date, '${frappe.datetime.str_to_user(today)}')) ${sort_direction}`,
            filters: filters
          };
        }
      };
    });


    frm.set_query("confirmed_by", function () {
      return {
        filters: {
          branch: frm.doc.branch_number,
          name: ["!=", frm.doc.requested_by_email],
        },
      };
    });
  },


  refresh: function (frm) {
    if (frm.is_new()) {
      var dct;
      frappe.call({
        method:
          "erpkenema.inventory.doctype.store_issue_voucher.store_issue_voucher.get_data",
        args: {},
        async: false,
        callback: function (r) {
          dct = r.message;
        },
      });

      frm.doc.branch_number = dct["branch_number"];
      frm.doc.requested_by = dct["requested_by"];
      frm.doc.approved_by = dct["approved_by"];
      frm.doc.issued_by = dct["issued_by"];
      frm.doc.requested_by_email = dct["requested_by_email"];
      frm.doc.approved_by_email = dct["approved_by_email"];
      frm.doc.issued_by_email = dct["issued_by_email"];

      frm.refresh_fields([
        "branch_number",
        "requested_by",
        "approved_by",
        "issued_by",
        "requested_by_email",
        "approved_by_email",
        "issued_by_email",
      ]);
    }
  },
});

frappe.ui.form.on("SIV", {
  issued_qty: function (frm, cdt, cdn) {
    calculate_values(frm, cdt, cdn);
  },

  value: function (frm, cdt, cdn) {
    calculate_values(frm, cdt, cdn);
  },
});

function calculate_values(frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  item.unit_purchase_cost = item.unit_cost / item.value;
  item.total_cost = item.issued_qty * item.unit_selling_price_after_vat;
  item.unit_selling_price = item.unit_selling_price_after_vat / item.value;
  item.total_selling_price_before_vat =
    item.issued_qty * item.value * item.unit_selling_price;
  item.quantity_issued_to_sales = item.issued_qty * item.value;
  frm.refresh_field("siv");
}

frappe.ui.form.on("SIV", {
  issued_qty: function (frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    if (item.issued_qty > item.stock_qty) {
      frappe.msgprint("The Issued quantity cannot exceed the Stock quantity.");
      frappe.model.set_value(cdt, cdn, "issued_qty", item.stock_qty); // Set issued_qty to stock_qty
      frappe.validated = false;
    }
  }
});
