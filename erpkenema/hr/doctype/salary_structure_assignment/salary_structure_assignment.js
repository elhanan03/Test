// // Copyright (c) 2022, TechEthio IT Solution plc and contributors
// // For license information, please see license.txt

frappe.ui.form.on("Salary Structure Assignment", {
  setup: function (frm) {
    frm.set_query("employee", function () {
      return {
        filters: {
          status: "Active",
        },
      };
    });
  },
  salary_structure: function (frm) {
    let sal_st = frm.doc.salary_structure;
    if (sal_st) {
      frappe.call({
        method:
          "erpkenema.hr.doctype.salary_structure_assignment.salary_structure_assignment.get_monthly_salary_structure",
        args: { salary_structure: sal_st },
        callback: function (r) {
          frm.doc.earning = [];
          frm.doc.deduction = [];
          $.each(r.message, function (i, e) {
            if (e.parentfield == "earnings") {
              let earning = frm.add_child("earning");
              earning.name1 = e.name1;
              earning.type = e.type;
              earning.amount = e.amount;
              earning.formula = e.formula;
              earning.is_tax_applicable = e.is_tax_applicable;
              earning.do_not_include_in_total = e.do_not_include_in_total;
              earning.earning_category = e.earning_category;
              earning.allowance_type = e.allowance_type;
              earning.deduction_category = e.deduction_category;
            } else {
              let deduction = frm.add_child("deduction");
              deduction.name1 = e.name1;
              deduction.type = e.type;
              deduction.amount = e.amount;
              deduction.formula = e.formula;
              deduction.is_tax_applicable = e.is_tax_applicable;
              deduction.do_not_include_in_total = e.do_not_include_in_total;
              deduction.earning_category = e.earning_category;
              deduction.allowance_type = e.allowance_type;
              deduction.deduction_category = e.deduction_category;
            }
          });
          refresh_many(["earning", "deduction"]);
        },
      });
    }
  },
  refresh: function (frm) {
    frm.add_custom_button(
      __("Assign Salary Structure to All Active Employees"),
      function () {
        frappe.prompt(
          {
            label: "Salary Structure",
            fieldname: "salary_structure",
            fieldtype: "Link",
            options: "Monthly Salary Structure",
            reqd: 1,
          },
          function (data) {
            frappe.call({
              method:
                "erpkenema.hr.doctype.salary_structure_assignment.salary_structure_assignment.assign_salary_structure_bulk",
              args: {
                salary_structure: data.salary_structure,
              },
              callback: function (r) {
                if (r.message) {
                  frappe.msgprint(
                    __("Salary Structure assigned to all active employees.")
                  );
                }
              },
            });
          },
          __("Assign Salary Structure to All Active Employees"),
          __("Assign")
        );
      }
    );
  },
});
