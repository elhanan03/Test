// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Applicant', {
	refresh: function(frm) {
		frm.set_query("job_opening", function () {
			return {
				filters:{
					"status": "Open"
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
	},
	birth_date: function (frm) {
		let birthdate = new Date(frm.doc.birth_date);
		let birthyear = birthdate.getFullYear();
		let age = new Date().getFullYear() - birthyear;
		
		if (age < 18 || age > 65) {
			frm.doc.birth_date = null;
			refresh_field("birth_date");
			
			if (age < 18) {
				frappe.throw("Applicant under 18 years not allowed to apply a job");
			} else {
				frappe.throw("Applicant Over 65 years not allowed to apply a job");
			}
		}
	},
});

	