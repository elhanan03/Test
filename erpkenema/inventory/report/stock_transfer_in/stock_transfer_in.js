// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */
var data;
var division;
frappe.call({
    method: "erpkenema.api.get_employee_data",
    args: {},
    async: false,
    callback: function (r) {
          data = r.message;
    },
});

if (data[0]){
	division = data[0].division
}
else{
	division = null
}

frappe.query_reports["Stock Transfer In"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.month_start(frappe.datetime.get_today()),
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today(),
		},
		{
			"depends_on": "eval: division == 'Head Office'",
			"fieldname": "branch_number",
			"fieldtype": "Link",
			"label": __("Branch"),
			"options": "Kenema Branches",
			"width": "80",
		},
	]
};
