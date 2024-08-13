// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Salary Slip", {
  setup: function (frm) {
    frm.set_query("employee", function () {
      return {
        filters: {
          status: "Active",
        },
      };
    });
    frm.set_query("overtime", function () {
      if (frm.doc.employee) {
        return {
          filters: {
            employee_name: frm.doc.employee,
            workflow_state: "Checked"
          },
        };
      } else {
        return {};
      }
    });

    frm.set_query("salary_structure", function () {
      if (frm.doc.employee) {
        return {
          filters: {
            employee: frm.doc.employee,
            salary_structure: frm.doc.sal_str,
          },
        };
      } else {
        return {};
      }
    });
  },
  //   refresh: function (frm) {
  //     frm.add_custom_button(
  //         __("Create Salary Slips for Selected Employees"),
  //         function () {
  //             frappe.prompt(
  //                 [
  //                     {
  //                         label: "Salary Structure",
  //                         fieldname: "salary_structure",
  //                         fieldtype: "Link",
  //                         options: "Monthly Salary Structure",
  //                         reqd: 1,
  //                     },
  //                     {
  //                       label: "Employees",
  //                       fieldname: "employees",
  //                       fieldtype: "MultiSelectList",
  //                       options: "Salary Structure Assignment",
  //                       get_data: function (txt) {
  //                           return frappe.db.get_link_options("Salary Structure Assignment", txt, {
  //                               employees: frm.doc.salary_structure // Filter by the salary structure
  //                           });
  //                       },
  //                       reqd: 1,
  //                   },
  //                 ],
  //                 function (data) {
  //                     frappe.call({
  //                         method: "erpkenema.hr.doctype.salary_slip.salary_slip.create_salary_slips_for_selected_employees",
  //                         args: {
  //                             salary_structure: data.salary_structure,
  //                             salary_structure_assignment: data.employees, // Corrected from 'values'
  //                         },
  //                         callback: function (r) {
  //                             if (r.message) {
  //                                 frappe.msgprint(
  //                                     __("Salary Slips created: " + r.message.join(", "))
  //                                 );
  //                                 frm.reload_doc(); // Reload the form after creating salary slips
  //                             }
  //                         },
  //                     });
  //                 },
  //                 __("Select Salary Structure and Employees"),
  //                 __("Create")
  //             );
  //         }
  //     );
  // },
  // salary_structure: function (frm) {
  //   let sal_st = frm.doc.salary_structure;
  //   if (sal_st) {
  //     frappe
  //       .call({
  //         method:
  //           "erpkenema.hr.doctype.salary_slip.salary_slip.get_salary_structure",
  //         args: { salary_structure: sal_st },
  //       })
  //       .done((r) => {
  //         frm.doc.earning = [];
  //         frm.doc.deduction = [];
  //         var net_income = 0;
  //         var income_tax_var = 0;
  //         $.each(r.message, function (i, e) {
  //           if (e.parentfield == "earning" && e.is_applicable) {
  //             let earning = frm.add_child("earning");
  //             earning.name1 = e.name1;
  //             earning.formula = e.formula;
  //             earning.is_tax_applicable = e.is_tax_applicable;
  //             earning.do_not_include_in_total = e.do_not_include_in_total;
  //             earning.earning_category = e.earning_category;
  //             earning.allowance_type = e.allowance_type;
  //             if (earning.earning_category == "Basic Salary") {
  //               earning.amount =
  //                 frm.doc.basic_salary -
  //                 (frm.doc.basic_salary / 26) * frm.doc.absent_days;

  //               net_income += frm.doc.basic_salary;
  //             } else if (earning.earning_category == "Allowance") {
  //               earning.amount = get_allowance_amount(
  //                 e.allowance_type,
  //                 frm.doc.role
  //               );
  //             } else if (earning.earning_category == "Overtime") {
  //               earning.amount = get_overtime_amount(frm.doc.overtime);
  //             } else {
  //               earning.amount = get_component_amount(
  //                 e.formula,
  //                 frm.doc.basic_salary,
  //                 e.amount
  //               );
  //             }
  //           } else if (e.parentfield == "deduction" && e.is_applicable) {
  //             let deduction = frm.add_child("deduction");
  //             deduction.name1 = e.name1;
  //             deduction.formula = e.formula;
  //             deduction.do_not_include_in_total = e.do_not_include_in_total;
  //             deduction.deduction_category = e.deduction_category;
  //             if (deduction.deduction_category == "Income Tax") {
  //               var taxable_income = 0.0;
  //               let myArray = cur_frm.doc.earning;
  //               myArray.forEach(function (x) {
  //                 if (x.is_tax_applicable) {
  //                   taxable_income += parseFloat(x.amount);
  //                 }
  //               });
  //               deduction.amount = get_income_tax_amount(
  //                 taxable_income,
  //                 frm.doc.basic_salary
  //               );

  //               net_income -= deduction.amount;
  //               income_tax_var = deduction.amount;
  //             } else if (deduction.deduction_category == "PP") {
  //               net_income -= frm.doc.basic_salary * 0.07;
  //               deduction.amount = get_pp_amount(net_income);
  //             } else if (deduction.deduction_category == "Staff Loan") {
  //               // Fetch staff loan amount and set it in deduction
  //               get_loan_amount(frm.doc.loan, function(loanAmount) {
  //                   deduction.amount = loanAmount;
  //                   refresh_field("deduction"); // Refresh deduction table after setting amount
  //               });
  //             } else {
  //               deduction.amount = get_component_amount(
  //                 e.formula,
  //                 frm.doc.basic_salary,
  //                 e.amount
  //               );
  //             }
  //           }
  //         });
  //         frm.doc.return_income_tax = income_tax_var;
  //         refresh_many(["earning", "deduction"]);
  //       });
  //   }
  // },

  end_date: function (frm) {
    fetch_absent_days(frm);
  },
});

