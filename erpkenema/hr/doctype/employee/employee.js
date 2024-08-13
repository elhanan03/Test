// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee", {
  setup: function (frm) {
    frm.set_query("get_from_employee_onboarding", function () {
      return {
        filters: {
          workflow_state: "Confirmed"
        }
      };
    });
  },
  refresh: function (frm) {
    frm.add_custom_button(__('Employee Promotion'), function () {
      frappe.model.with_doctype('Employee Promotion', function () {
        var new_doc = frappe.model.get_new_doc('Employee Promotion');
        new_doc.employee = frm.doc.name;
        new_doc.full_name = frm.doc.full_name;
        new_doc.division = frm.doc.division;
        new_doc.branch = frm.doc.branch;
        new_doc.date_of_joining = frm.doc.date_of_joining;
        new_doc.from_employement_type = frm.doc.employement_type;
        frappe.set_route('Form', 'Employee Promotion', new_doc.name);
      });
    });
  },
  validate: function (frm) {
    frm.set_value("full_name", `${frm.doc.first_name} ${frm.doc.middle_name} ${frm.doc.last_name}`);

    let tin = String(frm.doc.tin_number);
    if (tin.length !== 10) {
      frappe.msgprint("Enter a valid Tin Number");
      frappe.validated = false;
    }
  },
  get_from_employee_onboarding: function (frm) {
    let docname = frm.doc.get_from_employee_onboarding;
    if (docname) {
      frappe.call({
        method: 'erpkenema.hr.doctype.employee.employee.get_phone_number',
        args: { doctype: "Employee Onboarding", docname: docname },
        async: false,
        callback: function (r) {
          frm.doc.phone_number = r.message;
          refresh_field('phone_number');
        }
      });
    } else {
      frm.doc.phone_number = "";
      refresh_field('phone_number');
    }

    let get_from_employee_onboarding = frm.doc.get_from_employee_onboarding;
    if (get_from_employee_onboarding) {
      frappe.call({
        method: 'erpkenema.hr.doctype.employee.employee.get_qualification',
        args: { get_from_employee_onboarding: get_from_employee_onboarding }
      }).done(function (r) {
        frm.doc.educational_qualification = [];
        $.each(r.message, function (i, e) {
          let educational_qualification = frm.add_child('educational_qualification');
          educational_qualification.universitycollege = e.universitycollege;
          educational_qualification.department = e.department;
          educational_qualification.education_type = e.education_type;
          educational_qualification.education = e.education;
          educational_qualification.year_of_completing = e.year_of_completing;
          educational_qualification.cgpa = e.cgpa;
        });
        refresh_field('educational_qualification');
      });
    }
  },
  salary_scale_name: updateBasicSalary,
  level: updateBasicSalary,
  scale: updateBasicSalary,
  birth_date: function (frm) {
    validateAge(frm, frm.doc.birth_date);
  }
});

function updateBasicSalary(frm) {
  if (frm.doc.level && frm.doc.scale && frm.doc.salary_scale_name) {
    frm.doc.basic_salary = getBasicSalary(frm.doc.salary_scale_name, frm.doc.level, frm.doc.scale);
  } else {
    frm.doc.basic_salary = 0;
  }
  refresh_field('basic_salary');
}

function getBasicSalary(salary_scale_name, level, scale) {
  var basic_salary_amount;
  frappe.call({
    method: "erpkenema.hr.doctype.employee.employee.get_basic_salary",
    args: { salary_scale_name, level, scale },
    async: false,
    callback: function (r) {
      basic_salary_amount = r.message;
    }
  });
  return basic_salary_amount;
}

function setRetirementDate(frm, birthDate) {
  if (birthDate) {
    frappe.call({
      method: "erpkenema.hr.doctype.employee.employee.get_retirement_date",
      args: { birth_date: birthDate },
      callback: function (r) {
        if (r.message) {
          frm.set_value("date_of_retirement", r.message);
        }
      }
    });
  }
}

function validateAge(frm, birthDate) {
  let birthdate = new Date(birthDate);
  let birthyear = birthdate.getFullYear();
  let age = new Date().getFullYear() - birthyear;

  if (age < 18 || age > 65) {
    frm.doc.birth_date = null;
    refresh_field("birth_date");
    if (age < 18) {
      frappe.throw("Users under 18 years of age cannot be created");
    } else {
      frappe.throw("Users above 65 years of age cannot be created");
    }
  } else {
    setRetirementDate(frm, birthDate);
  }
}
