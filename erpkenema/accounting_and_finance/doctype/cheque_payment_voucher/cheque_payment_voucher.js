frappe.ui.form.on('Cheque Payment Voucher', {
  payment_type: function (frm) {
    clearFields(frm, ['payee', 'from_date', 'to_date', 'kenema_branches', 'fs_number', 'grand_total', 'total_vatable', 'tax_withhold', 'vat_withhold', 'payable_total', 'cheque_number', 'amount_in_words']);
    refresh_many(['payee', 'from_date', 'to_date', 'kenema_branches', 'fs_number', 'grand_total', 'total_vatable', 'tax_withhold', 'vat_withhold', 'payable_total', 'cheque_number', 'amount_in_words']);
  },

  to_date: function (frm) {
    let payee = frm.doc.payee;
    if (payee) {
      frappe.call({
        method: 'erpkenema.accounting_and_finance.doctype.cheque_payment_voucher.cheque_payment_voucher.get_credit_payment_data',
        args: {
          payee: frm.doc.payee,
          from_date: frm.doc.from_date,
          to_date: frm.doc.to_date
        },
        async: false
      }).done((r) => {
        var grand_total = 0;
        var total_vatable = 0;
        var branch_list = [];

        $.each(r.message, function (i, e) {
          if (e.status == 'Unpaid') {
            if (!branch_list.includes(e.branch_number)) {
              branch_list.push(e.branch_number);
            }

            var new_row = frappe.model.add_child(frm.doc, 'Cheque Payment Voucher', 'fs_number');
            new_row.fs_no = e.fs_no;

            grand_total += e.total;
            total_vatable += e.total_vatable;
          }
        });

        $.each(branch_list, function (i, branch) {
          var new_row = frappe.model.add_child(frm.doc, 'Cheque Payment Voucher', 'kenema_branches');
          new_row.branch = branch;
        });

        frm.doc.grand_total = grand_total;
        frm.doc.total_vatable = total_vatable;
        frm.doc.vat_withhold = total_vatable * 0.075;
        refresh_many(['kenema_branches', 'fs_number', 'grand_total', 'vat_withhold', 'total_vatable']);
      });
    }

    if (frm.doc.grand_total >= 10000) {
      frm.doc.tax_withhold = frm.doc.grand_total * 0.02;
      frm.doc.payable_total = frm.doc.grand_total - (frm.doc.tax_withhold + frm.doc.vat_withhold);
    } else {
      frm.doc.tax_withhold = 0;
      frm.doc.payable_total = frm.doc.grand_total - frm.doc.vat_withhold;
    }

    refresh_many(['payable_total', 'tax_withhold', 'difference']);
  },

  refresh: function (frm) {
    if (frm.doc.__islocal) {
      var dct;
      frappe.call({
        method: 'erpkenema.accounting_and_finance.doctype.cheque_payment_voucher.cheque_payment_voucher.get_data',
        args: {},
        async: false,
        callback: function (r) {
          dct = r.message;
        }
      });

      setFieldValues(frm, {
        finance_head: dct['finance_head'],
        finance_head_email: dct['finance_head_email'],
        finance_head1: dct['finance_head1'],
        finance_head_email1: dct['finance_head_email1'],
        hr_manager: dct['hr_manager'],
        hr_manager_email: dct['hr_manager_email'],
        deputy_manager: dct['deputy_manager'],
        deputy_manager_email: dct['deputy_manager_email'],
        hq_manager: dct['hq_manager'],
        hq_manager_email: dct['hq_manager_email'],
        hq_accountant: dct['hq_accountant'],
        hq_accountant_email: dct['hq_accountant_email'],
        audited_by_name: dct['audited_by_name'],
        audited_by_email: dct['audited_by_email']
      });

      refresh_many([
        'finance_head', 'finance_head_email', 'hr_manager', 'hr_manager_email', 'deputy_manager_email', 'deputy_manager',
        'hq_manager', 'hq_manager_email', 'hq_accountant', 'hq_accountant_email', 'audited_by_name', 'audited_by_email'
      ]);
    }
  }
});

function clearFields(frm, fields) {
  fields.forEach(function (field) {
    frm.doc[field] = '';
  });
}

function setFieldValues(frm, values) {
  for (var field in values) {
    if (values.hasOwnProperty(field)) {
      frm.doc[field] = values[field];
    }
  }
}
