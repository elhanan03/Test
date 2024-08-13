// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Sales Attachment", {
  refresh: function (frm) {
    if (frm.doc.__islocal) {
      frappe.call({
        method: "erpkenema.inventory.doctype.sales_attachment.sales_attachment.get_data",
        args: {},
        async: false,
        callback: function (r) {
          const dct = r.message;
          frm.set_value('branch_number', dct['branch_number']);
          frm.set_value('subcity', dct['subcity']);
          frm.set_value('woreda', dct['woreda']);
          frm.set_value('house_number', dct['house_number']);
          frm.set_value('prepared', dct['prepared']);
          frm.set_value('prepared_by_email', dct['prepared_by_email']);
          frm.refresh_fields(['branch_number', 'subcity', 'woreda', 'house_number', 'prepared', 'prepared_by_email']);
        }
      });
    }
  },
  sales_type: function (frm) {
    frm.set_value('to', null);
    frm.set_value('full_name', null);
    frm.set_value('tin_no', null);
    frm.set_value('organization', null);
    frm.set_value('credit_limit', null);
    frm.set_value('customer_subcity', null);
    frm.set_value('customer_woreda', null);
    frm.set_value('customer_house_number', null);
    frm.refresh_fields([
      'to',
      'full_name',
      'tin_no',
      'organization',
      'credit_limit',
      'customer_subcity',
      'customer_woreda',
      'customer_house_number'
    ]);

    const customerType = (frm.doc.sales_type === 'Credit Sales') ? 'Credit Customer' : 'Cash Customer';
    frm.set_query('to', { filters: { customer_type: customerType } });
  },

  setup: function (frm) {
    frm.set_query('to', { filters: { customer_type: 'Credit Customer' } });

    frm.set_query('cashier', { filters: { branch: frm.doc.branch_number } });

    frm.set_query('item_code', 'purchased_medicine', function (doc, cdt, cdn) {
      const row = frappe.get_doc(cdt, cdn);
      return {
        filters: [
          ['exp_date', '>=', frappe.datetime.add_days(frappe.datetime.get_today(), 1)],
          // ['exp_date', '>=', frappe.datetime.add_days(frappe.datetime.get_today(), 180)],
          ['quantity', '>', 0],
          ["kenema_pharmacy_drug_shop_number", "=", frm.doc.branch_number]
          // ['item_code', 'like', row.item_code],
          // ['unit', 'like', row.unit],
        ],
      };
    });
  },
});

frappe.ui.form.on("Purchased Medicine", "quantity", function (frm, cdt, cdn) {
  const item = frappe.get_doc(cdt, cdn);
  if (item.quantity > item.stock_quantity) {
    frappe.throw("Quantity cannot be greater than stock quantity.");
  } else {
    item.total_purchase_cost = item.quantity * item.unit_purchase_cost;
    item.total_price = item.quantity * item.unit_price;
    frm.refresh_field("purchased_medicine");
  }
});
