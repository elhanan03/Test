// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Loan management', {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.accounting_and_finance.doctype.loan_management.loan_management.get_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});

			frm.doc.hr_manager = dct['hr_manager']
			frm.doc.hr_manager_email = dct['hr_manager_email']



			refresh_many(['hr_manager', 'hr_manager_email'])

		}
	},
});
