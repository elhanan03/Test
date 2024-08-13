// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Transfer Request', {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.hr.doctype.employee_transfer_request.employee_transfer_request.get_field_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});
			
			frm.doc.approved_by = dct['approved_by']
			frm.doc.approved_by_email = dct['approved_by_email']
			frm.doc.authorized_by = dct['authorized_by']
			frm.doc.authorized_by_email = dct['authorized_by_email']

			refresh_many(['authorized_by', 'authorized_by_email', 'approved_by', 'approved_by_email'])
		}

		if (frm.doc.workflow_state == 'Authorized') {
			frm.add_custom_button(__('Transfer Employee'), function () {
				frappe.model.with_doctype('Employee Transfer', function () {
					var new_doc = frappe.model.get_new_doc('Employee Transfer');
					new_doc.employee1 = frm.doc.name;
					frappe.set_route('Form', 'Employee Transfer', new_doc.name);
				});
			});
		}
	},
	setup: function (frm) {
		frm.set_query("employee", function () {
			return {
				filters: {
					"status": "active"
				}
			};
		});
	},
});
