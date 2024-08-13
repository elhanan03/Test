// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stock Transfer Requisition Form', {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.inventory.doctype.stock_transfer_requisition_form.stock_transfer_requisition_form.get_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});
			frm.doc.branch = dct['branch']
			frm.doc.requested_by = dct['requested_by']
			frm.doc.requested_by_email = dct['requested_by_email']
			frm.doc.approved_by = dct['approved_by']
			frm.doc.approved_by = dct['approved_by']
			frm.doc.approved_by_email = dct['approved_by_email']

			refresh_many(['branch', 'requested_by', 'requested_by_email', 'approved_by', 'approved_by_email'])
		}
		if (frm.doc.workflow_state == 'Accepted') {
			frm.add_custom_button(__('Create A stock Transfer'), function () {
				frappe.set_route("List", "Stock Transfer Memo");
			});
		}
	},
	setup: function (frm) {
		frm.set_query("branch_manager", function () {
			return {
				filters: {
					"branch": frm.doc.from_branch,
				}
			};
		});
		frm.set_query("from_branch", function () {
			return {
				filters: {
					"name": ["!=", frm.doc.branch],
				}
			};
		});
	},
	from_branch: function (frm) {
		let from_branch = frm.doc.from_branch;
		if (from_branch) {
			var dct;
			frappe
				.call({
					method:
						"erpkenema.inventory.doctype.stock_transfer_requisition_form.stock_transfer_requisition_form.get_branch_manager",
					args: { from_branch: from_branch },
					async: false,
					callback: function (r) {
						dct = r.message;
					},
				});
			frm.doc.branch_manager = dct['branch_manager'];
			frm.doc.email = dct['email'];
		}
		refresh_many(["branch_manager", "email"]);
	},
});
// cur_frm.cscript.custom_validate = function (doc) {
// 	if (doc.date < get_today()) {
// 		msgprint("You can not select past date in Date");
// 		validated = false;
// 	}
// }
