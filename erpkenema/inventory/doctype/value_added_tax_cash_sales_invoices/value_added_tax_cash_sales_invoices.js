// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on('Value Added Tax Cash Sales Invoices', {
	setup: function(frm) {
		frm.set_query("item_code", "purchased_medicine", function(doc, cdt, cdn) {
			var row = locals[cdt][cdn];
			return {
				filters: [
					[
					  "exp_date",">=",frappe.datetime.add_days(frappe.datetime.get_today(), 180),
					],
					[
					  "description","like",row.description
					],
					[
					  "unit","like",row.unit
					],
				  ],
			}
		});
	}
});


frappe.ui.form.on("Purchased Medicine", "quantity", function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	if (item.quantity > item.stock_quantity){
	  frappe.throw('quantity can not be greater than stock quantity')
	} else {
	  item.total_price = item.quantity * item.unit_price;
	  frm.refresh_field("purchased_medicine");
	}
  });
  cur_frm.cscript.custom_validate = function(doc) {
	if (doc.date < get_today()) {
		msgprint("You can not select past date in From Date");
		validated = false;
	}
}