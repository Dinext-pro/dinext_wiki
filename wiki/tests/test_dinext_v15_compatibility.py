"""Regression checks for the Dinext compatibility changes retained during upgrades."""
import importlib.util
from pathlib import Path
import sys
from types import ModuleType
import unittest
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[1]


def load_file(path, frappe):
    spec = importlib.util.spec_from_file_location("dinext_compatibility_subject", ROOT / path)
    module = importlib.util.module_from_spec(spec)
    utils = ModuleType("frappe.utils")
    with patch.dict(sys.modules, {"frappe": frappe, "frappe.utils": utils}):
        spec.loader.exec_module(module)
    return module


class TestDesktopIconCompatibility(unittest.TestCase):
    def test_missing_desktop_icon_doctype_is_skipped(self):
        frappe = Mock()
        frappe.db.exists.return_value = False
        load_file("patches/update_desktop_icon_link.py", frappe).execute()
        frappe.db.has_column.assert_not_called()
        frappe.db.set_value.assert_not_called()

    def test_v15_icon_is_updated_without_v16_column(self):
        frappe = Mock()
        frappe.db.exists.return_value = True
        frappe.db.has_column.return_value = False
        load_file("patches/update_desktop_icon_link.py", frappe).execute()
        frappe.db.set_value.assert_called_once_with(
            "Desktop Icon", {"app": "wiki", "link": "/wiki"}, "link", "/wiki-app"
        )

    def test_v16_icon_retains_app_type_filter(self):
        frappe = Mock()
        frappe.db.exists.return_value = True
        frappe.db.has_column.return_value = True
        load_file("patches/update_desktop_icon_link.py", frappe).execute()
        frappe.db.set_value.assert_called_once_with(
            "Desktop Icon", {"app": "wiki", "link": "/wiki", "icon_type": "App"},
            "link", "/wiki-app"
        )


class TestOptionalPulse(unittest.TestCase):
    def test_import_and_capture_work_without_frappe_pulse(self):
        frappe = ModuleType("frappe")
        module = load_file("telemetry.py", frappe)
        self.assertIsNone(module.frappe_telemetry)
        self.assertIsNone(module.capture("document_saved"))
        self.assertEqual(module.reader_config(), {"enabled": False})


if __name__ == "__main__":
    unittest.main()
