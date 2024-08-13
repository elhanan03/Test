// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Annual Budget plan Request Letter', {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.plan_and_budget.doctype.annual_budget_plan_request_letter.annual_budget_plan_request_letter.get_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});
			frm.doc.plan_and_budget_manager = dct['plan_and_budget_manager']
			frm.doc.plan_and_budget_manager_email = dct['plan_and_budget_manager_email']
			
			refresh_many(['plan_and_budget_manager', 'plan_and_budget_manager_email'])
		}
		frm.add_custom_button(__('Create Budget Plan'), function () {
			frappe.set_route("List", "Budget Request");
		});


	},
});
// cur_frm.cscript.custom_validate = function(doc) {
// 	if (doc.date < get_today()) {
// 		msgprint("You can not select past date in From Date");
// 		validated = false;
// 	}
// }

