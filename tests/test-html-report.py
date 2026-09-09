#!/usr/bin/env python3
"""Regression checks for the architecture report's public HTML scaffold."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


class HeadMetadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.viewports = []

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.in_head = True
        if tag == "meta" and self.in_head:
            values = dict(attrs)
            if values.get("name", "").lower() == "viewport":
                self.viewports.append(values.get("content", ""))

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False


class ReportScaffoldTests(unittest.TestCase):
    def test_mobile_uses_device_width_instead_of_scaled_desktop(self):
        root = Path(__file__).resolve().parents[1]
        source = root / "skills/engineering/improve-codebase-architecture/HTML-REPORT.md"
        match = re.search(r"```html\s*\n(<!doctype html>.*?)(?:\n```)",
                          source.read_text(), flags=re.IGNORECASE | re.DOTALL)
        self.assertIsNotNone(match, "The public full-document scaffold must exist")
        parser = HeadMetadata()
        parser.feed(match.group(1))
        self.assertEqual(len(parser.viewports), 1,
                         "The document head must define one mobile viewport")
        settings = {}
        for part in parser.viewports[0].split(","):
            name, separator, value = part.partition("=")
            if separator:
                settings[name.strip().lower()] = value.strip()
        self.assertEqual(settings.get("width"), "device-width")
        self.assertEqual(float(settings.get("initial-scale", "nan")), 1.0)


if __name__ == "__main__":
    unittest.main()
