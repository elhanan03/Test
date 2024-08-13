// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Good Receiving Voucher", {
  setup: function (frm) {
    frm.set_query("purchase_order", function () {
      return {
        filters: [
          ["workflow_state", "=", "Received"],
          ["branch", "=", frm.doc.branch_number]
        ],
      };
    });
    
  },

  refresh: function (frm) {
    if (frm.is_new()) {
      var dct;
      frappe.call({
        method:
          "erpkenema.inventory.doctype.good_receiving_voucher.good_receiving_voucher.get_data",
        args: {},
        async: false,
        callback: function (r) {
          dct = r.message;
        },
      });

      (frm.doc.branch_number = dct["branch_number"]),
        (frm.doc.received_by = dct["received_by"]),
        (frm.doc.posted_by = dct["posted_by"]),
          (frm.doc.posted_by_email = dct["posted_by_email"]),
        refresh_many(["branch_number", "received_by", "posted_by", "posted_by_email"]);
    }
  },
  purchase_order: function (frm) {
    frm.doc.items_received = [];
    let purchase = frm.doc.purchase_order;
    if (purchase) {
      frappe
        .call({
          method:
            "erpkenema.inventory.doctype.good_receiving_voucher.good_receiving_voucher.get_mpr_items",
          args: { purchase_order: purchase },
        })
        .done((r) => {
          $.each(r.message, function (i, e) {
            let items = frm.add_child("items_received");
            items.item_code = e.item_code;
            items.batch_number = e.batch_number;
            items.barcode = e.item_code;
            items.description = e.description;
            items.unit = e.unit;
            items.pharmacological_category = e.pharmacological_category;
            items.quantity = e.supplied_qty;
            items.unit_purchase_cost = e.unit_purchase_cost;
            items.total_purchase_cost = e.total_purchase_cost;
            items.exp_date = e.exp_date;
            // items.unit_selling_price = e.unit_selling_price;
            items.brand = e.brand;
            items.manufacturer = e.manufacturer;
            items.country = e.country;
          });
          refresh_field("items_received");
        });
    }
  },
});
frappe.ui.form.on(
  "Items Received",
  "unit_purchase_cost",
  function (frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    item.total_purchase_cost = item.quantity * item.unit_purchase_cost;
    item.uspbv =
      item.profit * item.unit_purchase_cost + item.unit_purchase_cost;

    if (item.vatable_item) {
      item.vat = 0.15;
    } else {
      item.vat = 0.0;
    }
    let x = item.unit_purchase_cost * item.vat + item.unit_purchase_cost;
    item.unit_selling_price = x * item.profit + x;
    frm.refresh_field("items_received");
  }
);

frappe.ui.form.on("Items Received", "quantity", function (frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  item.total_purchase_cost = item.quantity * item.unit_purchase_cost;
  frm.refresh_field("items_received");
});
frappe.ui.form.on("Items Received", "description", function (frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  item.barcode = item.item_code;
  frm.refresh_field("items_received");
});
frappe.ui.form.on("Items Received", "profit", function (frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  item.uspbv = item.profit * item.unit_purchase_cost + item.unit_purchase_cost;

  if (item.vatable_item) {
    item.vat = 0.15;
  } else {
    item.vat = 0.0;
  }
  let x = item.unit_purchase_cost * item.vat + item.unit_purchase_cost;
  item.unit_selling_price = x * item.profit + x;
  frm.refresh_field("items_received");
});

frappe.ui.form.on("Items Received", "vatable_item", function (frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  if (item.vatable_item) {
    item.vat = 0.15;
  } else {
    item.vat = 0.0;
  }
  let x = item.unit_purchase_cost * item.vat + item.unit_purchase_cost;
  item.unit_selling_price = x * item.profit + x;
  frm.refresh_field("items_received");
});

frappe.ui.form.on("Items Received", "enter_quantity", function (frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  item.retail_price = item.unit_selling_price / item.enter_quantity;
  item.total_retail_pricepiece =
    item.quantity * item.enter_quantity * item.retail_price;
  frm.refresh_field("items_received");
});

frappe.ui.form.on(
  "Items Received",
  "enter_qty_on_piece",
  function (frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    item.retail_price_strip = item.retail_price / item.enter_qty_on_piece;
    frm.refresh_field("items_received");
  }
);

frappe.ui.form.on(
  "Items Received",
  "unit_selling_price",
  function (frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    item.retail_price = item.unit_selling_price / item.enter_quantity;
    item.total_retail_pricepiece =
      item.quantity * item.enter_quantity * item.retail_price;
    frm.refresh_field("items_received");
  }
);

frappe.ui.form.on("Items Received", "retail_price", function (frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  item.retail_price_strip = item.retail_price / item.enter_qty_on_piece;
  frm.refresh_field("items_received");
});
