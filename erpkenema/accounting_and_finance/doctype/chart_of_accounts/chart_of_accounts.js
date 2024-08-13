// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Chart Of Accounts', {
	setup: function (frm) {
		frm.set_query('account_type', function () {
			return {
				filters: {
					"root_type": frm.doc.root_type
				}
			};
		});
	}
});
