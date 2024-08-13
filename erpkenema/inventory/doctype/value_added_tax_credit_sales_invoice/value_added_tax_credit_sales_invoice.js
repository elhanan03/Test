// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Value Added Tax Credit Sales Invoice', {
	setup: function (frm) {
		frm.set_query("to", function () {
			return {
				filters: {
					"organization_type": frm.doc.credit_user_type,
				}
			};
		});

		frm.set_query("id_no", "patient_list", function (doc, cdt, cdn) {
			var row = locals[cdt][cdn];
			return {
				filters: {
					"customer_type": "Credit Customer",
				}
			};
		});
	},

	to: function (frm) {
		let to_org = frm.doc.to;
		if (to_org) {
			frappe.call({
				method: 'erpkenema.inventory.doctype.value_added_tax_credit_sales_invoice.value_added_tax_credit_sales_invoice.get_items',
				args: { from_branch: frm.doc.frombranch_no, to_org: frm.doc.to, from_date: frm.doc.from_date, to_date: frm.doc.to_date },
				async: false
			}).done((r) => {
				frm.doc.patient_list = []
				$.each(r.message, function (i, e) {
					let items = frm.add_child('patient_list');
					items.prescription_no = e.name
					items.id_no = e.id_number
					items.name_of_patient = e.full_name
					items.total = e.total
					items.vat = e.vat
					items.total_for_vat_items = e.total_for_vat_items
					items.prescription_amount = e.total_inc_vat
				})
				refresh_field('patient_list');
			})
		}
	},
});
