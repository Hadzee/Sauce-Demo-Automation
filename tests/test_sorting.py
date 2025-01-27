from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from user_data import USERNAME, PASSWORD

def test_sorting():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        login_page = LoginPage(page)
        login_page.goto()
        
        login_page.fill_username(USERNAME)
        login_page.fill_password(PASSWORD)
        login_page.click_on_login_button()
        
        inventory_page = InventoryPage(page)

        inventory_page.sort_products('az')
        prices = inventory_page.get_product_prices()
        assert inventory_page.verify_sorted(prices, ascending=True), "Products are not sorted A-Z"

        inventory_page.sort_products('za')
        prices = inventory_page.get_product_prices()
        assert inventory_page.verify_sorted(prices, ascending=False), "Products are not sorted Z-A"

        inventory_page.sort_products('lohi')
        prices = inventory_page.get_product_prices()
        assert inventory_page.verify_sorted(prices, ascending=True), "Products are not sorted low to high"

        inventory_page.sort_products('hilo')
        prices = inventory_page.get_product_prices()
        assert inventory_page.verify_sorted(prices, ascending=False), "Products are not sorted high to low"
        
        inventory_page.click_on_menu_button()
        inventory_page.click_on_logout_button()
        assert page.inner_text('h4') == "Accepted usernames are:", "Did not log out properly."

        browser.close()