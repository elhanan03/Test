// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Store Return Note", {
  refresh: function (frm) {
    if (frm.doc.__islocal) {
      var dct;
      frappe.call({
        method:
          "erpkenema.inventory.doctype.store_return_note.store_return_note.get_data",
        args: {},
        async: false,
        callback: function (r) {
          dct = r.message;
        },
      });

      frm.doc.branch_number = dct["branch_number"];
      frm.doc.prepared_by = dct["prepared_by"];
      frm.doc.approved_by = dct["approved_by"];
      frm.doc.received_by = dct["received_by"];
      frm.doc.received_by_email = dct["received_by_email"];
      frm.doc.prepared_by_email = dct["prepared_by_email"];
      frm.doc.approved_by_email = dct["approved_by_email"];

      refresh_many([
        "branch_number",
        "prepared_by",
        "approved_by",
        "received_by",
        "received_by_email",
        "prepared_by_email",
        "approved_by_email",
      ]);
    }
  },

  from_doc: function (frm) {
    frm.doc.damaged_or_expired_items = [];
    frm.doc.damaged_or_expired_items_from_inventory = [];
    frm.doc.return_type = null;
    refresh_many([
      "return_type",
      "damaged_or_expired_items",
      "damaged_or_expired_items_from_inventory",
    ]);
  },
  return_type: function (frm) {
    frm.doc.damaged_or_expired_items = [];
    frm.doc.damaged_or_expired_items_from_inventory = [];
    let ret_type = frm.doc.return_type;
    if (ret_type == "Expired") {
      frm.fields_dict.damaged_or_expired_items.grid.fields_map.damaged_date.hidden = 1;
      frm.fields_dict.damaged_or_expired_items_from_inventory.grid.fields_map.damaged_date.hidden = 1;

      frappe
        .call({
          method:
            "erpkenema.inventory.doctype.store_return_note.store_return_note.get_expired_items",
          args: {
            doctype: frm.doc.from_doc,
            date: frappe.datetime.get_today(),
            branch_number: frm.doc.branch_number,
          },
        })
        .done((r) => {
          frm.doc.damaged_or_expired_items = [];
          frm.doc.damaged_or_expired_items_from_inventory = [];
          $.each(r.message, function (i, e) {
            if (frm.doc.from_doc == "Sales Area Store") {
              let exp_items = frm.add_child("damaged_or_expired_items");

              exp_items.description = e.description;
              exp_items.unit = e.unit;
              exp_items.item_code = e.name;
              exp_items.supplier = e.supplier;
              exp_items.batch_number = e.batch_number;
              exp_items.pharmacological_category = e.pharmacological_category;
              exp_items.brand = e.brand;
              exp_items.manufacturer = e.manufacturer;
              exp_items.country = e.country;
              exp_items.purchase_type = e.purchase_type;
              exp_items.quantity = e.quantity;
              exp_items.exp_date = e.exp_date;
              exp_items.unit_cost = e.unit_purchase_cost;
              exp_items.total_cost = exp_items.quantity * exp_items.unit_cost;
            } else if (frm.doc.from_doc == "Inventory Area Store") {
              let exp_items = frm.add_child(
                "damaged_or_expired_items_from_inventory"
              );

              exp_items.description = e.description;
              exp_items.unit = e.unit;
              exp_items.item_code = e.name;
              exp_items.supplier = e.supplier;
              exp_items.batch_number = e.batch_number;
              exp_items.pharmacological_category = e.pharmacological_category;
              exp_items.brand = e.brand;
              exp_items.manufacturer = e.manufacturer;
              exp_items.country = e.country;
              exp_items.purchase_type = e.purchase_type;
              exp_items.quantity = e.quantity;
              exp_items.exp_date = e.exp_date;
              exp_items.unit_cost = e.unit_purchase_cost;
              exp_items.total_cost = exp_items.quantity * exp_items.unit_cost;
            }
          });
          refresh_many([
            "damaged_or_expired_items",
            "damaged_or_expired_items_from_inventory",
          ]);
        });
    } else {
      frm.fields_dict.damaged_or_expired_items.grid.fields_map.damaged_date.hidden = 0;
      frm.fields_dict.damaged_or_expired_items_from_inventory.grid.fields_map.damaged_date.hidden = 0;

      frm.set_query(
        "item_code",
        "damaged_or_expired_items",
        function (doc, cdt, cdn) {
          var row = locals[cdt][cdn];
          return {};
        }
      );

      refresh_many([
        "damaged_or_expired_items",
        "damaged_or_expired_items_from_inventory",
      ]);
    }
  },
});
frappe.ui.form.on(
  "Damaged or Expired Items",
  "quantity",
  function (frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    item.total_cost = item.quantity * item.unit_cost;
    frm.refresh_field("damaged_or_expired_items");
  }
);

frappe.ui.form.on(
  "Damaged or Expired Items from Inventory",
  "quantity",
  function (frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    item.total_cost = item.quantity * item.unit_cost;
    frm.refresh_field("damaged_or_expired_items_from_inventory");
  }
);


frappe.ui.form.on(
  "Other Returned Items",
  "quantity",
  function (frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    item.total_cost = item.quantity * item.unit_cost;
    frm.refresh_field("other_items");
  }
);