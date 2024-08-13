// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Over Time", {
  before_save: function (frm) {
    let total_hours = 0;
    let overtime_pay = 0;
    let isValid = true;

    frm.doc.working_time.forEach((item) => {
      let fromTime = "08/05/2015" + " " + item.from_time;
      let toTime = "08/05/2015" + " " + item.to_time;

      if (new Date(toTime) < new Date(fromTime)) {
        frappe.msgprint(
          __("To Time cannot be before From Time in row {0}", [item.idx])
        );
        isValid = false;
        return;
      }

      let each_hour = calculate(item.from_time, item.to_time);
      total_hours += each_hour;
      overtime_pay += (frm.doc.basic_salary / 208) * item.rate * each_hour;
    });

    if (!isValid) {
      // Prevent saving if there are invalid entries
      frappe.validated = false;
      return;
    }

    frm.doc.total_working_time = total_hours;
    frm.doc.total_payment = overtime_pay;
    frm.refresh_field("total_working_time");
    frm.refresh_field("total_payment");
  },

  refresh: function (frm) {
    if (frm.doc.__islocal) {
      var dct;
      frappe.call({
        method: "erpkenema.hr.doctype.over_time.over_time.get_data",
        args: {},
        async: false,
        callback: function (r) {
          dct = r.message;
        },
      });

      frm.doc.branch = dct["branch"];
      frm.doc.prepared_by = dct["prepared_by"];
      frm.doc.prepared_by_email = dct["prepared_by_email"];
      frm.doc.approved_by = dct["approved_by"];
      frm.doc.approved_by_email = dct["approved_by_email"];
      frm.doc.finance_head = dct["finance_head"];
      frm.doc.finance_head_email = dct["finance_head_email"];
      frm.doc.hr_manager = dct["hr_manager"];
      frm.doc.hr_manager_email = dct["hr_manager_email"];

      refresh_many([
        "branch",
        "finance_head",
        "finance_head_email",
        "hr_manager",
        "hr_manager_email",
        "prepared_by",
        "prepared_by_email",
        "approved_by",
        "approved_by_email",
      ]);
    }
  },

  setup: function (frm) {
    frm.set_query("employee_name", function () {
      return {
        filters: {
          branch: frm.doc.branch,
        },
      };
    });
  },
});

frappe.ui.form.on("Working Time", {
  from_time: function (frm, cdt, cdn) {
    validateTimeOrder(frm, cdt, cdn);
    calculateTotalTime(frm, cdt, cdn);
  },
  to_time: function (frm, cdt, cdn) {
    validateTimeOrder(frm, cdt, cdn);
    calculateTotalTime(frm, cdt, cdn);
  },
});

function validateTimeOrder(frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  let fromTime = "08/05/2015" + " " + item.from_time;
  let toTime = "08/05/2015" + " " + item.to_time;

  if (new Date(toTime) < new Date(fromTime)) {
    frappe.msgprint(
      __("To Time cannot be before From Time in row {0}", [item.idx])
    );
    item.to_time = "";
    item.total_time = "";
    frm.refresh_field("working_time");
  }
}

function calculateTotalTime(frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  let d1 = "08/05/2015" + " " + item.from_time;
  let d2 = "08/05/2015" + " " + item.to_time;

  let date1 = new Date(d2);
  let date2 = new Date(d1);

  let diff = date1.getTime() - date2.getTime();
  let msec = diff;
  let hh = Math.floor(msec / 1000 / 60 / 60);

  item.total_time = `${hh}:${Math.floor((msec / 1000 / 60) % 60)}:${Math.floor(
    (msec / 1000) % 60
  )}`;
  frm.refresh_field("working_time");
}

function calculate(from_time, to_time) {
  let ft = "08/05/2015" + " " + from_time;
  let tt = "08/05/2015" + " " + to_time;
  let date1 = new Date(tt);
  let date2 = new Date(ft);

  let diff = date1.getTime() - date2.getTime();
  let msec = diff;
  let hh = msec / 1000 / 60 / 60;

  return hh;
}
