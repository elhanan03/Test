// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Action Plan', {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.plan_and_budget.doctype.action_plan.action_plan.get_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});

			frm.doc.branch = dct['branch']
			frm.doc.prepared_by = dct['prepared_by']
			frm.doc.approved_by = dct['approved_by']
		}
		refresh_many(['branch', 'prepared_by', 'approved_by'])
	},

	previous_performance: function (frm) {
		let previous_performance = frm.doc.previous_performance;
		if (previous_performance) {
			frappe
				.call({
					method:
						"erpkenema.plan_and_budget.doctype.action_plan.action_plan.get_previous_performance",
					args: { previous_performance: previous_performance },
				})
				.done((r) => {
					frm.doc.monthly_plan = [];
					$.each(r.message, function (i, e) {
						let items = frm.add_child("monthly_plan");
						items.description = e.description;
						items.plan = e.performance;
	
					});

					refresh_field("monthly_plan");
				});
		}
	},

});

