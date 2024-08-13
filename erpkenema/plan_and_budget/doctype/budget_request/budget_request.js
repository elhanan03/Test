// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Budget Request', {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.plan_and_budget.doctype.budget_request.budget_request.get_data",
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
			frm.doc.hq_manager = dct['hq_manager']
			frm.doc.hq_manager_email = dct['hq_manager_email']


			refresh_many(['branch_name', 'finance_head', 'finance_head_email', 'hr_manager', 'hr_manager_email', 'branch_manager_name', 'branch_manager_email', 'operation_manager_email', 'operation_manager', 'hq_manager', 'hq_manager_email'])

		}
	},
});
frappe.ui.form.on("List Of Items", "unit_cost", function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	item.total_cost = item.quantity * item.unit_cost;
	frm.refresh_field("list_of_items");
}
);
frappe.ui.form.on("List Of Items", "quantity", function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	item.total_cost = item.quantity * item.unit_cost;
	frm.refresh_field("list_of_items");
}
);