// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Leave Encashment", {
  employee: function (frm) {
    var dct;
    frappe.call({
      method: "erpkenema.hr.doctype.leave_encashment.leave_encashment.get_data",
      args: {
        "employee_id": frm.doc.employee,
        "date_of_joining": frm.doc.date_of_joining,
        "current_date": frm.doc.date,
      },
      async: false,
      callback: function (r) {
        dct = r.message;
      },
    });

    frm.doc.encashment_days = dct["encashment_days"];
    frm.doc.encashment_amount = (dct["salary"]/26) * (dct["encashment_days"])
    frm.doc.p = dct["p"];

    refresh_many(["encashment_days", "p","encashment_amount"]);
  },


  date: function (frm) {
    var dct;
    frappe.call({
      method: "erpkenema.hr.doctype.leave_encashment.leave_encashment.get_data",
      args: {
        "employee_id": frm.doc.employee,
        "date_of_joining": frm.doc.date_of_joining,
        "current_date": frm.doc.date,
      },
      async: false,
      callback: function (r) {
        dct = r.message;
      },
    });

    frm.doc.encashment_days = dct["encashment_days"];
    frm.doc.encashment_amount = (dct["salary"]/26) * (dct["encashment_days"])
    frm.doc.p = dct["p"];

    refresh_many(["encashment_days", "p", "encashment_amount"]);
  },

});
