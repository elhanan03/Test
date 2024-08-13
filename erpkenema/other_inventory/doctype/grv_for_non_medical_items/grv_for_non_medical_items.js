// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('GRV For Non Medical Items', {
	setup: function (frm) {
		frm.set_query("purchase_order", function () {
			return {
				filters: {
					workflow_state: "Confirmed"
				},
			};
		});
	},

	purchase_order: function (frm) {
		frm.doc.non_medical_items = []
		let purchase_order = frm.doc.purchase_order;
		if (purchase_order) {
			frappe.call({
				method:
					"erpkenema.other_inventory.doctype.grv_for_non_medical_items.grv_for_non_medical_items.get_items",
				args: { purchase_order: frm.doc.purchase_order },
			})
				.done((r) => {
					$.each(r.message, function (i, e) {
						let items = frm.add_child("non_medical_items");
						items.item_name = e.item_name;
						items.item_category = e.item_category;
						items.quantity = e.quantity;
						items.uom = e.uom;
						items.manufacturer = e.manufacturer;
						items.brand = e.brand;
						items.unit_cost = e.unit_cost;
						items.total_cost = e.total_cost;

					});
					refresh_field("non_medical_items");
				});
		}
	},
});

frappe.ui.form.on("GRV For Non Medical Items Child", "unit_cost", function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	item.total_cost = item.quantity * item.unit_cost;
	frm.refresh_field("non_medical_items");
}
);
frappe.ui.form.on("GRV For Non Medical Items Child", "quantity", function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	item.total_cost = item.quantity * item.unit_cost;
	frm.refresh_field("non_medical_items");
}
);