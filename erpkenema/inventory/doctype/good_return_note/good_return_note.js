// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Good Return Note", {
  refresh: function (frm) {
    if (frm.doc.__islocal) {
      var dct;
      frappe.call({
        method:
          "erpkenema.inventory.doctype.good_return_note.good_return_note.get_data",
        args: {},
        async: false,
        callback: function (r) {
          dct = r.message;
        },
      });

      frm.doc.branch = dct["branch"];
      frm.doc.prepared_by = dct["prepared_by"];
      frm.doc.approved_by = dct["approved_by"];
      frm.doc.prepared_by_email = dct["prepared_by_email"];
      frm.doc.approved_by_email = dct["approved_by_email"];

      refresh_many([
        "branch",
        "prepared_by",
        "approved_by",
        "prepared_by_email",
        "approved_by_email",
      ]);
    }
  },

  supplier: function (frm) {
    let supplier = frm.doc.supplier;
    if (supplier) {
      frappe
        .call({
          method:
            "erpkenema.inventory.doctype.good_return_note.good_return_note.get_items",
          args: {
            branch_number: frm.doc.branch,
            return_type: frm.doc.return_type,
            supplier: frm.doc.supplier,
            from_date: frappe.datetime.get_today(),
            to_date: frappe.datetime.add_days(frappe.datetime.get_today(), 180),
          },
        })
        .done((r) => {
          frm.doc.items_list = [];
          $.each(r.message, function (i, e) {
            let items = frm.add_child("items_list");
            items.doc_name = e.name;
            items.item_code = e.item_code;
            items.batch_number = e.batch_number;
            items.description = e.description;
            items.unit = e.unit;
            items.quantity = e.quantity;
            if (frm.doc.return_type == 'Near Expiry'){
              items.unit_purchase_cost = e.unit_purchase_cost;
              items.total_purchase_cost = e.total_purchase_cost;
            }
            if (frm.doc.return_type == 'Consignment Out'){
              items.unit_purchase_cost = e.unit_purchase_cost;
              items.total_purchase_cost = e.total_purchase_cost;
            }
            else{
              items.unit_purchase_cost = e.unit_cost;
              items.total_purchase_cost = e.total_cost;
            }
            
            items.exp_date = e.exp_date;
          });
          refresh_field("items_list");
        });
    }
  },
});
