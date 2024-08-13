// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Petty Cash Summary', {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.accounting_and_finance.doctype.petty_cash_summary.petty_cash_summary.get_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});

			frm.doc.branch = dct['branch']
			frm.doc.prepared_by = dct['prepared_by']
			frm.doc.prepared_by_email = dct['prepared_by_email']
			frm.doc.approved_by = dct['approved_by']
			frm.doc.approved_by_email = dct['approved_by_email']

			refresh_many(['branch', 'prepared_by', 'prepared_by_email', 'approved_by', 'approved_by_email'])
		}
	},

	from_date: function (frm) {
		if (frm.doc.to_date) {
			let from_date = frm.doc.from_date;
			if (from_date) {
				frappe.call({
					method: 'erpkenema.accounting_and_finance.doctype.petty_cash_summary.petty_cash_summary.get_items',
					args: { from_date: frm.doc.from_date, to_date: frm.doc.to_date, branch: frm.doc.branch },
					async: false
				}).done((r) => {
					frm.doc.list_of_paid = []
					$.each(r.message, function (i, e) {
						let items = frm.add_child('list_of_paid');
						items.paye = e.payee
						items.amount = e.payable_amounts_in_figure

					})
					refresh_field('list_of_paid');
				})
			}
		}
	},
	to_date: function (frm) {
		let to_date = frm.doc.to_date;
		if (to_date) {
			frappe.call({
				method: 'erpkenema.accounting_and_finance.doctype.petty_cash_summary.petty_cash_summary.get_items',
				args: { from_date: frm.doc.from_date, to_date: frm.doc.to_date, branch: frm.doc.branch },
				async: false
			}).done((r) => {
				frm.doc.list_of_paid = []
				$.each(r.message, function (i, e) {
					let items = frm.add_child('list_of_paid');
					items.paye = e.payee
					items.amount = e.payable_amounts_in_figure

				})
				refresh_field('list_of_paid');
			})
		}
	},
});
