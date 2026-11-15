"""Synthetic upgrade fixtures, available only through Frappe's test-server gate."""
import frappe
from frappe import _
from frappe.tests.ui_test_helpers import whitelist_for_tests
from frappe.utils.password import update_password

USER = "upgrade-wiki@example.com"
READER = "upgrade-wiki-reader@example.com"
TITLE = "Dinext upgrade smoke"


def _require_test_site():
	if not frappe.conf.allow_tests or not (frappe.flags.in_test or getattr(frappe.local, "dev_server", False)):
		frappe.throw(_("Upgrade fixtures require an enabled development test site"), frappe.PermissionError)
	frappe.only_for("System Manager")


@whitelist_for_tests
def csrf():
	_require_test_site()
	return frappe.sessions.get_csrf_token()


@whitelist_for_tests
def cleanup():
	_require_test_site()
	routes = ("dinext-upgrade-smoke", "dinext-upgrade-restricted")
	for name in frappe.get_all("Wiki Space", filters={"route": ("in", routes), "owner": USER}, pluck="name"):
		frappe.delete_doc("Wiki Space", name, force=True, ignore_permissions=True)
	for email in (READER, USER):
		if frappe.db.exists("User", email):
			frappe.delete_doc("User", email, force=True, ignore_permissions=True)


def _create_user(email, roles=()):
	password = frappe.generate_hash(length=24)
	user = frappe.get_doc({
		"doctype": "User", "email": email, "first_name": "Wiki Upgrade Test",
		"send_welcome_email": 0, "user_type": "System User", "language": "en",
	})
	user.insert(ignore_permissions=True)
	if roles:
		user.add_roles(*roles)
	update_password(email, password)
	return password


@whitelist_for_tests
def prepare():
	_require_test_site()
	cleanup()
	roles = [r for r in ("System Manager", "Wiki Manager", "Wiki User") if frappe.db.exists("Role", r)]
	password = _create_user(USER, roles)
	reader_password = _create_user(READER)
	result = {"user": USER, "password": password, "title": TITLE}
	from wiki.tests.factory import make_space, make_document
	space = make_space(route="dinext-upgrade-smoke", space_name=TITLE, owner=USER)
	document = make_document(parent=space.root_group, title=TITLE, content="Upgrade content before edit", owner=USER)
	restricted = make_space(
		route="dinext-upgrade-restricted", space_name="Restricted upgrade space",
		roles=[("System Manager", "Write")], owner=USER,
	)
	result.update({
		"space": space.name, "document": document.name, "route": document.route,
		"restricted": restricted.name, "reader": READER, "readerPassword": reader_password,
	})
	return result
