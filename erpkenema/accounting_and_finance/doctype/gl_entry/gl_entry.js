// Copyright (c) 2023, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('GL Entry', {
	refresh: function(frm) {
		frm.page.btn_secondary.hide()
	}
});
