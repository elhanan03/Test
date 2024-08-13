// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Information', {
	setup: function (frm) {
		frm.set_query("insurance_coverage_company", function () {
			return {
				filters: {
					"organization_type": frm.doc.credit_customers_category,
				}
			};
		});
	},

	validate: function (frm) {
		if (frm.doc.customer_type == 'Cash Customer') {
			let tin = frm.doc.tin_number.toString()
			if (tin.length != 10) {
				frappe.msgprint(("Enter a valid Tin Number"));
				frappe.validated = false;
			}
		}
	}
});
