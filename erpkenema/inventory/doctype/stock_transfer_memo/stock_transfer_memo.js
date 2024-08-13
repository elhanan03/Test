// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stock Transfer Memo', {
	setup: function (frm) {
		frm.set_query("item_code", "stm", function (doc, cdt, cdn) {
			var row = locals[cdt][cdn];
			return {
				filters: [
					[
						"exp_date", ">=", frappe.datetime.add_days(frappe.datetime.get_today(), 180),
					],
					[
						"description", "like", row.description
					],
					[
						"unit", "like", row.unit
					],
				],
			};
		});

		frm.set_query("requisition_number", function () {
			return {
				filters: {
					"workflow_state": "Accepted"
				}
			};
		});
	},
	requisition_number: function (frm) {
		
		let req_num = frm.doc.requisition_number;
		if (req_num) {
			frappe
				.call({
					method:
						"erpkenema.inventory.doctype.stock_transfer_memo.stock_transfer_memo.get_data",
					args: { doc: req_num },
					async: false
				})
				.done((r) => {
					$.each(r.message, function (i, e) {
						frm.doc.to_branch = e.branch
						frm.doc.accepted_by = e.requested_by
						frm.doc.accepted_by_email = e.requested_by_email
						frm.doc.authorized_by = e.approved_by
						frm.doc.authorized_by_email = e.approved_by_email
						frm.doc.approved_by = e.branch_manager
						frm.doc.approved_by_email = e.email
					});
					refresh_many(['to_branch', 'approved_by', 'approved_by_email', 'accepted_by', 'accepted_by_email', 'authorized_by', 'authorized_by_email']);
				})
		}


		let to_branch = frm.doc.to_branch;
		if (to_branch) {
			var dct;
			frappe
				.call({
					method:
						"erpkenema.inventory.doctype.stock_transfer_memo.stock_transfer_memo.get_store_manager",
					args: { to_branch: "Merkato_1" },
					async: false,
					callback: function (r) {
						dct = r.message;
					},
				});
			frm.doc.received_by = dct['received_by'];
			frm.doc.received_by_email = dct['received_by_email'];

		}
		refresh_many(["received_by_email", "received_by"]);



		if (req_num) {
			frappe
				.call({
					method:
						"erpkenema.inventory.doctype.stock_transfer_memo.stock_transfer_memo.get_child_data",
					args: { doc: req_num },
					async: false
				})
				.done((r) => {
					frm.doc.stm = []
					$.each(r.message, function (i, e) {
						let items = frm.add_child('stm')
						items.description = e.description
						items.unit = e.uom
						items.quantity = e.quantity
					});
					refresh_field('stm');
				})
		}
	},
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.inventory.doctype.stock_transfer_memo.stock_transfer_memo.get_field_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});
			frm.doc.from_branch = dct['from_branch']
			frm.doc.issued_by = dct['issued_by']
			frm.doc.issued_by_email = dct['issued_by_email']

			refresh_many(['from_branch', 'issued_by', 'issued_by_email'])
		}
	},
	to_branch: function (frm) {
		let to_branch = frm.doc.to_branch;
		if (to_branch) {
			var dct;
			frappe
				.call({
					method:
						"erpkenema.inventory.doctype.stock_transfer_memo.stock_transfer_memo.get_store_manager",
					args: { to_branch: to_branch },
					async: false,
					callback: function (r) {
						dct = r.message;
					},
				});
			frm.doc.received_by = dct['received_by'];
			frm.doc.received_by_email = dct['received_by_email'];
		}
		refresh_many(["received_by_email", "received_by"]);
	},
});

frappe.ui.form.on('STM', 'quantity', function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	item.total_purchase_cost = item.quantity * item.unit_purchase_cost;
	item.total_selling_price = item.quantity * item.unit_selling_price;
	frm.refresh_field('stm');
});
frappe.ui.form.on('STM', 'item_code', function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	item.total_purchase_cost = item.quantity * item.unit_purchase_cost;
	item.total_selling_price = item.quantity * item.unit_selling_price;
	frm.refresh_field('stm');
});
// cur_frm.cscript.custom_validate = function (doc) {
// 	if (doc.date < get_today()) {
// 		msgprint("You can not select past date in Date");
// 		validated = false;
// 	}
// }