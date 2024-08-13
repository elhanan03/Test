// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Attendance', {
	before_save: function (frm) {
		if (frm.doc.status == "Absent") {
			frm.doc.number_status = 0
		}
		else {
			frm.doc.number_status = 1
		}
	}
});
// cur_frm.cscript.custom_validate = function (doc) {
// 	if (doc.date < get_today()) {
// 		msgprint("You can not select past date in From Date");
// 		validated = false;
// 	}
// }

// cur_frm.cscript.custom_validate = function(doc) {
//     if (doc.date < get_today()) {
//         msgprint("You cannot select a past date.");
//         return false;
//     }
//     return true;
// };