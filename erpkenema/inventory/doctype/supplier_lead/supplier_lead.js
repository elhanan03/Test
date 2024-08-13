// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Supplier_Lead', {
	validate: function (frm) {
		let tin = String(frm.doc.tin);
		if (tin.length != 10) {
			frappe.msgprint("Enter a valid Tin Number");
			frappe.validated = false;
		}
	},
});