function get_component_amount(formula, basic_salary, amount) {
  var val;
  frappe.call({
    method: "erpkenema.hr.doctype.salary_slip.salary_slip.get_component_amount",
    args: { formula: formula, basic_salary: basic_salary, amount: amount },
    async: false,
    callback: function (r) {
      val = r.message;
    },
  });
  return val;
}

function get_allowance_amount(allowance_type, role) {
  var allowance_amount;
  frappe.call({
    method: "erpkenema.hr.doctype.salary_slip.salary_slip.get_allowance_amount",
    args: { allowance_type: allowance_type, role: role },
    async: false,
    callback: function (r) {
      allowance_amount = r.message;
    },
  });
  return allowance_amount;
}

function get_income_tax_amount(taxable_income, basic_salary) {
  var income_tax_amount;
  frappe.call({
    method:
      "erpkenema.hr.doctype.salary_slip.salary_slip.get_income_tax_amount",
    args: { taxable_income: taxable_income, basic_salary: basic_salary },
    async: false,
    callback: function (r) {
      income_tax_amount = r.message;
    },
  });
  return income_tax_amount;
}

// function get_pp_amount(net_income) {
//   var pp_amount;
//   frappe.call({
//     method: "erpkenema.hr.doctype.salary_slip.salary_slip.get_pp_amount",
//     args: { net_income: net_income },
//     async: false,
//     callback: function (r) {
//       pp_amount = r.message;
//     },
//   });
//   return pp_amount;
// }

function get_pp_amount(net_income) {
  var pp_amount = null; // Initialize pp_amount as null
  frappe.call({
    method: "erpkenema.hr.doctype.salary_slip.salary_slip.get_pp_amount",
    args: { net_income: net_income },
    async: false,
    callback: function (r) {
      if (r.message) { // Check if r.message is defined
        pp_amount = r.message;
      }
    },
  });
  return pp_amount;
}


function get_overtime_amount(overtime) {
  var overtime_amount;

  // Check if overtime is provided
  if (overtime) {
    frappe.call({
      method: "erpkenema.hr.doctype.salary_slip.salary_slip.get_overtime_amount",
      args: { overtime: overtime },
      async: false,
      callback: function (r) {
        overtime_amount = r.message;
      },
    });
  } else {
    // Handle case where overtime is not provided
    overtime_amount = 0; // or any default value you prefer
  }

  return overtime_amount;
}


function get_loan_amount(loan, callback) {
  frappe.call({
    method: "erpkenema.hr.doctype.salary_slip.salary_slip.get_loan_amount",
    args: { loan: loan },
    callback: function (r) {
      if (r.message) {
        callback(r.message);
      }
    },
  });
}

function fetch_absent_days(frm) {
  if (frm.doc.employee && frm.doc.start_date && frm.doc.end_date) {
    frappe.call({
      method: "erpkenema.hr.doctype.salary_slip.salary_slip.get_absent_days",
      args: {
        employee: frm.doc.employee,
        start_date: frm.doc.start_date,
        end_date: frm.doc.end_date,
      },
      callback: function (r) {
        if (r.message && !r.exc) {
          frm.set_value("absent_days", r.message.absent_days);
          frm.refresh_field("absent_days");
        } else {
          // Set absent_days to 0 if there's an error or no records found
          frm.set_value("absent_days", 0);
          frm.refresh_field("absent_days");
        }
      },
    });
  } else {
    // Set absent_days to 0 if any required fields are missing
    frm.set_value("absent_days", 0);
    frm.refresh_field("absent_days");
  }
}

