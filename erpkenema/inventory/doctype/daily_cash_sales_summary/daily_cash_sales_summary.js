// Copyright (c) 2022, TechEthio IT Solution plc and contributors
// For license information, please see license.txt

frappe.ui.form.on("Daily Cash sales Summary", {
  refresh: function (frm) {
    if (frm.doc.__islocal) {
      var br;
      frappe.call({
        method:
          "erpkenema.inventory.doctype.daily_cash_sales_summary.daily_cash_sales_summary.get_data",
        args: {},
        async: false,
        callback: function (r) {
          br = r.message;
        },
      });
      frm.doc.branch = br;
      refresh_field("branch");
    }
  },

  sales_date: function (frm) {
    let sales_date = frm.doc.sales_date;
    if (sales_date) {
      frappe
        .call({
          method:
            "erpkenema.inventory.doctype.daily_cash_sales_summary.daily_cash_sales_summary.get_items",
          args: {
            sales_date: frm.doc.sales_date,
            branch_number: frm.doc.branch,
          },
          async: false,
        })
        .done((r) => {
          frm.doc.sales_breakdown = [];
          $.each(r.message, function (i, e) {
            let items = frm.add_child("sales_breakdown");
            items.cashier = e.cashier_full_name;

            var dispensarylist = e.dispensary_list;
            dispensarylist = dispensarylist.split(',')
            var joinedDispensaries = dispensarylist.join(', ');
            items.dispensary_list = joinedDispensaries;
            

            var value = e.amount_list;
            var list = value.split(",").map(parseFloat);
            var joinedValues = list.join(', ');
            items.amount_list = joinedValues;
            

            var ticketlist =  e.item_list;
            ticketlist = ticketlist.split(',')
            var joinedtickets = ticketlist.join(', ');
            items.sales_ticket_number = joinedtickets;

            items.amount_in_birr = e.total;
            items.vat = e.vat;
          });
          refresh_field("sales_breakdown");
        });
    }
  },
  update_variance: function (frm) {
    frm.doc.variance = [];
    frm.doc.sales_breakdown.forEach(function (row) {
      if (row.cash_over || row.cash_short) {
        let variance = frm.add_child("variance");
        variance.cashier = row.cashier;
        variance.ticket_number = row.sales_ticket_number;
        if (row.cash_over) {
          variance.overage_birr = row.amount;
        } else {
          variance.shortage_birr = row.amount;
        }
      }
    });
    frm.refresh_field("variance");
  },
});
frappe.ui.form.on("Sales Breakdown", "cash_over", function (frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  item.cash_short = 0;
  frm.refresh_field("sales_breakdown");
});

frappe.ui.form.on("Sales Breakdown", "cash_short", function (frm, cdt, cdn) {
  let item = locals[cdt][cdn];
  item.cash_over = 0;
  frm.refresh_field("sales_breakdown");
});
