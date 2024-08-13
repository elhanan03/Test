// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Journal Entry', {
	setup: function (frm) {
		frm.set_query("party_type", "account_entry", function () {
			return {
				query: "erpkenema.accounting_and_finance.doctype.party_type.party_type.get_party_type",
			};
		})
	},
});
// cur_frm.cscript.update_totals = function (doc) {
// 	var td = 0.0; var tc = 0.0;
// 	var account_entry = doc.account_entry || [];
// 	for (var i in account_entry) {
// 		td += flt(account_entry[i].debit, precision("debit", account_entry[i]));
// 		tc += flt(account_entry[i].credit, precision("credit", account_entry[i]));
// 	}
// 	var doc = locals[doc.doctype][doc.name];
// 	doc.total_debit = td;
// 	doc.total_credit = tc;
// 	doc.difference = flt((td - tc), precision("difference"));
// 	refresh_many(['total_debit', 'total_credit', 'difference']);
// }