// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Leave Allocation", {
    holiday_list: function (frm) {
        var dct;
        frappe.call({
          method:
            "erpkenema.hr.doctype.leave_allocation.leave_allocation.get_data",
          args: {
            "holiday_list": frm.doc.holiday_list,
            "total_leave_days": frm.doc.total_leave_days,
            "from_date": frm.doc.from_date,
            "to_date": frm.doc.to_date
          },
          async: false,
          callback: function (r) {
            dct = r.message;
          },
        });
      
        frm.doc.actual_leave_days = dct['actual_leave_days'];
    
        refresh_many(["actual_leave_days"]);
      },
});
