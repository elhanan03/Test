// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Budget Allocation Page', {
	amount: function (frm) {
		frm.doc.left_balance = frm.doc.amount
		refresh_field('left_balance')
	}
});
