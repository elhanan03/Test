// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Credit Purchase Register', {
	branch: function (frm) {
		let branch = frm.doc.branch;
		if (branch) {
			frappe.call({
				method: 'erpkenema.inventory.doctype.credit_purchase_register.credit_purchase_register.get_items',
				args: { branch: frm.doc.branch, from_date: frm.doc.from_date, to_date: frm.doc.to_date },
				async: false
			}).done((r) => {
				frm.doc.credit_purchase = []
				$.each(r.message, function (i, e) {
					let items = frm.add_child('credit_purchase');
					items.supplier_name = e.supplier_name
					items.purchase_invoice_number = e.purchase_invoice_number
					items.supplier_tin_number = e.supplier_tin_number
					items.cash_register_number = e.cash_register_number
					items.fs_date = e.fs_date
					items.date = e.date
					items.debit  = e.total
					items.credit = e.total
					items.grv_no = e.name
					
				})
				refresh_field('credit_purchase');
			})
		}
	},
});
