// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bank Account', {
	setup: function (frm) {
		frm.set_query("party_type", function () {
			return {
				query: "erpkenema.accounting_and_finance.doctype.party_type.party_type.get_party_type",
			};
		})
	},

	party: function (frm) {
		let party_type = frm.doc.party_type
		let party = frm.doc.party
		var dct;
		if (party) {
			frappe.call({
				method: "erpkenema.accounting_and_finance.doctype.bank_account.bank_account.get_account_number",
				args: { doctype: party_type, doc: party },
				async: false,
				callback: function (r) {

					dct = r.message
				},
			});
			frm.doc.account_number = dct["bank_account_no"]
			refresh_field('account_number')
		}
	}
});
