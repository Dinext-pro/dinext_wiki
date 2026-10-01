"""Point the Wiki desktop icon at /wiki-app on sites still holding the pre-rename /wiki link."""

import frappe


def execute():
	filters = {"app": "wiki", "link": "/wiki"}
	# icon_type exists on Frappe v16 Desktop Icon only.
	if frappe.db.has_column("Desktop Icon", "icon_type"):
		filters["icon_type"] = "App"
	frappe.db.set_value("Desktop Icon", filters, "link", "/wiki-app")
