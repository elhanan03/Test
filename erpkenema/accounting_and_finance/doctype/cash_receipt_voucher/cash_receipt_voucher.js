// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cash Receipt Voucher', {

	payer: function (frm) {

		let payer = frm.doc.payer;
		if (payer) {
			if (payer) {

				var val;
				frappe.call({
					method: "erpkenema.accounting_and_finance.doctype.cash_receipt_voucher.cash_receipt_voucher.get_data",
					args: { payer: payer, from_date: frm.doc.from_date, to_date: frm.doc.to_date },
					async: false,
					callback: function (r) {
						val = r.message;
					},
				});

				frm.doc.amount_in_figure = val

			}
		}
		refresh_many(['amount_in_figure', 'amount_in_words'])
	}

});
