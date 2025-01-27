from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from user_data import USERNAME, PASSWORD

def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        login_page = LoginPage(page)
        login_page.goto()
        
        random_username = login_page.generate_random_username()
        login_page.fill_username(random_username)
        login_page.fill_password(PASSWORD)
        login_page.click_on_login_button()
        assert page.inner_text('h3') == "Epic sadface: Username and password do not match any user in this service", "Logged in with invalid credentials."
        
        login_page.fill_username(USERNAME)
        login_page.fill_password(PASSWORD)
        login_page.click_on_login_button()
        assert page.title() == "Swag Labs", "Did not log in properly."
        
        inventory_page = InventoryPage(page)
        inventory_page.click_on_menu_button()
        inventory_page.click_on_logout_button()
        assert page.inner_text('h4') == "Accepted usernames are:", "Did not log out properly."

        browser.close()