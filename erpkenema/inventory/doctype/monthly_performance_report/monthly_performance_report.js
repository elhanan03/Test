// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Monthly Performance Report", {
  refresh: function (frm) {
    if (frm.doc.__islocal) {
      var dct;
      frappe.call({
        method:
          "erpkenema.inventory.doctype.monthly_performance_report.monthly_performance_report.get_data",
        args: {},
        async: false,
        callback: function (r) {
          dct = r.message;
        },
      });

      frm.doc.drug_store_number = dct["drug_store_number"];
      frm.doc.prepared_by = dct["prepared_by"];
      frm.doc.approved_by = dct["approved_by"];
      frm.doc.authorized_by = dct["authorized_by"];
      frm.doc.checked_by = dct["checked_by"];
      frm.doc.prepared_by_email = dct["prepared_by_email"];
      frm.doc.approved_by_email = dct["approved_by_email"];
      frm.doc.authorized_by_email = dct["authorized_by_email"];
      frm.doc.checked_by_email = dct["checked_by_email"];

      refresh_many([
        "drug_store_number",
        "prepared_by",
        "approved_by",
        "authorized_by",
        "checked_by",
        "prepared_by_email",
        "approved_by_email",
        "authorized_by_email",
        "checked_by_email",
      ]);
    }
  },
  action_plan: function (frm) {
    let action_plan = frm.doc.action_plan;
    if (action_plan) {
      var dct;
      frappe
        .call({
          method:
            "erpkenema.inventory.doctype.monthly_performance_report.monthly_performance_report.get_from_to_date",
          args: { action_plan: action_plan },
          async: false,
          callback: function (r) {
            dct = r.message;
          },
        });
      frm.doc.from_date = dct["from_date"];
      frm.doc.to_date = dct["to_date"];

      refresh_many(["from_date", "to_date"]);

      frappe
        .call({
          method:
            "erpkenema.inventory.doctype.monthly_performance_report.monthly_performance_report.get_action_plan",
          args: { action_plan: action_plan },
          async: false
        })
        .done((r) => {
          frm.doc.monthly_plan = [];
          $.each(r.message, function (i, e) {
            let items = frm.add_child("performance_list");
            items.description = e.description;
            items.plan = e.plan;
            items.performance = get_performance_amount(frm.doc.from_date, frm.doc.to_date, frm.doc.drug_store_number,items.description)

          });
          refresh_field("performance_list");
        });
    }
  },
});

function get_performance_amount(from_date,to_date,drug_store_number,description) {
 
  var performance_amount;
  frappe.call({
    method:
      "erpkenema.inventory.doctype.monthly_performance_report.monthly_performance_report.get_performance",
    args: {
      from_date: from_date,
      to_date: to_date,
      shop_number: drug_store_number,
      description: description,
    },
    async: false,
    callback: function (r) {
      performance_amount = r.message;
    },
  });

  return performance_amount;
}



