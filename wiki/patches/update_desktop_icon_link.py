"""Point an existing Wiki desktop icon at /wiki-app across supported Frappe versions."""

import frappe


def execute():
	if not frappe.db.exists("DocType", "Desktop Icon"):
		return
	filters = {"app": "wiki", "link": "/wiki"}
	if frappe.db.has_column("Desktop Icon", "icon_type"):
		filters["icon_type"] = "App"
	frappe.db.set_value("Desktop Icon", filters, "link", "/wiki-app")
