// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
frappe.ui.form.on('Employee Onboarding', {
	setup: function (frm) {
		frm.set_query("job_applicant", function () {
			return {
				filters: {
					"status": "Accepted",
				}
			};
		});

		frm.set_query('job_offer', function () {
			return {
				filters: {

					"status": "Accepted",
				}
			};
		});
	},
	validate: function (frm) {
		frm.set_value(
			"full_name",
			String(frm.doc.first_name) +
			" " +
			String(frm.doc.middle_name) +
			" " +
			String(frm.doc.last_name)
		);
		let tin = String(frm.doc.tin_number);
		if (tin.length != 10) {
			frappe.msgprint("Enter a valid Tin Number");
			frappe.validated = false;
		}
	},
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.hr.doctype.employee_onboarding.employee_onboarding.get_field_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});

			frm.doc.process_by = dct['process_by']
			frm.doc.process_by_email = dct['process_by_email']
			frm.doc.approved_by = dct['approved_by']
			frm.doc.approved_by_email = dct['approved_by_email']
			frm.doc.finance_head = dct['finance_head']
			frm.doc.finance_head_email = dct['finance_head_email']

			refresh_many(['finance_head', 'finance_head_email', 'process_by', 'process_by_email', 'approved_by', 'approved_by_email'])
		}

		if (frm.doc.workflow_state == 'Confirmed') {
			frm.add_custom_button(__('Add To Employee List'), function () {
				frappe.model.with_doctype('Employee', function () {
					var new_doc = frappe.model.get_new_doc('Employee');
					// set default value for get_from_employee_ondoarding field
					new_doc.get_from_employee_onboarding = frm.doc.name;
					frappe.set_route('Form', 'Employee', new_doc.name);
				});
			});
		}
	},

	job_applicant: function (frm) {

		let docname = frm.doc.job_applicant;
		if (docname) {
			frappe.call({
				method: 'erpkenema.hr.doctype.employee_onboarding.employee_onboarding.get_phone',
				args: { doctype: "Job Applicant", docname: docname },
				async: false,
				callback: function (r) {
					frm.doc.phone = r.message
				}

			})
		}
		refresh_field('phone')

		let job_applicant = frm.doc.job_applicant;
		if (job_applicant) {
			frappe.call({
				method:
					"erpkenema.hr.doctype.employee_onboarding.employee_onboarding.get_qualification",
				args: { job_applicant: frm.doc.job_applicant },
			})
				.done((r) => {
					$.each(r.message, function (i, e) {
						let qualification = frm.add_child("qualification");
						qualification.universitycollege = e.universitycollege;
						qualification.department = e.department;
						qualification.education_type = e.education_type;
						qualification.education = e.education;
						qualification.year_of_completing = e.year_of_completing;
						qualification.cgpa = e.cgpa;

					});
					refresh_field("qualification");
				});
		}
	},

	birth_date: function (frm) {
		let birthdate = new Date(frm.doc.birth_date);
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
		}
	},

});


