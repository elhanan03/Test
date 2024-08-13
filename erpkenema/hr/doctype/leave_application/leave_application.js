// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
frappe.ui.form.on('Leave Application', {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.hr.doctype.leave_application.leave_application.get_data",
				args: {},
				async: false,
				callback: function (r) {
					dct = r.message;
				},
			});

			frm.doc.branch_name = dct['branch_name']
			frm.doc.branch_manager_name = dct['branch_manager_name']
			frm.doc.branch_manager_email = dct['branch_manager_email']
			frm.doc.hr_manager = dct['hr_manager']
			frm.doc.hr_manager_email = dct['hr_manager_email']

			refresh_many(['branch_name', 'hr_manager', 'hr_manager_email', 'branch_manager_name', 'branch_manager_email'])

		}
	},
	employee: function(frm){
		frm.doc.employee_id=frm.doc.employee
		refresh_field('employee_id')
	},
	from_date: function (frm, cdt, cdn) {
		let item = locals[cdt][cdn];
		item.total_leave_days = frappe.datetime.get_diff(item.to_date, item.from_date);
		frm.refresh_field("total_leave_days");
	},
	to_date: function (frm, cdt, cdn) {
		let item = locals[cdt][cdn];
		item.total_leave_days = frappe.datetime.get_diff(item.to_date, item.from_date);
		frm.refresh_field("total_leave_days");
	}
});
