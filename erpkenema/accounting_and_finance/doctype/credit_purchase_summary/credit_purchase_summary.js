// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Credit Purchase Summary', {
	credit_purchase_register: function (frm) {
		// frappe.msgprint('hello')
		let cpr = frm.doc.credit_purchase_register;
		if (cpr) {
			frappe.call({
				method: 'erpkenema.accounting_and_finance.doctype.credit_purchase_summary.credit_purchase_summary.get_items',
				args: { doc: frm.doc.credit_purchase_register },
				async: false
			}).done((r) => {
				frm.doc.summary = []
				$.each(r.message, function (i, e) {
					let items = frm.add_child('summary');
					items.supplier_name = e.supplier_name
					items.fs_number = e.fs_number
					items.total = e.credit
				})
				refresh_field('summary');
			})
		}
	},
});
