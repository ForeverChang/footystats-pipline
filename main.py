from fastapi import FastAPI
from playwright.sync_api import sync_playwright
import os
import pandas as pd

app = FastAPI()

USERNAME = os.getenv("FOOTYSTATS_USER")
PASSWORD = os.getenv("FOOTYSTATS_PASS")

@app.post("/download-matches")
def download_matches():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://footystats.org/login")

        page.fill("#username", USERNAME)
        page.fill("#password", PASSWORD)
        page.click("#register_submit")
        page.wait_for_timeout(5000)  # wait for login

        # TODAY
        page.goto("https://footystats.org/")
        page.wait_for_selector('a[href*="matches_expanded"]')
        url_today = page.get_attribute('a[href*="matches_expanded"]', 'href')
        csv_today = page.request.get("https://footystats.org" + url_today)
        with open("matches_today.csv", "wb") as f:
            f.write(csv_today.body())

        # TOMORROW
        page.goto("https://footystats.org/tomorrow/")
        page.wait_for_selector('a[href*="matches_expanded"]')
        url_tomorrow = page.get_attribute('a[href*="matches_expanded"]', 'href')
        csv_tomorrow = page.request.get("https://footystats.org" + url_tomorrow)
        with open("matches_tomorrow.csv", "wb") as f:
            f.write(csv_tomorrow.body())

        browser.close()

    return {"status": "downloaded"}
