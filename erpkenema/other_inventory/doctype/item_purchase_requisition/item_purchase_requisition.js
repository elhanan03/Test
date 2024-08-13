// Copyright (c) 2022, TechEthio IT Solution and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item purchase Requisition', {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.other_inventory.doctype.item_purchase_requisition.item_purchase_requisition.get_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});

			frm.doc.branch_name = dct['branch_name']
			frm.doc.branch_manager_name = dct['branch_manager_name']
			frm.doc.branch_manager_email = dct['branch_manager_email']
			frm.doc.finance_head = dct['finance_head']
			frm.doc.finance_head_email = dct['finance_head_email']
			frm.doc.hr_manager = dct['hr_manager']
			frm.doc.hr_manager_email = dct['hr_manager_email']
			frm.doc.operation_manager = dct['operation_manager']
			frm.doc.operation_manager_email = dct['operation_manager_email']
			frm.doc.hq_store_manager = dct['hq_store_manager']
			frm.doc.operation_manager_email = dct['hq_store_manager_email']


			refresh_many(['branch_name', 'finance_head', 'finance_head_email', 'hr_manager', 'hr_manager_email', 'branch_manager_name', 'branch_manager_email', 'operation_manager_email', 'operation_manager', 'hq_store_manager','hq_store_manager_email'])

		}

		if (frm.doc.workflow_state == 'Confirmed') {
			frm.add_custom_button(__('Add To Warehouse'), function () {
				frappe.set_route("List", "GRV For Non Medical Items");
			});
		}

		frm.set_query('purchase_order', function () {
			return {
				filters: {

					"workflow_state": "Sent",
				}
			};
		});
	},

	purchase_order: function (frm) {
		let purchase_order = frm.doc.purchase_order;
		if (purchase_order) {
			frappe.call({
				method:
					"erpkenema.other_inventory.doctype.item_purchase_requisition.item_purchase_requisition.get_items",
				args: { purchase_order: frm.doc.purchase_order },
			})
				.done((r) => {
					$.each(r.message, function (i, e) {
						let items = frm.add_child("list_of_items");
						items.item_name = e.item_name;
						items.item_category = e.item_category;
						items.quantity = e.quantity;
						items.uom = e.uom;
						items.manufacturer = e.manufacturer;
						items.brand = e.brand;
					});
					refresh_field("list_of_items");
				});
		}
	},


});
frappe.ui.form.on("Non Medical Items Child", "unit_cost", function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	item.total_cost = item.quantity * item.unit_cost;
	frm.refresh_field("list_of_items");
}
);
frappe.ui.form.on("Non Medical Items Child", "quantity", function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	item.total_cost = item.quantity * item.unit_cost;
	frm.refresh_field("list_of_items");
}
);
