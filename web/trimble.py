import time
from playwright.sync_api import sync_playwright
from core.auth import wait_for_verification_code

def launch_browser(headless, user_agent, viewport, locale):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    context = browser.new_context(
        user_agent=user_agent,
        viewport=viewport,
        locale=locale,
        java_script_enabled=True
    )
    page = context.new_page()
    return p, browser, context, page

def fill_basic_info(page, email, full_name):
    first_name = full_name.split()[0]
    last_name = full_name.split()[-1]
    page.fill("#given_name", first_name)
    page.fill("#family_name", last_name)
    page.fill("#email", email)
    page.click('label[for="tc_check"]')
    page.click("button[type='submit']")

def fill_verification_code(page, verification_code):
    page.wait_for_selector("input[name='code']", timeout=60000)
    page.fill("input[name='code']", verification_code)
    page.click("body")
    time.sleep(1)
    page.eval_on_selector('input[name="code"]', '''
        el => {
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.blur();
        }
    ''')
    page.wait_for_selector('button.btn.btn-primary.float-right:not([disabled])', timeout=10000)
    page.click('button.btn.btn-primary.float-right:not([disabled])')

def set_password(page, password):
    page.wait_for_selector("input[name='new_password']", timeout=60000)
    page.fill("input[name='new_password']", password)
    page.fill("input[name='confirm_password']", password)
    page.click("body")
    time.sleep(1)
    page.wait_for_selector('button.btn.btn-primary.float-right:not([disabled])', timeout=10000)
    page.click('button.btn.btn-primary.float-right:not([disabled])')

def skip_passkey(page):
    page.wait_for_selector("#skip_passkey", timeout=60000)
    page.click("#skip_passkey")
    page.click("body")

def fill_preferences_and_skip_mfa(page):
    page.locator("#set_preferences.workflow_step.active button.btn.btn-primary.float-right").click()
    page.wait_for_selector("div#mfa_info.workflow_step.active form#mfa_info a#skip", state="visible", timeout=60000)
    page.click("div#mfa_info.workflow_step.active form#mfa_info a#skip")

def create_trimble_account(email, full_name, password, email_token, headless=False, wait_after=5):
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36")
    viewport = {'width': 1280, 'height': 800}
    locale = 'pt-BR'

    p, browser, context, page = launch_browser(headless, user_agent, viewport, locale)

    page.goto("https://id.trimble.com/ui/sign_up.html?state=eyJhbGciOiJSUzI1NiIsImtpZCI6IjEiLCJ0eXAiOiJKV1QifQ.eyJvYXV0aF9wYXJhbWV0ZXJzIjp7ImNsaWVudF9pZCI6ImNiMzg4Yzk2LTY2YjUtNDdhMS04MzZmLWFlYzQ0YTdmMGJjYSIsInByb21wdCI6ImNyZWF0ZSIsInJlZGlyZWN0X3VyaSI6Imh0dHBzOi8vd3d3LnNrZXRjaHVwLmNvbS9sb2dpbiIsInJlc3BvbnNlX3R5cGUiOiJjb2RlIiwic2NvcGUiOiJvcGVuaWQgdHJpbWJsZS1teHAtbG9naW4iLCJzdGF0ZSI6Ii9lbiJ9LCJleHRyYV9wYXJhbWV0ZXJzIjp7fSwiaW50ZXJuYWxfcGFyYW1ldGVycyI6eyJzZW5kX2FjY291bnRfaWRfaW5fY2xhaW1zIjpmYWxzZSwiaXNfaW50ZXJuYWwiOnRydWV9LCJleHAiOiIyMDI1LTA2LTIyIDIyOjU1OjUzLjQwMjM5NCIsInJlcV9leHAiOiIyMDI1LTA2LTIyIDIyOjQ3OjUzLjQwMjQxOSIsInRjcF9yZXF1ZXN0X2lkIjoiNmEyNTJmMzFhMDhiNDhlNmI5NjdkY2YxMTZiMjM3NWEiLCJjb3JyZWxhdGlvbl9pZCI6ImUzZDUzMDNmYTM0ZjQzYTdhZjQ1N2Q2ZTZmMDM2Yzg2XzE3NTA2MzIzNTMiLCJzdGF0ZV90b2tlbl9pZCI6ImJkZDNmODcwLWIxY2QtNDQ2Yy1hOGU1LTU4MTZlYmMzNDY4ZSIsInVzZXJfdHlwZSI6MCwidWFtIjowLCJpcG0iOlsxLDAsMCwwLDEsMV19.Q9Y4DQaJiTqVff8qexPB2P20ozENtoVJYf2_Icxvxc8H9Q7JQABgyyLyGgaLT6aMso37T0Syd3tW1f9vo7sakC89BK0PmBVE9GfZTfiZTBI1cwPTmBEmmuir2jyQA6hyWj3Ofeq5H8xD2tgvk-SkPOhPQRJ1DuazChOLi486CvzydtgYblMFcgdrXaU2tQAkLeFry4pOW95Rzg5pmflJzU6S7VqXSkTwibyS7OnI4C0xqAQ_Mmh-ZhfrjhwgN-Z-9SBG1BItRRK6T9teRYSgSWzS_noPFrL8THMgON1Nu5FJ3ReHCbLkgL9FoqQEiwZmzeQLiSCuPhiZUEu6fD4Utw")
    time.sleep(5)

    fill_basic_info(page, email, full_name)

    print("⏳ Esperando código de verificação no e-mail...")
    verification_code = wait_for_verification_code(email_token)
    print(f"✅ Código recebido: {verification_code}")

    fill_verification_code(page, verification_code)
    set_password(page, password)
    skip_passkey(page)
    fill_preferences_and_skip_mfa(page)

    time.sleep(wait_after)

    browser.close()
    p.stop()

    return email, password
