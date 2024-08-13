// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Request', {
	payment_type: function (frm) {
		frm.doc.document_type = null
		frm.doc.requested_by = null
		frm.doc.amount_in_figure = null
		refresh_many(['document_type', 'requested_by', 'amount_in_figure'])

		if (frm.doc.payment_type == 'Loan management') {
			frm.set_query("document_type", function () {
				return {
					filters: {
						"workflow_state": "Approved"
					}
				}
			});
		}
		else {
			frm.set_query("document_type", function () {
				return {
					filters: {}
				}
			});
		}
	},
	document_type: function (frm) {

		let doc_type = frm.doc.document_type;
		if (doc_type) {
			if (frm.doc.payment_type) {
				frappe
					.call({
						method:
							"erpkenema.accounting_and_finance.doctype.payment_request.payment_request.get_value",
						args: { doc: frm.doc.payment_type, doc_type: doc_type },
						async: false
					})
					.done((r) => {
						$.each(r.message, function (i, e) {
							if (frm.doc.payment_type == 'Loan management') {

								frm.doc.amount_in_figure = e.total_requested
								frm.doc.requested_by = e.requested_by
								frm.doc.hr_manager = e.hr_manager
							}
							else if (frm.doc.payment_type == 'Credit Purchase Register') {
								frm.doc.amount_in_figure = e.credit
								frm.doc.requested_by = e.supplier_name
							}
						});
					})
			}
		}
		refresh_many(['amount_in_figure', 'requested_by', 'hr_manager'])
	},
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.accounting_and_finance.doctype.payment_request.payment_request.get_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});

			frm.doc.finance_head = dct['finance_head']
			frm.doc.finance_head_email = dct['finance_head_email']
			frm.doc.hr_manager = dct['hr_manager']
			frm.doc.hr_manager_email = dct['hr_manager_email']
			frm.doc.deputy_manager = dct['deputy_manager']
			frm.doc.deputy_manager_email = dct['deputy_manager_email']
			frm.doc.hq_manager = dct['hq_manager']
			frm.doc.hq_manager_email = dct['hq_manager_email']


			refresh_many(['finance_head', 'finance_head_email', 'hr_manager', 'hr_manager_email', 'deputy_manager_email', 'deputy_manager', 'hq_manager', 'hq_manager_email'])

		}
	},

});