frappe.ui.form.on("Salary Slip", {
  onload: function (frm) {
    // Fetch staff loan amount on form load
    if (frm.doc.loan) {
      get_loan_amount(frm.doc.loan, function (loanAmount) {
        set_loan_deduction(frm, loanAmount);
      });
    }
  },
  salary_structure: function (frm) {
    // Handle salary structure change
    let sal_st = frm.doc.salary_structure;
    if (sal_st) {
      frappe.call({
        method:
          "erpkenema.hr.doctype.salary_slip.salary_slip.get_salary_structure",
        args: { salary_structure: sal_st },
        callback: function (r) {
          if (r.message) {
            // Reset earning and deduction tables
            frm.doc.earning = [];
            frm.doc.deduction = [];
            var net_income = 0;
            var income_tax_var = 0;

            // Loop through each item in the salary structure response
            $.each(r.message, function (i, e) {
              if (e.parentfield == "earning" && e.is_applicable) {
                let earning = frm.add_child("earning");
                earning.name1 = e.name1;
                earning.formula = e.formula;
                earning.is_tax_applicable = e.is_tax_applicable;
                earning.do_not_include_in_total = e.do_not_include_in_total;
                earning.earning_category = e.earning_category;
                earning.allowance_type = e.allowance_type;

                // Logic for calculating earnings
                if (earning.earning_category == "Basic Salary") {
                  earning.amount =
                    frm.doc.basic_salary -
                    (frm.doc.basic_salary / 26) * frm.doc.absent_days;
                  net_income += frm.doc.basic_salary;
                } else if (earning.earning_category == "Allowance") {
                  earning.amount = get_allowance_amount(
                    e.allowance_type,
                    frm.doc.role
                  );
                } else if (earning.earning_category == "Overtime") {
                  earning.amount = get_overtime_amount(frm.doc.overtime);
                } else {
                  earning.amount = get_component_amount(
                    e.formula,
                    frm.doc.basic_salary,
                    e.amount
                  );
                }
              } else if (e.parentfield == "deduction" && e.is_applicable) {
                let deduction = frm.add_child("deduction");
                deduction.name1 = e.name1;
                deduction.formula = e.formula;
                deduction.do_not_include_in_total = e.do_not_include_in_total;
                deduction.deduction_category = e.deduction_category;

                // Logic for calculating deductions
                if (deduction.deduction_category == "Income Tax") {
                  var taxable_income = 0.0;
                  frm.doc.earning.forEach(function (x) {
                    if (x.is_tax_applicable) {
                      taxable_income += parseFloat(x.amount);
                    }
                  });
                  deduction.amount = get_income_tax_amount(
                    taxable_income,
                    frm.doc.basic_salary
                  );
                  net_income -= deduction.amount;
                  income_tax_var = deduction.amount;
                } else if (deduction.deduction_category == "PP") {
                  net_income -= frm.doc.basic_salary * 0.07;
                  deduction.amount = get_pp_amount(net_income);
                } else if (deduction.deduction_category == "Staff Loan") {
                  // Fetch staff loan amount and set it in deduction
                  if (frm.doc.loan) {
                    get_loan_amount(frm.doc.loan, function (loanAmount) {
                      set_loan_deduction(frm, loanAmount);
                    });
                  }
                } else {
                  deduction.amount = get_component_amount(
                    e.formula,
                    frm.doc.basic_salary,
                    e.amount
                  );
                }
              }
            });

            frm.doc.return_income_tax = income_tax_var;
            refresh_many(["earning", "deduction"]);
          }
        },
      });
    }
  },
  loan: function (frm) {
    // Handle loan field change
    if (frm.doc.loan) {
      get_loan_amount(frm.doc.loan, function (loanAmount) {
        set_loan_deduction(frm, loanAmount);
      });
    } else {
      // Clear loan-related deductions if loan is not selected
      frm.doc.deduction.forEach(function (deduction) {
        if (deduction.deduction_category == "Staff Loan") {
          frm.get_field("deduction").grid.remove(deduction);
        }
      });
      refresh_field("deduction");
    }
  },
});

function get_loan_amount(loan, callback) {
  frappe.call({
    method: "erpkenema.hr.doctype.salary_slip.salary_slip.get_loan_amount",
    args: { loan: loan },
    callback: function (r) {
      if (r.message) {
        callback(r.message);
      }
    },
  });
}

function set_loan_deduction(frm, loanAmount) {
  // Set or update staff loan deduction amount
  frm.doc.deduction.forEach(function (deduction) {
    if (deduction.deduction_category == "Staff Loan") {
      deduction.amount = loanAmount;
    }
  });
  refresh_field("deduction");
}
