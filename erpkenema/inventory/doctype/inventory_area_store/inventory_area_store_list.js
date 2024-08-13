frappe.listview_settings["Inventory Area Store"] = {
    get_indicator: function (doc) {
      if (doc.exp_date <= frappe.datetime.get_today()) {
        return [__("Expired"), "red"];
      }
      if (doc.quantity <= 100) {
        return [__("Shortage"), "yellow"];
      }
    },
  };