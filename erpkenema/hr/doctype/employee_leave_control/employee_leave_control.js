// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Leave Control", {
  
  leave_application: function (frm) {
    var dct;
    frappe.call({
      method:
        "erpkenema.hr.doctype.employee_leave_control.employee_leave_control.get_data",
      args: {
        "date_of_joining": frm.doc.date_of_joining,
        "current_date": frm.doc.current_date,
        "employee_id": frm.doc.employee_id
      },
      async: false,
      callback: function (r) {
        dct = r.message;
      },
    });

    frm.doc.year_served = dct["year_served"];
    frm.doc.total_leave_days = dct["total_leave_days"];
    frm.doc.used_leave_days = dct["used_leave_days"];
    frm.doc.leave_balance =  dct["leave_balance"];
    frm.doc.role = dct["role"];
    
    refresh_many(["year_served","total_leave_days", "used_leave_days", "leave_balance","role"]);
  },


  current_date: function (frm) {
    frm.doc.year_served = null
    frm.doc.total_leave_days = null
    frm.doc.used_leave_days = null
    frm.doc.leave_balance = null

    refresh_many(["year_served","total_leave_days", "used_leave_days", "leave_balance"]);

    var dct;
    frappe.call({
      method:
        "erpkenema.hr.doctype.employee_leave_control.employee_leave_control.get_data",
      args: {
        "date_of_joining": frm.doc.date_of_joining,
        "current_date": frm.doc.current_date,
        "employee_id": frm.doc.employee_id
      },
      async: false,
      callback: function (r) {
        dct = r.message;
      },
    });

    frm.doc.year_served = dct["year_served"];
    frm.doc.total_leave_days = dct["total_leave_days"];
    frm.doc.used_leave_days = dct["used_leave_days"];
    frm.doc.leave_balance =  dct["leave_balance"];
    frm.doc.role = dct["role"];
    
    refresh_many(["year_served","total_leave_days", "used_leave_days", "leave_balance","role"]);
  },
});
