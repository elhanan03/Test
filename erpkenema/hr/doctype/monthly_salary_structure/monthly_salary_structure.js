// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Monthly Salary Structure", {
  setup: function (frm) {
    frm.set_query("name1", "earnings", function (doc, cdt, cdn) {
      var row = locals[cdt][cdn];
      return {
        filters: [["type", "like", "Earning"]],
      };
    });

    frm.set_query("name1", "deductions", function (doc, cdt, cdn) {
      var row = locals[cdt][cdn];
      return {
        filters: [["type", "like", "Deduction"]],
      };
    });
  },
  previous_month: function (frm) {
    let previous_month = frm.doc.previous_month;
    if (previous_month) {
      frappe
        .call({
          method:
            "erpkenema.hr.doctype.monthly_salary_structure.monthly_salary_structure.get_previous_month",
          args: { previous_month: previous_month },
        })
        .done((r) => {
          frm.doc.earnings = [];
          frm.doc.deductions = [];

          $.each(r.message, function (i, e) {
            if (e.parentfield == "earnings") {
              let earning = frm.add_child("earnings");
              earning.name1 = e.name1;
              earning.type = e.type;
              earning.is_tax_applicable = e.is_tax_applicable;
              earning.do_not_include_in_total = e.do_not_include_in_total;
              earning.earning_category = e.earning_category;
              earning.allowance_type = e.allowance_type;
              earning.deduction_category = e.deduction_category;
              earning.formula = e.formula;
              earning.amount = e.amount;

            } else if (e.parentfield == "deductions") {
              let deduction = frm.add_child("deductions");
              deduction.name1 = e.name1;
              deduction.type = e.type;
              deduction.formula = e.formula;
              deduction.amount = e.amount;
              deduction.do_not_include_in_total = e.do_not_include_in_total;
              deduction.deduction_category = e.deduction_category;

            }
          });
          refresh_many(["earnings", "deductions"]);
        });
    }
  },
});
