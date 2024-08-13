// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Offer', {
	refresh: function(frm) {
	frm.set_query("job_applicant", function () {
		return {
			filters:{
				"status": "Accepted"
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
	}

});
