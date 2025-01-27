from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from user_data import USERNAME, PASSWORD, EXPECTED_ITEMS

def test_remove_from_cart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        login_page = LoginPage(page)
        login_page.goto()
        
        login_page.fill_username(USERNAME)
        login_page.fill_password(PASSWORD)
        login_page.click_on_login_button()
        
        inventory_page = InventoryPage(page)
        inventory_page.add_item_and_check_cart("#add-to-cart-sauce-labs-backpack")
        inventory_page.add_item_and_check_cart("#add-to-cart-sauce-labs-bike-light")
        inventory_page.add_item_and_check_cart("#add-to-cart-sauce-labs-bolt-t-shirt")
        
        inventory_page.verify_items_in_cart(EXPECTED_ITEMS)
        
        inventory_page.remove_item_and_check_cart_decrease("#remove-sauce-labs-backpack")
        inventory_page.remove_item_and_check_cart_decrease("#remove-sauce-labs-bike-light")
        inventory_page.remove_item_and_check_cart_decrease("#remove-sauce-labs-bolt-t-shirt")
        inventory_page.click_on_menu_button()
        inventory_page.click_on_logout_button()
        assert page.inner_text('h4') == "Accepted usernames are:", "Did not log out properly."
        
        browser.close()