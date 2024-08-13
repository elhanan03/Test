// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Transfer', {
	setup: function (frm) {
		frm.set_query("employee1", function () {
			return {
				filters: {
					"workflow_state": "Authorized"
				}
			};
		});

		frm.set_query("employee", function () {
			return {
				filters: {
					"status": "Active"
				}
			};
		});
	},
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.hr.doctype.employee_transfer.employee_transfer.get_field_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});

			frm.doc.approved_by = dct['approved_by']
			frm.doc.approved_by_email = dct['approved_by_email']


			refresh_many(['approved_by', 'approved_by_email'])
		}
	},

	employee: function (frm) {	
		if (frm.doc.get_from_employee = 1) {
			var dct;
			frappe.call({
				method: "erpkenema.hr.doctype.employee_transfer.employee_transfer.get_employee_data",
				args: { name: frm.doc.employee },
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});
			frm.doc.from_branch = dct['from_branch']
			frm.doc.department = dct['department']
			frm.doc.designation = dct['designation']
			frm.doc.role = dct['role']

			refresh_many(['from_branch', 'department', 'designation', 'role'])
		}
	}
});

// cur_frm.cscript.custom_validate = function (doc) {
// 	if (doc.transfer_date < get_today()) {
// 		msgprint("You can not select past date in Transfer Date");
// 		validated = false;
// 	}
// }