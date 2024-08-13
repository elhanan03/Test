// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Request for Non-medical items', {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.other_inventory.doctype.purchase_request_for_non_medical_items.purchase_request_for_non_medical_items.get_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message; 
				},
			});

			frm.doc.requested_by = dct['requested_by']
			frm.doc.requested_by_email = dct['requested_by_email']

			refresh_many(['requested_by', 'requested_by_email'])
		}

		frm.add_custom_button(__('Create Items'), function () {
			frappe.set_route("List", "Item purchase Requisition");
		});

	},

	
});
