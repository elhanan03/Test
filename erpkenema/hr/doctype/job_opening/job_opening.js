// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Opening', {
	 setup: function (frm) {
    frm.set_query("employee_onboard_request", function () {
      return {
        filters: {
          workflow_state: "Authorized"
        }
      };
    });
  },
	onload: function (frm) {
		if (frm.doc.__islocal) {
			frm.set_value('opening_date', frappe.datetime.now_date());
			frm.refresh_field('opening_date');
		}
	},
	opening_date: function(frm) {
		var today = frappe.datetime.get_today();
	
		// Check if opening_date is not less than today
		if (frm.doc.opening_date < today) {
		  frappe.msgprint(__('The <b>opening date</b> cannot be in the past.'));
		  frappe.validated = false;
		  frm.set_value('opening_date', '');
		}
	},
	deadline_date: function (frm) {
		if (frm.doc.deadline_date < frm.doc.opening_date) {
			frappe.msgprint(__('The <b>deadline date</b> cannot be before the opening date.'));
			frappe.validated = false;
			frm.set_value('deadline_date', '');
		}

		var today = new Date();
		var deadline_date = new Date(frm.doc.deadline_date);

		if (deadline_date <= today) {
			setStatus(frm, 'Closed');
		} else {
			setStatus(frm, 'Open');
		}
	},

	refresh: function (frm) {
		var today = new Date();
		var deadline_date = new Date(frm.doc.deadline_date);

		if (deadline_date <= today && frm.doc.status !== 'Closed') {
			setStatus(frm, 'Closed');
		}
	},


	salary_scale_name: function (frm) {
		if (frm.doc.level && frm.doc.scale && frm.doc.salary_scale_name) {
			frm.doc.basic_salary = getBasicSalary(frm.doc.salary_scale_name, frm.doc.level, frm.doc.scale)
		}
		else {
			frm.doc.basic_salary = 0
		}
		refresh_field('basic_salary')
	},
	level: function (frm) {
		if (frm.doc.level && frm.doc.scale && frm.doc.salary_scale_name) {
			frm.doc.basic_salary = getBasicSalary(frm.doc.salary_scale_name, frm.doc.level, frm.doc.scale)
		}
		else {
			frm.doc.basic_salary = 0
		}
		refresh_field('basic_salary')
	},
	scale: function (frm) {
		if (frm.doc.level && frm.doc.scale && frm.doc.salary_scale_name) {
			frm.doc.basic_salary = getBasicSalary(frm.doc.salary_scale_name, frm.doc.level, frm.doc.scale)
		}
		else {
			frm.doc.basic_salary = 0
		}
		refresh_field('basic_salary')
	},
});

function setStatus(frm, status) {
	frm.set_value('status', status);
	frm.refresh_field('status');
}


function getBasicSalary(salary_scale_name, level, scale) {
	var basic_salary_amount;
	frappe.call({
		method: "erpkenema.hr.doctype.job_opening.job_opening.get_basic_salary",
		args: { salary_scale_name: salary_scale_name, level: level, scale: scale },
		async: false,
		callback: function (r) {
			basic_salary_amount = r.message;
		},
	});
	return basic_salary_amount;
}