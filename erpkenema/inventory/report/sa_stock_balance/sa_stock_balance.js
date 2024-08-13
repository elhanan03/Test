// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt
/* eslint-disable */


function getUserBranch(user_id) {
	return new Promise(function (resolve, reject) {
		frappe.call({
			method: "erpkenema.inventory.report.sa_stock_balance.sa_stock_balance.get_employee_branch",
			args: {
				user: user_id,
			},
			callback: function (response) {
				if (response && response.message && response.message !== null) {
					resolve(response.message);
				} else {
					reject(new Error("User Branch not found or an error occurred."));
				}
			},
			error: function (xhr, textStatus, errorThrown) {
				console.error(textStatus, errorThrown);
				reject(new Error("AJAX error occurred."));
			},
		});
	});
}

function setDefaultBranchFilterValue() {
	getUserBranch(frappe.session.user)
		.then(function (userBranchValue) {
			const branchFilter = frappe.query_reports["SA Stock Balance"].filters.find(filter => filter.fieldname === "branch");
			if (userBranchValue) {
				branchFilter.default = userBranchValue;
				branchFilter.read_only = 1;
			} else {
				branchFilter.default = null;
				branchFilter.read_only = 0;
			}
		})
		.catch(function (error) {
			console.error(error);
			// If an error occurs, remove the default value and make the filter editable
			frappe.query_reports["SA Stock Balance"].filters.find(filter => filter.fieldname === "branch").default = null;
			frappe.query_reports["SA Stock Balance"].filters.find(filter => filter.fieldname === "branch").read_only = 0;
		});
}

// Call the function to set the default value for the "Branch" filter
setDefaultBranchFilterValue();

frappe.query_reports["SA Stock Balance"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.year_start(frappe.datetime.get_today())
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "branch",
			"label": __("Branch"),
			"fieldtype": "Link",
			"options": "Kenema Branches",
			"width": "200",
			"read_only": 0,
		},
	],
};
