// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Promotion', {
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
