// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Onboard Request Form', {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			var dct;
			frappe.call({
				method: "erpkenema.hr.doctype.employee_onboard_request_form.employee_onboard_request_form.get_data",
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
			frm.doc.approved_by_email = dct['approved_by_email']
			frm.doc.process_by = dct['process_by']
			frm.doc.process_by_email = dct['process_by_email']

			refresh_many(['branch', 'requested_by', 'requested_by_email', 'approved_by', 'approved_by_email', 'process_by', 'process_by_email'])
		}
	},
});

frappe.ui.form.on('List Of Jobs', 'salary_scale_name', function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	if (item.level && item.scale && item.salary_scale_name) {
		item.basic_salary = getBasicSalary(item.salary_scale_name, item.level, item.scale)
	}
	else {
		item.basic_salary = 0
	}
	frm.refresh_field('list_of_jobs')
});

frappe.ui.form.on('List Of Jobs', 'level', function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	if (item.salary_scale_name && item.scale && item.level) {
		item.basic_salary = getBasicSalary(item.salary_scale_name, item.level, item.scale)
	}
	else {
		item.basic_salary = 0
	}
	frm.refresh_field('list_of_jobs')
});

frappe.ui.form.on('List Of Jobs', 'scale', function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	if (item.salary_scale_name && item.level && item.scale) {
		item.basic_salary = getBasicSalary(item.salary_scale_name, item.level, item.scale)
	}
	else {
		item.basic_salary = 0
	}
	frm.refresh_field('list_of_jobs')
});


function getBasicSalary(salary_scale_name, level, scale) {
	var basic_salary_amount;
	frappe.call({
		method: "erpkenema.hr.doctype.employee_onboard_request_form.employee_onboard_request_form.get_basic_salary",
		args: { salary_scale_name: salary_scale_name, level: level, scale: scale },
		async: false,
		callback: function (r) {
			basic_salary_amount = r.message;
		},
	});
	return basic_salary_amount;
}