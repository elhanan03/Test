// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Petty Cash Payment  Voucher', {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.accounting_and_finance.doctype.petty_cash_payment__voucher.petty_cash_payment__voucher.get_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});

			if (dct['branch']) {
				frm.set_query("allocated_budget", function () {
					return {
						filters: {
							branch: dct['branch'],
						},
					};
				});
				frm.doc.branch = dct['branch']
				frm.doc.division = "Branch"
			}
			else {
				frm.set_query("allocated_budget", function () {
					return {
						filters: {
							division: 'Head Office'
						},
					};
				});

				frm.doc.division = "Head Office"
			}

			frm.doc.prepared_by = dct['prepared_by']
			frm.doc.prepared_by_email = dct['prepared_by_email']
			frm.doc.approved_by = dct['approved_by']
			frm.doc.approved_by_email = dct['approved_by_email']
			frm.doc.authorized_by = dct['authorized_by']
			frm.doc.authorized_by_email = dct['authorized_by_email']

			refresh_many(['branch', 'division','prepared_by', 'approved_by', 'authorized_by', 'prepared_by_email', 'approved_by_email', 'authorized_by_email'])

		}
	},

});

