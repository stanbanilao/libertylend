"""Smoke, interaction and responsive checks for Liberty Lend SA preview.

Requires: pip install playwright && python -m playwright install chromium
Run: python3 tests/test_site.py from repository root.
"""
from __future__ import annotations
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tests" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    base = ROOT.as_uri()
    browser = p.chromium.launch(headless=True)
    for label, width, height in [("desktop", 1440, 900), ("tablet", 768, 1024), ("mobile", 390, 844), ("small-mobile", 320, 700)]:
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        errors = []
        requests = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("request", lambda req: requests.append(req.url))
        response = page.goto(base + "/index.html", wait_until="networkidle")
        assert page.locator("h1").inner_text().startswith("A little more"), label
        assert page.locator("meta[name=robots]").get_attribute("content") == "noindex,nofollow"
        overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        assert overflow <= 1, f"{label}: horizontal overflow {overflow}px"
        assert not errors, f"{label}: JS exceptions {errors}"
        assert all(url.startswith(base) for url in requests), f"{label}: external request {requests}"
        page.screenshot(path=str(OUT / f"{label}.png"), full_page=True)
        if width <= 820:
            toggle = page.get_by_role("button", name="Open menu")
            assert toggle.is_visible(), label
            toggle.click()
            assert toggle.get_attribute("aria-expanded") == "true"
            page.get_by_role("navigation", name="Main navigation").get_by_role("link", name="Questions").click()
            assert toggle.get_attribute("aria-expanded") == "false"
        page.locator("#planner-form").scroll_into_view_if_needed()
        page.get_by_role("button", name="See my next steps").click()
        assert page.locator("#amount-error").is_visible(), f"{label}: should validate required amount"
        page.locator("#loan-amount").fill("3500")
        page.get_by_role("button", name="See my next steps").click()
        assert page.locator("#planner-result").is_visible(), f"{label}: planner result missing"
        assert "3" in page.locator("#result-title").inner_text(), label
        page.get_by_role("button", name="Start again").click()
        assert page.locator("#planner-form").is_visible(), f"{label}: reset failed"
        assert page.locator("#loan-amount").input_value() == "", label
        page.locator("#questions").scroll_into_view_if_needed()
        page.get_by_text("Is approval guaranteed?").click()
        assert page.locator("#questions details:nth-child(2)").get_attribute("open") is not None
        page.close()
        print(f"PASS {label} at {width}x{height}: layout, navigation, validation, planning, FAQ, no external requests")
    for subpage in ("privacy.html", "terms.html"):
        page = browser.new_page()
        page.goto(base + "/" + subpage, wait_until="networkidle")
        assert page.locator("h1").count() == 1
        assert page.get_by_role("link", name="Back to home").count() >= 1
        page.close()
        print("PASS " + subpage)
    browser.close()
