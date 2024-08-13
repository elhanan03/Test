// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Purchase request for drug and medical supplies", {
  refresh: function (frm) {
    if (frm.is_new()) {
      var dct;
      frappe.call({
        method:
          "erpkenema.inventory.doctype.purchase_request_for_drug_and_medical_supplies.purchase_request_for_drug_and_medical_supplies.get_data",
        args: {},
        async: false,
        callback: function (r) {
          dct = r.message;
        },
      });

        (frm.doc.branch = dct["branch"]),
        (frm.doc.requested_by = dct["requested_by"]),
        (frm.doc.approved_by = dct["approved_by"]),
        (frm.doc.authorized_by = dct["authorized_by"]),
        (frm.doc.requested_by_email = dct["requested_by_email"]),
        (frm.doc.approved_by_email = dct["approved_by_email"]),
        (frm.doc.authorized_by_email = dct["authorized_by_email"]);

      refresh_many([
        "branch",
        "requested_by",
        "approved_by",
        "authorized_by",
        "requested_by_email",
        "approved_by_email",
        "authorized_by_email",
      ]);

      frm.fields_dict.date.datepicker.update({
        minDate: new Date(frappe.datetime.get_today()),
      });
    }
  },
});

+frappe.ui.form.on("MPR_Child_Table", "supplied_qty", function (frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  item.total_purchase_cost = item.supplied_qty * item.unit_purchase_cost;
  frm.refresh_field("mpr");
});

frappe.ui.form.on(
  "MPR_Child_Table",
  "unit_purchase_cost",
  function (frm, cdt, cdn) {
    let item = locals[cdt][cdn];
    item.total_purchase_cost = item.supplied_qty * item.unit_purchase_cost;
    frm.refresh_field("mpr");
  }
);

frappe.ui.form.on("MPR_Child_Table", "exp_date", function (frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  let six_months_from_today = frappe.datetime.add_months(frappe.datetime.get_today(), 6);

  if (item.exp_date < six_months_from_today) {
      frappe.msgprint("The expiry date must be greater than 6 months from today!");
      frappe.model.set_value(cdt, cdn, "exp_date", six_months_from_today);
  }
});

frappe.ui.form.on("MPR_Child_Table", {
    supplied_qty: function (frm, cdt, cdn) {
        let item = locals[cdt][cdn];
        if (item.supplied_qty > item.requested_qty) {
            frappe.msgprint("The supplied quantity cannot exceed the requested quantity.");
            frappe.model.set_value(cdt, cdn, "supplied_qty", ""); // Clear the supplied_qty field
            frappe.validated = false;
        }
    }
});
